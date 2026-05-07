import json
import logging
import os
import asyncio
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from src.reddit_scraper import RedditScraper
from src.tts_engine import TTSEngine
from src.video_generator import VideoGenerator
from src.story_generator import StoryGenerator
from src.uploader import Uploader
from src.utils import download_sample_background

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "process.log")),
        logging.StreamHandler()
    ]
)

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

async def run_pipeline():
    try:
        config = load_config()
        logging.info("Starting Viral Story Factory pipeline...")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(base_dir, config['settings']['output_folder'])
        os.makedirs(output_folder, exist_ok=True)
        
        bg_folder = os.path.join(base_dir, config['settings']['background_folder'])
        os.makedirs(bg_folder, exist_ok=True)

        # Ensure backgrounds exist
        download_sample_background(bg_folder)
        
        # Determine source of story
        if config.get('ai', {}).get('enabled', False):
            logging.info("AI Story Generation enabled. Generating story...")
            ai_gen = StoryGenerator(api_key=config['ai']['api_key'], model=config['ai']['model'])
            story = ai_gen.generate_story(
                topic=config['ai'].get('topic', 'a random dramatic event'),
                subreddit=config['ai'].get('subreddit_style', 'AmItheAsshole')
            )
        else:
            scraper = RedditScraper(
                config['reddit']['client_id'],
                config['reddit']['client_secret'],
                config['reddit']['user_agent']
            )
            story = scraper.get_story(config['settings']['subreddit'])
        
        if not story:
            logging.error("Failed to obtain story.")
            return

        logging.info(f"Story obtained: {story['title']}")

        # 2. TTS Engine
        tts = TTSEngine(config['voice']['voice_name'])
        audio_path = os.path.join(output_folder, f"{story['original_id']}.mp3")
        
        full_text = f"{story['title']}. {story['body']}"
        duration, subtitles = await tts.generate_audio(full_text, audio_path)
        
        if duration > config['settings']['max_duration_seconds']:
            logging.warning(f"Story too long ({duration:.2f}s). Skipping.")
            return

        # 3. Video Generation
        video_gen = VideoGenerator(config)
        # Fix font path if relative
        if not config['settings']['font_path'].startswith('/'):
            video_gen.font_path = os.path.join(base_dir, config['settings']['font_path'])
            
        header_path = video_gen.create_reddit_header(config['settings']['subreddit'], story['title'])
        
        output_filename = f"{story['original_id']}_final.mp4"
        final_path = video_gen.generate_video(audio_path, subtitles, header_path, output_filename)
        
        logging.info(f"Successfully generated video: {final_path}")
        
        # 4. Metadata Generation
        caption = f"{story['title']} #redditstories #storytime #reddit #perspective"
        metadata_path = os.path.join(output_folder, f"{story['original_id']}_metadata.txt")
        with open(metadata_path, 'w') as f:
            f.write(f"Title: {story['title']}\n\n")
            f.write(f"Caption: {caption}\n")
            
        logging.info(f"Metadata saved to {metadata_path}")
        
        # 5. Multi-Platform Upload
        uploader = Uploader(config)
        uploader.upload_all(final_path, caption)

    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(run_pipeline())

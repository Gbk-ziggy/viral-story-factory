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
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "reddit": {},
            "settings": {
                "subreddit": "AmItheAsshole",
                "max_duration_seconds": 60,
                "background_folder": "assets/backgrounds",
                "output_folder": "output",
                "font_path": "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
            },
            "voice": {"voice_name": "en-US-ChristopherNeural"},
            "ai": {"enabled": True},
            "upload": {"instagram": {"enabled": False}, "tiktok": {"enabled": False}, "youtube": {"enabled": False}}
        }
    
    # Override with env vars for deployment
    if os.getenv('REDDIT_CLIENT_ID'):
        config['reddit']['client_id'] = os.getenv('REDDIT_CLIENT_ID')
    if os.getenv('REDDIT_CLIENT_SECRET'):
        config['reddit']['client_secret'] = os.getenv('REDDIT_CLIENT_SECRET')
    if os.getenv('REDDIT_USER_AGENT'):
        config['reddit']['user_agent'] = os.getenv('REDDIT_USER_AGENT')
    if os.getenv('OPENAI_API_KEY'):
        config['ai']['api_key'] = os.getenv('OPENAI_API_KEY')
    
    return config

async def run_pipeline(subreddit_override=None, ai_override=None):
    try:
        config = load_config()
        if subreddit_override:
            config['settings']['subreddit'] = subreddit_override
        if ai_override is not None:
            config['ai']['enabled'] = ai_override

        logging.info(f"Starting Viral Story Factory pipeline (Subreddit: {config['settings']['subreddit']}, AI: {config['ai']['enabled']})...")
        
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

        return final_path

    except Exception as e:
        logging.error(f"An error occurred during pipeline execution: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(run_pipeline())

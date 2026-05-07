import os
import random
import logging
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip, ColorClip, concatenate_videoclips

class VideoGenerator:
    def __init__(self, config):
        self.config = config
        self.background_folder = config['settings']['background_folder']
        self.output_folder = config['settings']['output_folder']
        self.font_path = config['settings']['font_path']
        
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def select_random_background(self):
        bg_path = os.path.join("/home/team/shared/viral-story-factory", self.background_folder)
        if not os.path.exists(bg_path):
             return None
        videos = [f for f in os.listdir(bg_path) if f.endswith(('.mp4', '.mov', '.mkv'))]
        if not videos:
            logging.error(f"No background videos found in {bg_path}")
            return None
        return os.path.join(bg_path, random.choice(videos))

    def create_reddit_header(self, subreddit, title, author="RedditUser", upvotes="1.2k"):
        """Generates a Reddit-style header image using Pillow."""
        # Constants for Dark Mode colors
        BG_COLOR = (26, 26, 27)
        TEXT_COLOR = (215, 218, 220)
        SUBREDDIT_COLOR = (255, 69, 0) # Orange-ish
        
        width, height = 800, 300
        img = Image.new('RGB', (width, height), color=BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        try:
            # Attempt to load font, fallback to default
            font_main = ImageFont.truetype(self.font_path, 30)
            font_sub = ImageFont.truetype(self.font_path, 20)
        except:
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()
            
        draw.text((20, 20), f"r/{subreddit}", fill=SUBREDDIT_COLOR, font=font_sub)
        draw.text((20, 50), f"Posted by u/{author}", fill=(129, 131, 132), font=font_sub)
        
        # Wrap title text
        lines = []
        words = title.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if draw.textbbox((0, 0), test_line, font=font_main)[2] < width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        y_offset = 100
        for line in lines:
            draw.text((20, y_offset), line, fill=TEXT_COLOR, font=font_main)
            y_offset += 40
            
        header_path = os.path.join(self.output_folder, "reddit_header.png")
        img.save(header_path)
        return header_path

    def create_caption_image(self, word, font_size=100):
        """Creates a transparent image with a single word using Pillow."""
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except:
            font = ImageFont.load_default()
            
        # Get text size
        img_dummy = Image.new('RGBA', (1, 1))
        draw_dummy = ImageDraw.Draw(img_dummy)
        bbox = draw_dummy.textbbox((0, 0), word.upper(), font=font)
        w = bbox[2] - bbox[0] + 20
        h = bbox[3] - bbox[1] + 20
        
        img = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw stroke/shadow
        stroke_width = 4
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                draw.text((10+dx, 10+dy), word.upper(), font=font, fill=(0, 0, 0, 255))
        
        # Draw main text
        draw.text((10, 10), word.upper(), font=font, fill=(255, 255, 0, 255)) # Yellow
        
        temp_path = os.path.join(self.output_folder, f"temp_word_{random.randint(0, 100000)}.png")
        img.save(temp_path)
        return temp_path

    def upload_to_socials(self, video_path, caption):
        """Placeholder for TikTok/Instagram Graph API upload."""
        logging.info(f"Uploading {video_path} to social media with caption: {caption}")
        return True

    def generate_video(self, audio_path, subtitles, reddit_header_path, output_filename):
        logging.info(f"Assembling video: {output_filename}")
        
        # 1. Load Audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # 2. Select and Load Background
        bg_video_path = self.select_random_background()
        if not bg_video_path:
            logging.warning("Creating dummy background as no videos were found.")
            bg_clip = ColorClip(size=(1080, 1920), col=(50, 50, 50)).set_duration(duration)
        else:
            bg_clip = VideoFileClip(bg_video_path)
            if bg_clip.duration < duration:
                n_loops = int(duration / bg_clip.duration) + 1
                clips_to_loop = [bg_clip] * n_loops
                bg_clip = concatenate_videoclips(clips_to_loop).set_duration(duration)
            else:
                start_time = random.uniform(0, bg_clip.duration - duration)
                bg_clip = bg_clip.subclip(start_time, start_time + duration)
            
            # Crop and Resize to 1080x1920
            w, h = bg_clip.size
            target_ratio = 9/16
            if w/h > target_ratio:
                new_w = h * target_ratio
                bg_clip = bg_clip.crop(x_center=w/2, width=new_w)
            else:
                new_h = w / target_ratio
                bg_clip = bg_clip.crop(y_center=h/2, height=new_h)
            
            bg_clip = bg_clip.resize(width=1080, height=1920)

        # 3. Add Reddit Header (show for 5 seconds)
        header_clip = ImageClip(reddit_header_path).set_duration(min(5, duration)).set_position(("center", 200)).resize(width=900)
        
        # 4. Create Captions using Pillow-generated images
        caption_clips = []
        temp_files = []
        for sub in subtitles:
            word = sub['word'].strip()
            if not word: continue
            
            start = sub['start']
            word_img_path = self.create_caption_image(word)
            temp_files.append(word_img_path)
            
            txt_clip = ImageClip(word_img_path).set_start(start).set_duration(sub['duration']).set_position('center')
            caption_clips.append(txt_clip)

        # 5. Composite
        final_video = CompositeVideoClip([bg_clip, header_clip] + caption_clips)
        final_video = final_video.set_audio(audio)
        
        output_path = os.path.join(self.output_folder, output_filename)
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        
        # Cleanup temp files
        for f in temp_files:
            try: os.remove(f)
            except: pass
            
        return output_path

import logging
import os

try:
    from instagrapi import Client
except ImportError:
    Client = None

class Uploader:
    def __init__(self, config):
        self.config = config
        self.instagram_config = config.get('upload', {}).get('instagram', {})
        self.tiktok_config = config.get('upload', {}).get('tiktok', {})
        self.youtube_config = config.get('upload', {}).get('youtube', {})

    def upload_to_instagram(self, video_path, caption):
        """Uploads a video to Instagram Reels."""
        if not Client:
            logging.error("instagrapi library not installed. Instagram upload skipped.")
            return False
            
        if not self.instagram_config.get('enabled', False):
            logging.info("Instagram upload is disabled in config.")
            return False

        username = self.instagram_config.get('username')
        password = self.instagram_config.get('password')
        
        if not username or not password:
            logging.error("Instagram credentials missing.")
            return False

        try:
            cl = Client()
            cl.login(username, password)
            logging.info(f"Uploading {video_path} to Instagram Reels...")
            media = cl.clip_upload(video_path, caption)
            logging.info(f"Instagram upload successful. Media ID: {media.pk}")
            return True
        except Exception as e:
            logging.error(f"Instagram upload failed: {e}")
            return False

    def upload_to_tiktok(self, video_path, caption):
        """Placeholder for TikTok upload."""
        if not self.tiktok_config.get('enabled', False):
            logging.info("TikTok upload is disabled in config.")
            return False
            
        logging.info(f"TikTok upload (PLACEHOLDER) for {video_path} with caption: {caption}")
        # Logic for tiktok-uploader or official API would go here
        return True

    def upload_to_youtube(self, video_path, caption):
        """Placeholder for YouTube Shorts upload."""
        if not self.youtube_config.get('enabled', False):
            logging.info("YouTube upload is disabled in config.")
            return False
            
        logging.info(f"YouTube Shorts upload (PLACEHOLDER) for {video_path} with caption: {caption}")
        # Logic for Google API client would go here
        return True

    def upload_all(self, video_path, caption):
        """Attempts to upload to all enabled platforms."""
        results = {}
        results['instagram'] = self.upload_to_instagram(video_path, caption)
        results['tiktok'] = self.upload_to_tiktok(video_path, caption)
        results['youtube'] = self.upload_to_youtube(video_path, caption)
        return results

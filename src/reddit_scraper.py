import praw
import re
import logging

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_top_post(self, subreddit_name, time_filter="day"):
        logging.info(f"Fetching top post from r/{subreddit_name} (filter: {time_filter})...")
        subreddit = self.reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(time_filter=time_filter, limit=1)
        
        for post in top_posts:
            return {
                "title": post.title,
                "body": post.selftext,
                "id": post.id,
                "url": post.url
            }
        return None

    def clean_text(self, text):
        # Remove "EDIT:" and everything after it (optional, but often good for stories)
        text = re.sub(r'EDIT:.*', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        
        # Remove excessive emojis (keeping some might be okay, but for TTS we want clean text)
        # This is a simple regex for non-ascii, might need refinement
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def get_story(self, subreddit_name):
        post = self.fetch_top_post(subreddit_name)
        if not post:
            logging.error(f"No posts found in r/{subreddit_name}")
            return None
        
        cleaned_title = self.clean_text(post['title'])
        cleaned_body = self.clean_text(post['body'])
        
        return {
            "title": cleaned_title,
            "body": cleaned_body,
            "original_id": post['id']
        }

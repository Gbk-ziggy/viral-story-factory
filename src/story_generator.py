import logging
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class StoryGenerator:
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        if api_key and OpenAI:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            if not OpenAI:
                logging.warning("OpenAI library not installed. AI Story Generation will be unavailable.")

    def generate_story(self, topic="a dramatic life event", subreddit="AmItheAsshole"):
        """Generates a Reddit-style story using LLM."""
        if not self.client:
            logging.error("AI Story Generator: No API key or library missing. Returning mock story.")
            return self._get_mock_story(subreddit)

        prompt = f"Write a compelling, realistic, and dramatic first-person story in the style of a top post on the r/{subreddit} subreddit. The topic is: {topic}. Include a title and the body text. Do not include 'TL;DR' or 'Edit' tags."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative writer who specializes in viral Reddit storytelling."},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content
            
            # Simple parsing: assume first line is title if it starts with 'Title:' or just use the first paragraph
            lines = content.split('\n')
            title = lines[0].replace("Title: ", "").strip()
            body = "\n".join(lines[1:]).strip()
            
            return {
                "title": title,
                "body": body,
                "original_id": "ai_generated_" + str(hash(content))[:8]
            }
        except Exception as e:
            logging.error(f"Error generating AI story: {e}")
            return self._get_mock_story(subreddit)

    def _get_mock_story(self, subreddit):
        """Returns a hardcoded story for testing if AI is unavailable."""
        return {
            "title": f"AITAH for implementing an AI story generator?",
            "body": "I (24M) am an automation engineer. My boss asked me to build a system that generates viral videos. I decided to use AI to write the stories. My coworkers say it's 'cheating' and that the stories lack 'human soul'. I think they are just jealous of my efficiency. AITAH?",
            "original_id": "mock_ai_story"
        }

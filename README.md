# Viral Story Factory 🚀

An automated "Reddit-to-Vertical-Video" pipeline that transforms trending Reddit stories (or AI-generated scripts) into engaging vertical videos for TikTok, Instagram Reels, and YouTube Shorts.

## Features
- **Smart Sourcing**: Scrape top posts from Reddit (PRAW) or generate fictional stories (OpenAI).
- **High-Quality TTS**: Integrated with `edge-tts` for natural voiceovers with word-level timing.
- **Dynamic Visuals**: 
  - Native-looking Reddit header overlays.
  - Word-by-word dynamic captions (yellow text with black stroke).
  - 9:16 vertical cropping and background looping.
- **Auto-Posting**: Built-in support for Instagram Reels and placeholders for TikTok/YouTube Shorts.
- **Plug-and-Play**: Automatically downloads sample background footage if none is provided.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure `config.json` with your API keys (Reddit, OpenAI, etc.).
4. Run: `python main.py`.

## Architecture
- `src/reddit_scraper.py`: Reddit API integration.
- `src/story_generator.py`: LLM story generation.
- `src/tts_engine.py`: TTS and subtitle timing.
- `src/video_generator.py`: Video assembly and captioning.
- `src/uploader.py`: Social media publishing.

Made with ❤️ by team redditmaker.

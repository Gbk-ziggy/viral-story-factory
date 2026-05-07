# Viral Story Factory 🚀

An automated pipeline to convert trending Reddit stories (or AI-generated ones) into engaging vertical videos (9:16) for TikTok, Instagram Reels, and YouTube Shorts.

## Features ✨

- **Reddit Scraping**: Automatically fetches top posts from specific subreddits (e.g., r/AmItheAsshole).
- **AI Story Generation**: Optionally uses OpenAI to generate fictional, Reddit-style stories.
- **High-Quality TTS**: Integrated with `edge-tts` for natural-sounding voiceovers.
- **Dynamic Captions**: Word-by-word animated captions synced with the audio.
- **Auto-Formatting**: Background videos are automatically cropped and resized to 1080x1920.
- **Native reddit Header**: Generates a clean, native-looking Reddit post header overlay.
- **Multi-Platform Posting**: Supports automated uploading to Instagram Reels (via `instagrapi`) and provides placeholders for TikTok and YouTube.
- **Robustness**: Automatically downloads sample background footage if none is provided.

## Project Structure 📁

```
viral-story-factory/
├── assets/
│   ├── backgrounds/    # Place your "satisfying" videos here
│   └── fonts/          # Custom fonts (e.g., Impact, FreeSans)
├── src/
│   ├── reddit_scraper.py
│   ├── tts_engine.py
│   ├── video_generator.py
│   ├── story_generator.py
│   ├── uploader.py
│   └── utils.py
├── output/             # Generated videos and metadata
├── main.py             # Main entry point
├── config.json         # API keys and settings
└── requirements.txt
```

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd viral-story-factory
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the pipeline**:
   Edit `config.json` with your API credentials (Reddit, OpenAI, Instagram) and preferred settings.

## Usage 🚀

Run the pipeline end-to-end:
```bash
python main.py
```

Check `process.log` for logs and the `output/` folder for your finished videos!

## Dependencies 📦

- `praw` (Reddit API)
- `edge-tts` (Text-to-Speech)
- `moviepy` (Video Processing)
- `Pillow` (Image/Overlay Generation)
- `instagrapi` (Instagram Automation)
- `openai` (AI Story Generation)
- `mutagen` (Audio Metadata)

## License 📄
MIT

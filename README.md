# Viral Story Factory 🚀

An automated pipeline to convert trending Reddit stories (or AI-generated ones) into engaging vertical videos (9:16) for TikTok, Instagram Reels, and YouTube Shorts.

## Features ✨

- **Reddit Scraping**: Automatically fetches top posts from specific subreddits (e.g., r/AmItheAsshole).
- **AI Story Generation**: Optionally uses OpenAI to generate fictional, Reddit-style stories.
- **High-Quality TTS**: Integrated with `edge-tts` for natural-sounding voiceovers.
- **Dynamic Captions**: Word-by-word animated captions synced with the audio.
- **Auto-Formatting**: Background videos are automatically cropped and resized to 1080x1920.
- **Native Reddit Header**: Generates a clean, native-looking Reddit post header overlay.
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

## Prerequisites 📋

- **Python 3.8+**
- **FFmpeg**: Must be installed and accessible in your system PATH for video processing.

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Gbk-ziggy/viral-story-factory.git
   cd viral-story-factory
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration ⚙️

Edit the `config.json` file with your details:

### 1. Reddit API (praw)
Get your keys at [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps). Create a "script" type app.
- `client_id`
- `client_secret`
- `user_agent`: A unique string identifying your script.

### 2. OpenAI API (Optional)
If you want to use the AI Story Generator, get your key at [https://platform.openai.com/](https://platform.openai.com/).
- `enabled`: Set to `true`.
- `api_key`: Your OpenAI API key.

### 3. Instagram (Optional)
- `enabled`: Set to `true` under the `upload` section.
- `username` & `password`: Your account credentials.

## Usage 🚀

Run the pipeline end-to-end:
```bash
python main.py
```

The script will:
1. Fetch a story from the configured subreddit OR generate one using AI.
2. Generate a voiceover.
3. Select a random background video from `assets/backgrounds/`.
4. Render the video with a Reddit header and dynamic captions.
5. Save the final video to the `output/` folder.
6. Upload to Instagram (if enabled).

Check `process.log` for logs and detailed progress!

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

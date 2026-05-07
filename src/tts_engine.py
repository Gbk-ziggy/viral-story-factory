import asyncio
import edge_tts
import logging
import os
from mutagen.mp3 import MP3

class TTSEngine:
    def __init__(self, voice="en-US-ChristopherNeural"):
        self.voice = voice

    async def generate_audio(self, text, output_path):
        logging.info(f"Generating audio for text (length: {len(text)})...")
        communicate = edge_tts.Communicate(text, self.voice)
        
        subtitles = []
        
        # We use a custom stream to capture word boundaries
        # edge-tts Communicate.save() doesn't give us boundaries directly easily
        # but we can use communicate.stream()
        
        with open(output_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    subtitles.append({
                        "word": text[chunk["offset"]:chunk["offset"] + chunk["text_length"]],
                        "start": chunk["offset_t"] / 10000000, # convert to seconds
                        "duration": chunk["duration_t"] / 10000000
                    })
        
        duration = self.get_duration(output_path)
        logging.info(f"Audio generated: {output_path} (Duration: {duration:.2f}s)")
        return duration, subtitles

    def get_duration(self, file_path):
        audio = MP3(file_path)
        return audio.info.length

    def run_tts(self, text, output_path):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return loop.run_until_complete(self.generate_audio(text, output_path))
        else:
            return asyncio.run(self.generate_audio(text, output_path))

# Note: mutagen is needed for duration calculation if we don't want to use FFmpeg directly

# youtube_summary_full.py

import os
from dotenv import load_dotenv
from euriai import EuriaiClient
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

load_dotenv()

api_key = os.getenv("EURI_API_KEY")
client = EuriaiClient(api_key=api_key, model="gpt-4.1-nano")


def extract_video_id(youtube_url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", youtube_url)
    if not match:
        raise ValueError("❌ Invalid YouTube URL format.")
    return match.group(1)


def summarize_youtube_video_full(url: str) -> dict:
    try:
        print(f"🔍 Processing YouTube URL: {url}")
        video_id = extract_video_id(url)
        print(f"📹 Extracted Video ID: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if not transcript or not isinstance(transcript, list):
            raise ValueError("❌ No transcript found or transcript is not in expected format.")
        print(f"📝 Formatting transcript: {transcript}")
        print(f"📜 Transcript retrieved for video ID: {video_id}")
        formatter = TextFormatter()
        raw_text = formatter.format_transcript(transcript)
        print(f"📝 Transcript formatted for video ID: {video_id}")
        clipped_text = raw_text[:6000]

        summary_prompt = f"""
You are an AI content expert. Watch this YouTube video transcript and generate the following:
1. Timestamped and formatted summary of the video (with key sections and timestamps).
2. 5 SEO-friendly YouTube title suggestions (separated by new lines).
3. Comma-separated video tags for SEO.
4. A short thumbnail title for this video.

Transcript:
{clipped_text}

"""
        print(f"📝 Summary prompt prepared for video ID: {video_id}")
        response = client.generate_completion(
            prompt=summary_prompt,
            temperature=0.6,
            max_tokens=3000
        )
        print(f"✅ Summary generated for video ID: {video_id}")

        return {
            "video_id": video_id,
            "video_url": url,
            "response": response
        }

    except Exception as e:
        return {"error": str(e), "video_url": url}

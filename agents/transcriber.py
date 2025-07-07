import os
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from openai import OpenAI

client = OpenAI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def transcribe_youtube(url: str) -> str:
    video_id = url.split("v=")[-1].split("&")[0]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([seg["text"] for seg in transcript])
        return text
    except (TranscriptsDisabled, NoTranscriptFound):
        return None

def download_audio(url: str) -> str:
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    path = audio_stream.download(output_path=UPLOAD_DIR)
    return path

def transcribe_file(filepath: str) -> str:
    with open(filepath, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

import os

# Set required binary paths
os.environ["IMAGEMAGICK_BINARY"] = "/opt/homebrew/bin/magick"
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"

import requests
from moviepy.editor import (
    concatenate_videoclips,
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)

# Constants
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"
PEXELS_BASE_URL = "https://api.pexels.com/videos/search"
VOICEOVER_FILE = "voiceover.mp3"
OUTPUT_VIDEO = "shadow_reel.mp4"
SCRIPT_TEXT_FILE = "voiceover.txt"
CLIP_FOLDER = "clips"

# Upload Audio
def upload_custom_audio(file_path):
    if os.path.exists(file_path):
        os.rename(file_path, VOICEOVER_FILE)
        print(f"[INFO] Custom audio uploaded: {file_path}")
    else:
        print("[ERROR] Provided audio file does not exist.")

# Generate Voiceover Placeholder
def generate_voiceover(script_text):
    with open(SCRIPT_TEXT_FILE, "w") as f:
        f.write(script_text)
    print("[INFO] Placeholder: Insert TTS system to generate voiceover.mp3 from script_text")

# Fetch B-roll video clips from Pexels
def fetch_video_clips(keyword, limit=3):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": limit}
    response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    results = response.json()

    urls = [video['video_files'][0]['link'] for video in results.get('videos', [])]
    os.makedirs(CLIP_FOLDER, exist_ok=True)

    for idx, url in enumerate(urls):
        filename = f"{CLIP_FOLDER}/clip_{idx}.mp4"
        clip_response = requests.get(url)
        if clip_response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(clip_response.content)
            print(f"[INFO] Downloaded: {filename}")
        else:
            print(f"[WARNING] Skipped invalid clip from: {url}")

# Create the Shadow Reel video
def create_shadow_reel(script_text):
    script_lines = script_text.splitlines()
    clips = []

    audio = AudioFileClip(VOICEOVER_FILE)
    audio_duration = audio.duration
    per_line_duration = audio_duration / max(1, len(script_lines))

    caption_clips = []
    for i, line in enumerate(script_lines):
        txt = TextClip(
            line.strip(),
            fontsize=42,
            color='white',
            font='Arial-Bold'
        )
        txt = txt.set_position('center').set_duration(per_line_duration).set_start(i * per_line_duration)
        caption_clips.append(txt)

    # Load video clips from 'clips/' folder
    video_files = [f"{CLIP_FOLDER}/clip_{i}.mp4" for i in range(len(script_lines))]
    video_clips = []

    for f in video_files:
        try:
            clip = VideoFileClip(f)
            subclip = clip.subclip(0, min(per_line_duration, clip.duration))
            video_clips.append(subclip)
        except Exception as e:
            print(f"[ERROR] Failed to load video clip {f}: {e}")

    # Loop clips if fewer than lines
    while len(video_clips) < len(script_lines):
        video_clips += video_clips[:len(script_lines) - len(video_clips)]
    video_clips = video_clips[:len(script_lines)]

    # Composite text + video
    composited = [
        CompositeVideoClip([v.set_duration(per_line_duration), c])
        for v, c in zip(video_clips, caption_clips)
    ]

    final_video = concatenate_videoclips(composited, method="compose").set_audio(audio)
    final_video = final_video.set_duration(final_video.duration + 1.5)
    final_video.write_videofile(OUTPUT_VIDEO, codec="libx264", audio_codec="aac")

    print(f"[INFO] Final video saved as {OUTPUT_VIDEO}")

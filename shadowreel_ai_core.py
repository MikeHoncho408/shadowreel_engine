import os
os.environ["IMAGEMAGICK_BINARY"] = "/opt/homebrew/bin/magick"
import requests
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"
PEXELS_BASE_URL = "https://api.pexels.com/videos/search"
VOICEOVER_FILE = "voiceover.mp3"
OUTPUT_VIDEO = "shadow_reel.mp4"
SCRIPT_TEXT_FILE = "voiceover.txt"

def upload_custom_audio(file_path):
    if os.path.exists(file_path):
        os.rename(file_path, VOICEOVER_FILE)
        print(f"[INFO] Custom audio uploaded: {file_path}")
    else:
        print("[ERROR] Provided audio file does not exist.")

def generate_voiceover(script_text):
    with open(SCRIPT_TEXT_FILE, "w") as f:
        f.write(script_text)
    print("[INFO] Placeholder: Insert TTS system to generate voiceover.mp3 from script_text")

def fetch_video_clips(keyword, limit=3):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": limit}
    response = requests.get(PEXELS_BASE_URL, headers=headers, params=params)
    results = response.json()
    urls = [video['video_files'][0]['link'] for video in results.get('videos', [])]
    os.makedirs("clips", exist_ok=True)
    for idx, url in enumerate(urls):
        filename = f"clips/clip_{idx}.mp4"
        clip_response = requests.get(url)
        if clip_response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(clip_response.content)
            print(f"[INFO] Downloaded: {filename}")
        else:
            print(f"[WARNING] Skipped invalid clip from: {url}")

from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

def create_shadow_reel(script_text):
    script_lines = script_text.splitlines()
    ...
    clips = []

    # Get the duration of the voiceover
    audio = AudioFileClip("voiceover.mp3")
    audio_duration = audio.duration

    # Calculate duration per caption (split evenly)
    per_line_duration = audio_duration / max(1, len(script_lines))

    # Build text caption clips
    caption_clips = []
    for i, line in enumerate(script_lines):
        txt = TextClip(line.strip(), fontsize=42, color='white', font='Arial-Bold')
        txt = txt.set_position('center').set_duration(per_line_duration).set_start(i * per_line_duration)
        caption_clips.append(txt)

    # Load your video clips
    video_files = ["clip1.mp4", "clip2.mp4", "clip3.mp4"]  # Replace with real paths
    video_clips = [
        VideoFileClip(f).subclip(0, min(per_line_duration, VideoFileClip(f).duration))
        for f in video_files
    ]

    # Match video clips to the caption count
    while len(video_clips) < len(script_lines):
        video_clips += video_clips[:len(script_lines) - len(video_clips)]
    video_clips = video_clips[:len(script_lines)]

    # Stack video + captions
    composited = [
        CompositeVideoClip([v.set_duration(per_line_duration), c])
        for v, c in zip(video_clips, caption_clips)
    ]

    # Concatenate scenes and add audio
    final_video = concatenate_videoclips(composited, method="compose").set_audio(audio)

    # Add a small buffer to ensure last line finishes
    final_duration = final_video.duration
    final_video = final_video.set_duration(final_duration + 1.5)

    # Export final video
    final_video.write_videofile("shadow_reel.mp4", codec="libx264", audio_codec="aac")
    print("[INFO] Final video saved as shadow_reel.mp4")

import os
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

def create_shadow_reel():
    video_files = [f"clips/{file}" for file in os.listdir("clips") if file.endswith(".mp4")]

    clips = []
    for file in video_files:
        try:
            clip = VideoFileClip(file).subclip(0, 5)
            clips.append(clip)
        except Exception as e:
            print(f"[ERROR] Skipping file {file}: {e}")

    if not clips:
        print("[ERROR] No valid video clips available to create a reel.")
        return

    final_video = concatenate_videoclips(clips, method="compose")

    if os.path.exists(VOICEOVER_FILE):
        audio = AudioFileClip(VOICEOVER_FILE)
        final_video = final_video.set_audio(audio)

    if os.path.exists(SCRIPT_TEXT_FILE):
        with open(SCRIPT_TEXT_FILE, "r") as f:
            script_lines = f.readlines()

        caption_clips = []
        total_duration = final_video.duration / max(1, len(script_lines))

        for i, line in enumerate(script_lines):
            txt_clip = TextClip(line.strip(), fontsize=40, color='white', font='Arial-Bold')
            txt_clip = txt_clip.set_position('center').set_duration(total_duration).set_start(i * total_duration)
            caption_clips.append(txt_clip)

        final_video = CompositeVideoClip([final_video, *caption_clips])

    final_video.write_videofile(OUTPUT_VIDEO, fps=24)
    print(f"[INFO] Final video saved as {OUTPUT_VIDEO}")

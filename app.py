import streamlit as st
from shadowreel_ai_core import generate_voiceover, fetch_video_clips, create_shadow_reel, upload_custom_audio

st.set_page_config(layout="centered", page_title="ShadowForge AI", page_icon="🎬")

st.title("🎬 ShadowForge AI")
st.markdown(
    """
    Welcome to **ShadowForge AI**, your cinematic storytelling machine.  
    Drop your script. Pick your vibe. Get your revolution on tape.
    """
)



script_text = st.text_area("✍️ Enter your video script below:", height=200)
keyword = st.text_input("🔍 B-Roll Search Keyword:", value="surveillance")
script_text = st.text_area("✍️ Enter your video script below:", height=200)
keyword = st.text_input("🔍 B-Roll Search Keyword:", value="surveillance")

from pydub import AudioSegment  # Make sure this is already at the top of the file

uploaded_audio_files = st.file_uploader(
    "🎤 Upload one or more .mp3 voiceover files", 
    type=["mp3"], 
    accept_multiple_files=True
)

merged_audio_path = "voiceover_merged.mp3"

if st.button("🚀 Generate Cinematic Reel"):
    ...
            for idx, audio_file in enumerate(uploaded_audio_files):
                filename = f"temp_audio_{idx}.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_file.read())
                segment = AudioSegment.from_mp3(filename)
                merged_audio += segment

            merged_audio.export("voiceover.mp3", format="mp3")
            upload_custom_audio("voiceover.mp3")
        else:
            generate_voiceover(script_text)

        fetch_video_clips(keyword)
        create_shadow_reel()
        st.success("✅ Your video is ready!")
        st.video("shadow_reel.mp4")

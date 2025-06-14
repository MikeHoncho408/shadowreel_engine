import streamlit as st
from shadowreel_ai_core import generate_voiceover, fetch_video_clips, create_shadow_reel, upload_custom_audio
import os

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
uploaded_audio = st.file_uploader("🎤 Upload a .mp3 voiceover file", type=["mp3"])

if st.button("🚀 Generate Cinematic Reel"):
    if not script_text.strip():
        st.warning("Please enter a script first.")
    elif not uploaded_audio:
        st.warning("Please upload a voiceover .mp3 file.")
    else:
        # Save uploaded audio
        voiceover_path = "voiceover.mp3"
        with open(voiceover_path, "wb") as f:
            f.write(uploaded_audio.read())
        st.info("⚙️ Audio uploaded. Creating video...")

        upload_custom_audio(voiceover_path)

        fetch_video_clips(keyword)

        def create_shadow_reel(script_text):
            script_lines = script_text.splitlines()
            clips = []

        st.success("✅ Your video is ready!")
        st.video("shadow_reel.mp4")
        st.markdown("[Download Video](shadow_reel.mp4)", unsafe_allow_html=True)

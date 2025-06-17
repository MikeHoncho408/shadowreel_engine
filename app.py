import streamlit as st
import os
from shadowreel_ai_core import generate_voiceover, fetch_video_clips, create_shadow_reel, upload_custom_audio

st.set_page_config(layout="centered", page_title="ShadowForge AI", page_icon="🎬")
st.title("🎬 ShadowForge AI: Storytelling Engine")
st.markdown("Upload a custom voiceover or enter a script to auto-generate one.")

# --- B-Roll Search Keyword ---
keyword = st.text_input("🔍 B-Roll Search Keyword:")

# --- Upload Audio File ---
uploaded_audio = st.file_uploader("🎤 Upload a .mp3 voiceover file", type="mp3")

# --- Script Text Input ---
script_text = st.text_area("📝 Enter your script here (if not uploading audio):")

# --- Trigger Button ---
if st.button("⚙️ Generate ShadowReel"):
    try:
        if uploaded_audio is not None:
            # Save and use uploaded audio file
            with open("voiceover.mp3", "wb") as f:
                f.write(uploaded_audio.read())
            st.info("✅ Custom audio uploaded. Creating video...")

            # Also create a placeholder script file for subtitle purposes
            with open("voiceover.txt", "w") as f:
                f.write(script_text)

        elif script_text.strip():
            st.info("⚙️ Generating voiceover and video...")
            generate_voiceover(script_text)

            with open("voiceover.txt", "w") as f:
                f.write(script_text)

        else:
            raise ValueError("Script text is required.")

        # Always fetch clips & generate video using script
        fetch_video_clips(keyword)
        create_shadow_reel()

        # Show video if available
        if os.path.exists("shadow_reel.mp4"):
            st.success("✅ Your video is ready!")
            st.video("shadow_reel.mp4")
            st.markdown("[Download Video](shadow_reel.mp4)", unsafe_allow_html=True)
        else:
            st.error("⚠️ Video generation failed. Please check logs.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

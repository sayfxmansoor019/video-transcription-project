

import streamlit as st


st.set_page_config(
    page_title="Video Intelligence Dashboard",
    layout="wide"
)

from pathlib import Path
from moviepy.editor import VideoFileClip
from scripts.reaction_annotations import annotate_reactions
import json


with st.spinner("Loading models..."):
    from scripts.transcribe_video import transcribe_video
    from scripts.annotate_emotions import analyze_emotions
    from scripts.delivery_nuances import analyze_delivery
    from scripts.summarize_with_llm import summarize_text


Path("outputs").mkdir(exist_ok=True)

st.title("🎥 Video Intelligence Dashboard")
st.caption("Timestamped Transcription → Emotion, Delivery & Reactions → Summary")


uploaded_file = st.file_uploader(
    "Upload a video call recording",
    type=["mp4", "mov", "avi"]
)

if uploaded_file:
    video_path = Path("outputs") / uploaded_file.name
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video(str(video_path))
    st.success("Video uploaded successfully!")

    
    st.info("🔄 Extracting audio from video...")
    video = VideoFileClip(str(video_path))
    audio_path = video_path.with_suffix(".wav")
    video.audio.write_audiofile(str(audio_path), verbose=False, logger=None)
    st.success("Audio extraction completed")

    
    st.info("🔄 Transcribing audio with timestamps...")
    try:
        transcript_segments = transcribe_video(str(audio_path))
        st.subheader("📄 Timestamped Transcript")

        full_text = []
        for seg in transcript_segments:
            st.write(f"[{seg['start']} - {seg['end']}] {seg['text']}")
            full_text.append(seg["text"])

        full_transcript_text = " ".join(full_text)

    except Exception as e:
        st.error(f"Transcription failed: {e}")
        transcript_segments = []
        full_transcript_text = ""

    
    st.info("🎧 Analyzing emotions...")
    try:
        emotions = []
        st.subheader("😊 Emotion Annotations")

        for seg in transcript_segments:
            emotion_scores = analyze_emotions(seg["text"])
            emotion = max(emotion_scores, key=emotion_scores.get)
            emotions.append(emotion)
            st.write(
                f"[{seg['start']} - {seg['end']}] {seg['text']} → Emotion: {emotion}"
            )

    except Exception as e:
        st.error(f"Emotion analysis failed: {e}")
        emotions = []

    
    st.info("🎙️ Analyzing delivery nuances...")
    try:
        delivery = analyze_delivery(str(audio_path), full_transcript_text)
        st.subheader("🎵 Delivery Nuances")

        for k, v in delivery.items():
            st.write(f"{k.replace('_', ' ').title()} → {v}")

    except Exception as e:
        st.error(f"Delivery analysis failed: {e}")
        delivery = {}

    
    st.info("🤔 Annotating reactions...")
    try:
        reactions = annotate_reactions(transcript_segments)
        st.subheader("💬 Reactions")

        for seg, react in zip(transcript_segments, reactions):
            st.write(
                f"[{seg['start']} - {seg['end']}] {seg['text']} → Reaction: {react}"
            )

    except Exception as e:
        st.error(f"Reaction annotation failed: {e}")
        reactions = []

    
    st.info("🧠 Generating summary...")
    try:
        summary = summarize_text(full_transcript_text)
        st.subheader("📝 Summary")
        st.text_area("Summary", summary, height=150)

    except Exception as e:
        st.error(f"Summarization failed: {e}")
        summary = ""

    
    output = {
        "transcript": transcript_segments,
        "emotions": emotions,
        "delivery_nuances": delivery,
        "reactions": reactions,
        "summary": summary
    }

    with open("outputs/final_output.json", "w") as f:
        json.dump(output, f, indent=4)

    st.success("✅ Final enriched transcript saved")

else:
    st.info("Upload a video file to begin analysis.")

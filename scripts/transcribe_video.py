

import whisper


model = whisper.load_model("base")  

def transcribe_video(audio_path: str):
    """
    Transcribe audio to timestamped text using Whisper.
    Returns: List of dicts [{start, end, text}]
    """
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=False  
    )

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip()
        })

    return segments

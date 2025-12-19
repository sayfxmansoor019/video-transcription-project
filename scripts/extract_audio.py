import subprocess

video_path = "data/sample_call.mp4"
audio_path = "audio/extracted_audio.wav"

command = [
    "ffmpeg",
    "-i", video_path,
    "-ar", "16000",
    "-ac", "1",
    audio_path
]

subprocess.run(command)
print("✅ Audio extracted successfully")


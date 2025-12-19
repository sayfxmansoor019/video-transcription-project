

from transformers import pipeline


emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def analyze_emotions(audio_path_or_text):
    """
    Emotion analysis based on transcript text.
    Returns a dict of emotion probabilities.
    """

    
    if not isinstance(audio_path_or_text, str):
        return {}

    text = audio_path_or_text.strip()
    if len(text) < 5:
        return {}

    results = emotion_classifier(text[:512])[0]

    emotions = {
        r["label"].lower(): round(r["score"], 3)
        for r in results
    }

    return emotions

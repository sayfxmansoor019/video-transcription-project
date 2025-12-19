

def annotate_reactions(transcript_segments: list) -> list:
    """
    Annotate reactions to specific statements.
    Returns list of reactions, aligned with transcript segments.
    """
    reactions = []
    for seg in transcript_segments:
        text = seg["text"].lower()
        if any(word in text for word in ["wow", "amazing", "great"]):
            reactions.append("Positive")
        elif any(word in text for word in ["uh", "hmm", "wait"]):
            reactions.append("Thinking")
        elif any(word in text for word in ["sorry", "unfortunately"]):
            reactions.append("Negative")
        else:
            reactions.append("Neutral")
    return reactions

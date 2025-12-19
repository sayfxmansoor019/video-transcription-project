

def summarize_text(text: str) -> str:
    """
    Generate a short summary of the text.
    Placeholder using first few sentences.
    """
    sentences = text.split(". ")
    summary = ". ".join(sentences[:2])  
    return summary

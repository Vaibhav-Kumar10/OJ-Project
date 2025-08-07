from difflib import SequenceMatcher


def is_similar(code1, code2, threshold=0.9):
    return SequenceMatcher(None, code1, code2).ratio() > threshold

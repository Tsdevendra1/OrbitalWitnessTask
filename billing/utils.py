def is_word(text: str) -> bool:
    """
    Assumptions: position of ' and - in a word is not important. Also, unicode letters are considered as normal characters.
    """
    if not text or not isinstance(text, str):
        return False

    if any(char.isspace() for char in text):
        return False

    for char in text:
        if char.isalpha() or char in "'-":
            continue

        return False

    return True


def get_valid_words(text: str) -> list[str]:
    return [word for word in text.split() if is_word(word)]

def to_notion_language(pygments_language: str) -> str:
    if pygments_language == "default":
        # default means "not specified"
        return "plain text"
    if pygments_language == "text":
        return "plain text"
    if pygments_language == "pytb":
        return "plain text"
    if pygments_language == "output":
        return "plain text"
    if pygments_language == "pycon":
        return "python"
    # TODO: Support for other languages
    return pygments_language

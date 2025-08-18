def to_notion_language(pygments_language: str) -> str:
    if pygments_language == "default":
        # default means "not specified"
        return "plain text"
    if pygments_language == "text":
        return "plain text"
    return pygments_language

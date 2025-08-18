PygmentsLanguage = str

_as_python: set[PygmentsLanguage] = {"python", "pycon"}
# default means "not specified"
_as_plain_text: set[PygmentsLanguage] = {"default", "pytb", "text", "output"}


def to_notion_language(pygments_language: PygmentsLanguage) -> str:
    if pygments_language in _as_plain_text:
        return "plain text"
    if pygments_language in _as_python:
        return "python"
    # TODO: Support for other languages
    return pygments_language

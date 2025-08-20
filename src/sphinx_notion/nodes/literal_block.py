from pygments.lexers import get_lexer_by_name

PygmentsLanguage = str


def get_standard_pygments_language(language: str) -> PygmentsLanguage:
    lexer = get_lexer_by_name(language)
    # Lexer has aliases but mypy raises this error:
    # >error: "Lexer" has no attribute "aliases"  [attr-defined]
    # https://github.com/pygments/pygments/blob/2.19.2/pygments/lexer.py#L111-L113
    return lexer.aliases[0]  # type: ignore[attr-defined]


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

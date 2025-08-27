from pygments.lexers import get_lexer_by_name

PygmentsLanguage = str


def get_standard_pygments_language(language: str) -> PygmentsLanguage:
    # "default" language means "not specified"
    if language == "default":
        return "default"
    lexer = get_lexer_by_name(language)
    # Lexer has aliases but mypy raises this error:
    # >error: "Lexer" has no attribute "aliases"  [attr-defined]
    # https://github.com/pygments/pygments/blob/2.19.2/pygments/lexer.py#L111-L113
    return lexer.aliases[0]  # type: ignore[attr-defined]


def to_notion_language(pygments_language: PygmentsLanguage) -> str:
    if pygments_language in {"default", "pytb", "text", "output"}:
        return "plain text"
    if pygments_language in {"python", "pycon"}:
        return "python"
    # TODO: Support for other languages
    return pygments_language


def chunk_code(code: str, upper_limit: int):
    lines = code.splitlines(keepends=True)
    max_line_length = max(len(line) for line in lines)
    if max_line_length > upper_limit:
        raise ValueError(
            f"upper_limit (current {upper_limit}) needs to be greater "
            f"than max_line_length ({max_line_length})"
        )

    buffer = ""
    for line in lines:
        if len(buffer) + len(line) <= upper_limit:
            buffer += line
        else:
            yield buffer
            buffer = line
    if buffer:
        yield buffer

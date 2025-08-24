import pytest

from sphinx_notion.nodes.literal_block import (
    chunk_code,
    get_standard_pygments_language,
    to_notion_language,
)


@pytest.mark.parametrize(
    "language, expected",
    [
        ("python", "python"),
        ("python3", "python"),
        ("pycon", "pycon"),
        ("python-console", "pycon"),
        ("pytb", "pytb"),
        ("py3tb", "pytb"),
        ("text", "text"),
        ("output", "output"),
        ("default", "default"),
    ],
)
def test_get_standard_pygments_language(language, expected):
    assert get_standard_pygments_language(language) == expected


@pytest.mark.parametrize(
    "pygments_language, expected",
    [
        ("python", "python"),
        ("default", "plain text"),
        ("pycon", "python"),
        ("pytb", "plain text"),
        ("text", "plain text"),
        ("output", "plain text"),
    ],
)
def test_to_notion_language(pygments_language, expected):
    assert to_notion_language(pygments_language) == expected


def test_chunk_code():
    code = """1 + 2
3 - 4
5 * 6
7 / 8
"""
    actual = chunk_code(code, 6)
    expected = [
        "1 + 2\n",
        "3 - 4\n",
        "5 * 6\n",
        "7 / 8\n",
    ]
    assert list(actual) == expected


def test_chunk_code_multiple_lines():
    code = """1 + 2
3 - 4
5 * 6
7 / 8
"""
    actual = chunk_code(code, 12)
    expected = [
        "1 + 2\n3 - 4\n",
        "5 * 6\n7 / 8\n",
    ]
    assert list(actual) == expected

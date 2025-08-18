import pytest

from sphinx_notion.nodes.literal_block import to_notion_language


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

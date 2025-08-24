from sphinx.application import Sphinx

from sphinx_notion.builders import NotionBuilder

__version__ = "0.0.4"

NOTION_API_CHARACTER_UPPER_LIMIT = 2_000


def setup(app: Sphinx):
    app.add_config_value(
        "sphinx_notion_character_upper_limit",
        NOTION_API_CHARACTER_UPPER_LIMIT,
        True,
    )
    app.add_builder(NotionBuilder)

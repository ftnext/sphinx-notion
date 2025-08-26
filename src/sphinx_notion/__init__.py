from sphinx.application import Sphinx

from sphinx_notion.builders import NotionBuilder

__version__ = "0.0.4"

# https://developers.notion.com/reference/request-limits#size-limits
NOTION_API_RICH_TEXT_CONTENT_CHARACTER_LIMIT = 2_000


def setup(app: Sphinx):
    app.add_config_value(
        "sphinx_notion_code_block_character_limit",
        NOTION_API_RICH_TEXT_CONTENT_CHARACTER_LIMIT,
        "env",
    )
    app.add_builder(NotionBuilder)

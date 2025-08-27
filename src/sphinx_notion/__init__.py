from sphinx.application import Sphinx

from sphinx_notion.builders import NotionBuilder

__version__ = "0.0.5"

# https://developers.notion.com/reference/request-limits#size-limits
NOTION_API_RICH_TEXT_CONTENT_CHARACTER_LIMIT = 2_000


def setup(app: Sphinx):
    app.add_config_value(
        "sphinx_notion_code_block_character_limit",
        NOTION_API_RICH_TEXT_CONTENT_CHARACTER_LIMIT,
        "env",
        description=(
            "Character limit for Sphinx code-blocks. "
            "Cannot exceed 2000 characters, "
            "as it is the size limit of Notion's rich_text.content."
        ),
    )
    app.add_builder(NotionBuilder)

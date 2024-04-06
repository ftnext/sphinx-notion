from sphinx.builders.text import TextBuilder

from sphinx_notion.writers import NotionTranslator


class NotionBuilder(TextBuilder):
    name = "notion"
    out_suffix = ".json"
    default_translator_class = NotionTranslator

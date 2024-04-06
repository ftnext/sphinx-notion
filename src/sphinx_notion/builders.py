from sphinx.builders.text import TextBuilder


class NotionBuilder(TextBuilder):
    name = "notion"
    out_suffix = ".json"

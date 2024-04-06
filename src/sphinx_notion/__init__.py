from sphinx.application import Sphinx

from sphinx_notion.builders import NotionBuilder

__version__ = "0.0.1"


def setup(app: Sphinx):
    app.add_builder(NotionBuilder)

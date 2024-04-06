from __future__ import annotations

import json
from typing import Any

from docutils import nodes
from sphinx.builders.text import TextBuilder
from sphinx.writers.text import TextTranslator


class NotionTranslator(TextTranslator):
    def __init__(self, document: nodes.document, builder: TextBuilder) -> None:
        super().__init__(document, builder)
        self._json: list[Any] = []

    def depart_document(self, node: nodes.Element) -> None:
        super().depart_document(node)
        self.body = json.dumps(self._json, ensure_ascii=False, indent=4)

    def visit_section(self, node: nodes.Element) -> None:
        super().visit_section(node)

        heading_type = (
            f"heading_{self.sectionlevel}"
            if self.sectionlevel <= 3
            else "paragraph"
        )
        heading_text = node[0].astext() if len(node) >= 2 else node.astext()
        self._json.append(
            {
                "object": "block",
                "type": heading_type,
                heading_type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": heading_text},
                        }
                    ]
                },
            }
        )

    @staticmethod
    def convert_inline_elements(node: nodes.Node) -> dict[str, Any]:
        if isinstance(node, nodes.strong):
            return {
                "type": "text",
                "text": {"content": node.astext()},
                "annotations": {"bold": True},
            }
        if isinstance(node, nodes.reference):
            return {
                "type": "text",
                "text": {
                    "content": node.attributes["name"],
                    "link": node.attributes["refuri"],
                },
            }
        # node is Text
        return {
            "type": "text",
            "text": {"content": node.astext().strip(" ")},
        }

    def visit_paragraph(self, node: nodes.Element) -> None:
        super().visit_paragraph(node)

        if isinstance(node.parent, nodes.list_item):
            # Ignore list_item's paragraph (Cause duplication)
            return

        texts = [self.convert_inline_elements(n) for n in node]

        self._json.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": texts},
            }
        )

    def visit_bullet_list(self, node: nodes.Element) -> None:
        super().visit_bullet_list(node)

        self._json.extend(
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": list_item.astext()},
                        }
                    ]
                },
            }
            for list_item in node
        )

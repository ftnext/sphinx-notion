from __future__ import annotations

import json
from typing import Any

from docutils.nodes import Element, Node, document, strong
from sphinx.builders.text import TextBuilder
from sphinx.writers.text import TextTranslator


class NotionTranslator(TextTranslator):
    def __init__(self, document: document, builder: TextBuilder) -> None:
        super().__init__(document, builder)
        self._json: list[Any] = []

    def depart_document(self, node: Element) -> None:
        super().depart_document(node)
        self.body = json.dumps(self._json, ensure_ascii=False, indent=4)

    def visit_section(self, node: Element) -> None:
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
    def convert_inline_elements(node: Node) -> dict[str, Any]:
        if isinstance(node, strong):
            return {
                "type": "text",
                "text": {"content": node.astext()},
                "annotations": {"bold": True},
            }
        # node is Text
        return {
            "type": "text",
            "text": {"content": node.astext().strip(" ")},
        }

    def visit_paragraph(self, node: Element) -> None:
        super().visit_paragraph(node)

        texts = [self.convert_inline_elements(n) for n in node]

        self._json.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": texts},
            }
        )

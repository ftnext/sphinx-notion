from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, cast

from docutils import nodes
from sphinx.builders.text import TextBuilder
from sphinx.util import logging
from sphinx.writers.text import TextTranslator

from sphinx_notion.nodes.literal_block import (
    chunk_code,
    get_standard_pygments_language,
    to_notion_language,
)

if TYPE_CHECKING:
    from sphinx_notion.types import (
        NotionCode,
        NotionCodeBlock,
        NotionCodeWithCaption,
    )

logger = logging.getLogger(__name__)


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
        if isinstance(node, nodes.emphasis):
            return {
                "type": "text",
                "text": {"content": node.astext()},
                "annotations": {"italic": True},
            }
        if isinstance(node, nodes.reference):
            return {
                "type": "text",
                "text": {
                    "content": node.astext(),
                    "link": {
                        "type": "url",
                        "url": node.attributes["refuri"],
                    },
                },
            }
        # node is Text
        return {
            "type": "text",
            "text": {"content": node.astext().strip(" ")},
        }

    @staticmethod
    def convert_paragraph(node: nodes.paragraph):
        paragraph: list[dict[str, Any]] = []
        for child in node:
            element = NotionTranslator.convert_inline_elements(child)
            if len(paragraph) > 0:
                if (
                    "link" in element["text"]
                    and element["text"]["link"]["url"]
                    == element["text"]["content"]
                ):
                    paragraph[-1]["text"]["content"] += " "
                elif (
                    "link" in paragraph[-1]["text"]
                    and paragraph[-1]["text"]["link"]["url"]
                    == paragraph[-1]["text"]["content"]
                ):
                    element["text"]["content"] = (
                        " " + element["text"]["content"]
                    )
            paragraph.append(element)
        return paragraph

    def visit_paragraph(self, node: nodes.Element) -> None:
        super().visit_paragraph(node)

        ignored_parents = (
            nodes.list_item,
            nodes.note,
            nodes.tip,
            nodes.hint,
            nodes.block_quote,
        )

        if isinstance(node.parent, ignored_parents):
            return

        self._json.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": self.convert_paragraph(
                        cast(nodes.paragraph, node)
                    )
                },
            }
        )

    def visit_bullet_list(self, node: nodes.Element) -> None:
        super().visit_bullet_list(node)

        self._json.extend(
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": self.convert_paragraph(
                        cast(
                            nodes.paragraph,
                            cast(nodes.list_item, list_item)[0],
                        )
                    )
                },
            }
            for list_item in node
        )

    def visit_enumerated_list(self, node: nodes.Element) -> None:
        super().visit_enumerated_list(node)

        self._json.extend(
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": self.convert_paragraph(
                        cast(
                            nodes.paragraph,
                            cast(nodes.list_item, list_item)[0],
                        )
                    )
                },
            }
            for list_item in node
        )

    def visit_literal_block(self, node: nodes.Element) -> None:
        super().visit_literal_block(node)

        pygments_language = get_standard_pygments_language(
            node.attributes["language"]
        )
        notion_language = to_notion_language(pygments_language)

        caption: str | None = None
        if isinstance(node.parent, nodes.container):
            for child in node.parent:
                if isinstance(child, nodes.caption):
                    caption = child.astext()
                    break

        character_limit = (
            self.builder.config.sphinx_notion_code_block_character_limit
        )
        code_text = node.astext().rstrip()
        if len(code_text) > character_limit:
            logger.info(
                "Code block exceeds character limit (%d > %d)",
                len(code_text),
                character_limit,
            )

        chunks = list(chunk_code(code_text, character_limit))
        chunk_count = len(chunks)
        for i, chunk in enumerate(chunks, start=1):
            code: NotionCodeWithCaption | NotionCode
            if caption:
                caption_text = (
                    f"{caption} ({i}/{chunk_count})"
                    if chunk_count > 1
                    else caption
                )
                code = {
                    "rich_text": [
                        {"type": "text", "text": {"content": chunk}}
                    ],
                    "language": notion_language,
                    "caption": [
                        {
                            "type": "text",
                            "text": {
                                "content": caption_text,
                            },
                        }
                    ],
                }
            else:
                code = {
                    "rich_text": [
                        {"type": "text", "text": {"content": chunk}}
                    ],
                    "language": notion_language,
                }
            code_block: NotionCodeBlock = {
                "object": "block",
                "type": "code",
                "code": code,
            }
            self._json.append(code_block)

    def _create_callout_block(
        self, node: nodes.Element, icon: str, color: str
    ) -> None:
        content_parts = []
        for child in node:
            if isinstance(child, nodes.paragraph):
                content_parts.append(child.astext())

        content = "\n".join(content_parts)

        self._json.append(
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": content},
                        }
                    ],
                    "icon": {"type": "emoji", "emoji": icon},
                    "color": color,
                },
            }
        )

    def visit_note(self, node: nodes.Element) -> None:
        super().visit_note(node)
        self._create_callout_block(node, "📝", "blue_background")

    def visit_tip(self, node: nodes.Element) -> None:
        super().visit_tip(node)
        self._create_callout_block(node, "✨", "gray_background")

    def visit_hint(self, node: nodes.Element) -> None:
        super().visit_hint(node)
        self._create_callout_block(node, "💡", "green_background")

    def visit_block_quote(self, node: nodes.Element) -> None:
        super().visit_block_quote(node)

        content_parts = []
        for child in node:
            if isinstance(child, nodes.paragraph):
                content_parts.append(child.astext())

        content = "\n".join(content_parts)

        self._json.append(
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": content},
                        }
                    ],
                },
            }
        )

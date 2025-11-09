from typing import Literal, TypedDict


class NotionRichTextContent(TypedDict):
    content: str


class NotionRichText(TypedDict):
    type: Literal["text"]
    text: NotionRichTextContent


class NotionCode(TypedDict):
    rich_text: list[NotionRichText]
    language: str


class NotionCodeWithCaption(NotionCode):
    caption: list[NotionRichText]


class NotionCodeBlock(TypedDict):
    object: Literal["block"]
    type: Literal["code"]
    code: NotionCode | NotionCodeWithCaption

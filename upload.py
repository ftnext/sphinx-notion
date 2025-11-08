# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "notion-client",
# ]
# ///

import argparse
import json
import os
from itertools import batched
from pathlib import Path

from notion_client import Client

CHILDLEN_LIMIT = 100

notion = Client(auth=os.environ["NOTION_TOKEN"])  # integration secret

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload to Notion")
    parser.add_argument(
        "-f", "--file", help="JSON File to upload", required=True, type=Path
    )
    parser.add_argument(
        "-p",
        "--parent_page_id",
        help="Parent page ID (integration connected)",
        required=True,
    )
    parser.add_argument(
        "-t", "--title", help="Title of the new page", required=True
    )
    args = parser.parse_args()

    with args.file.open("r", encoding="utf-8") as f:
        contents = json.load(f)

    if len(contents) <= CHILDLEN_LIMIT:
        new_page = notion.pages.create(
            parent={"type": "page_id", "page_id": args.parent_page_id},
            properties={
                "title": {"title": [{"text": {"content": args.title}}]},
            },
            children=contents,
        )
        print(
            f"Created {args.title}: https://notion.so/{new_page['id'].replace('-', '')}"
        )
    else:
        for i, chunk in enumerate(batched(contents, CHILDLEN_LIMIT), start=1):
            new_page = notion.pages.create(
                parent={"type": "page_id", "page_id": args.parent_page_id},
                properties={
                    "title": {
                        "title": [{"text": {"content": f"{args.title}-{i}"}}]
                    },
                },
                children=chunk,
            )
            print(
                f"Created {args.title}-{i}: https://notion.so/{new_page['id'].replace('-', '')}"
            )

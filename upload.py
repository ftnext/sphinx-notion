# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "notion-client",
# ]
# ///

import argparse
import json
import os
from pathlib import Path

from notion_client import Client

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

    new_page = notion.pages.create(
        parent={"type": "page_id", "page_id": args.parent_page_id},
        properties={
            "title": {"title": [{"text": {"content": args.title}}]},
        },
        children=contents,
    )

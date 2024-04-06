import json
import shutil
from pathlib import Path


class TestNotionBuilder:
    def test_can_build(
        self, make_app, sphinx_test_tempdir: Path, rootdir: Path
    ) -> None:
        case_name = "can-build"
        srcdir = sphinx_test_tempdir / case_name
        testroot_path = rootdir / f"test-{case_name}"
        shutil.copytree(testroot_path, srcdir)

        app = make_app("notion", srcdir=srcdir)
        app.build()

        assert (app.outdir / "index.json").exists()

    def test_paragraph(
        self, make_app, sphinx_test_tempdir: Path, rootdir: Path
    ) -> None:
        case_name = "paragraph"
        srcdir = sphinx_test_tempdir / case_name
        testroot_path = rootdir / f"test-{case_name}"
        shutil.copytree(testroot_path, srcdir)

        app = make_app("notion", srcdir=srcdir)
        app.build()

        actual = json.loads((app.outdir / "index.json").read_text())
        expected = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Hello World\nこんにちは"},
                        }
                    ]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "2つ目の段落"},
                        }
                    ]
                },
            },
        ]
        assert actual == expected

    def test_heading(
        self, make_app, sphinx_test_tempdir: Path, rootdir: Path
    ) -> None:
        case_name = "heading"
        srcdir = sphinx_test_tempdir / case_name
        testroot_path = rootdir / f"test-{case_name}"
        shutil.copytree(testroot_path, srcdir)

        app = make_app("notion", srcdir=srcdir)
        app.build()

        actual = json.loads((app.outdir / "index.json").read_text())
        expected = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Heading 1"},
                        }
                    ]
                },
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "見出し 2"},
                        }
                    ]
                },
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Level 3 Heading"},
                        }
                    ]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "レベル 4 見出し"},
                        }
                    ]
                },
            },
        ]
        assert actual == expected

    def test_inline(
        self, make_app, sphinx_test_tempdir: Path, rootdir: Path
    ) -> None:
        case_name = "inline"

        srcdir = sphinx_test_tempdir / case_name
        testroot_path = rootdir / f"test-{case_name}"
        shutil.copytree(testroot_path, srcdir)

        app = make_app("notion", srcdir=srcdir)
        app.build()

        actual = json.loads((app.outdir / "index.json").read_text())
        expected = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "大事なところを"},
                        },
                        {
                            "type": "text",
                            "text": {"content": "強調"},
                            "annotations": {"bold": True},
                        },
                    ]
                },
            }
        ]
        assert actual == expected

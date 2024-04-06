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

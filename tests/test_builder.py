import json
import shutil
from pathlib import Path

import pytest


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

    @pytest.mark.parametrize(
        "case_name",
        [
            "paragraph",
            "heading",
            "inline",
            "list-item",
            "code",
            "codeblock-limit",
        ],
    )
    def test_convert(
        self,
        make_app,
        sphinx_test_tempdir: Path,
        rootdir: Path,
        case_name: str,
    ) -> None:
        srcdir = sphinx_test_tempdir / case_name
        testroot_path = rootdir / f"test-{case_name}" / "source"
        shutil.copytree(testroot_path, srcdir)

        app = make_app("notion", srcdir=srcdir)
        app.build()

        actual = json.loads((app.outdir / "index.json").read_text())
        expected = json.loads(
            (rootdir / f"test-{case_name}" / "expected.json").read_text()
        )
        assert actual == expected

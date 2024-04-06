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

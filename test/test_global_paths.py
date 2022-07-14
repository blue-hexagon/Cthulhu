import os

from src.conf.global_paths import paths


def test_paths_resolves() -> None:
    assert os.path.exists(paths["ROOT_DIR"])
    assert os.path.exists(paths["SRC_DIR"])
    assert os.path.exists(paths["TEST_DIR"])
    assert os.path.exists(paths["OUT_DIR"])

import os

from src.conf import global_paths


def test_paths_resolves():
    assert os.path.exists(global_paths.config["ROOT_DIR"])
    assert os.path.exists(global_paths.config["SRC_DIR"])
    assert os.path.exists(global_paths.config["TEST_DIR"])
    assert os.path.exists(global_paths.config["OUT_DIR"])

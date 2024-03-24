import os

from src.conf.path_manager import PathManager


def test_paths_resolves() -> None:
    pm = PathManager()
    assert os.path.exists(pm.app_root)
    assert os.path.exists(pm.out_root)
    assert os.path.exists(pm.src_root)
    assert os.path.exists(pm.app_config)

import os
import pathlib

from src.utils.singleton import Singleton


class PathManager(metaclass=Singleton):
    def __init__(self) -> None:
        # Folders
        self.app_root: pathlib.Path = pathlib.Path(self.folder_exists("Cthulhu")).resolve()
        self.src_root: pathlib.Path = self.app_root / "src"
        self.out_root: pathlib.Path = self.app_root / "out"

        # Directories
        self.app_config: pathlib.Path = self.app_root / "app_config.toml"

        """ Ensure certain directories exists """
        # make_dirs = [self.out_root]
        # for path in [v for k, v in vars(self).items() if k in make_dirs]:
        #   os.makedirs(path, exist_ok=True)

    @staticmethod
    def folder_exists(folder_name: str = "Cthulhu") -> str | bool:
        """
        Recursively check if a folder exists in the current directory or any of its parent directories.

        Args:
        - folder_name (str): The name of the folder to check for existence.

        Returns:
        - bool: True if the folder exists in the current directory or any of its parent directories, False otherwise.
        """
        current_dir = os.path.abspath(os.curdir)

        while True:
            if os.path.exists(os.path.join(current_dir, folder_name)) and os.path.isdir(
                    os.path.join(current_dir, folder_name)):
                return os.path.join(current_dir, folder_name)

            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir

        return False


if __name__ == '__main__':
    pm = PathManager()
    print(pm.app_root)
    print(pm.src_root)
    print(pm.out_root)

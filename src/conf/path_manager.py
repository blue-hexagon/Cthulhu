import os
import pathlib

from src.utils.singleton import Singleton


class PathManager(metaclass=Singleton):
    """Manages paths for the application.
    app_root makes up the base paths from which every other path is derived.
    It finds the app_root by recursively searching upwards for the project folder "Cthulhu",
    starting from the location of __file__"""

    def __init__(self) -> None:
        project_root = self.find_project_root("Cthulhu")
        if project_root is None:
            raise RuntimeError("Unable to find project root folder which should be 'Cthulhu' (first letter uppercased)")
        self.app_root: pathlib.Path = pathlib.Path(project_root).resolve()
        self.src_root: pathlib.Path = self.app_root / "src"
        self.out_root: pathlib.Path = self.app_root / "out"

        # Directories
        self.app_config: pathlib.Path = self.app_root / "app_config.toml"
        self.payload_profiles: pathlib.Path = self.app_root / "payload_profiles.yml"

        """ Ensure certain directories exists """
        # make_dirs = [self.out_root]
        # for path in [v for k, v in vars(self).items() if k in make_dirs]:
        #   os.makedirs(path, exist_ok=True)

    @staticmethod
    def find_project_root(folder_name: str = "Cthulhu") -> str | None:
        """
        Recursively check if a folder exists in the current directory or any of its parent directories.

        Args:
        - folder_name (str): The name of the folder to check for existence.

        Returns:
        - bool: True if the folder exists in the current directory or any of its parent directories, False otherwise.
        """
        current_dir = os.path.abspath(os.curdir)

        while True:
            if os.path.exists(os.path.join(current_dir, folder_name)) and os.path.isdir(os.path.join(current_dir, folder_name)):
                return os.path.join(current_dir, folder_name)

            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir

        return None


if __name__ == "__main__":
    pm = PathManager()
    print(pm.app_root)
    print(pm.src_root)
    print(pm.out_root)

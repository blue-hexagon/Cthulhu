import os
import pathlib

paths = {
    "ROOT_DIR": pathlib.Path(__file__).parent.parent.parent.absolute(),
    "SRC_DIR": os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "src"),
    "OUT_DIR": os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "out"),
    "TEST_DIR": os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "test"),
}

if __name__ == "__main__":
    print(paths["ROOT_DIR"])
    print(paths["SRC_DIR"])
    print(paths["OUT_DIR"])
    print(paths["TEST_DIR"])

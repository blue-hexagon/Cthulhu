import os
import pathlib

config = {
    "ROOT_DIR": pathlib.Path(__file__).parent.parent.parent.absolute(),
    "SRC_DIR": os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "src"),
    "OUT_DIR": os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "out"),
    "TEST_DIR": os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute(), "test"),
}

if __name__ == "__main__":
    print(config["ROOT_DIR"])
    print(config["SRC_DIR"])
    print(config["OUT_DIR"])
    print(config["TEST_DIR"])

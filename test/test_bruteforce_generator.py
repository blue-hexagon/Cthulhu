import os
import pathlib

from src.bruteforce_generator import BruteforcePWGenerator
from src.conf import filewriter


def test_bruteforce_filewriter():
    __filename = "test123.txt"
    BruteforcePWGenerator(1, 4, filename=__filename).use_filewriter(["abc0123"])
    assert pathlib.Path(os.path.join(filewriter.config["OUT_DIR"], __filename)).resolve().is_file()
    os.remove(os.path.join(filewriter.config["OUT_DIR"], __filename))


def test_bruteforce_generator():
    pw_permuter = BruteforcePWGenerator(2, 4).use_generator(["abc"])
    while True:
        try:
            assert next(pw_permuter) is not None
        except StopIteration:
            break

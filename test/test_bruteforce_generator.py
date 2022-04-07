import itertools
import os
import pathlib

from src.bruteforce_generator import BruteforcePWGenerator
from src.conf import global_paths


def test_bruteforce_filewriter():
    filename = "test123.txt"
    BruteforcePWGenerator(1, 4, filename=filename).use_filewriter(["abc0123"])
    assert pathlib.Path(os.path.join(global_paths.config["OUT_DIR"], filename)).resolve().is_file()
    os.remove(os.path.join(global_paths.config["OUT_DIR"], filename))
    assert pathlib.Path(os.path.join(global_paths.config["OUT_DIR"], filename)).exists() is False



def test_bruteforce_generator():
    pw_permuter = BruteforcePWGenerator(2, 2, combinatoric_iterator=itertools.product).use_generator(
        ["0123456789abcdef"])
    while True:
        try:
            assert next(pw_permuter) is not None
        except StopIteration:
            break


def test_bruteforce_generator_permutations():
    pw_permuter = BruteforcePWGenerator(2, 2, combinatoric_iterator=itertools.permutations).use_generator(
        ["0123456789abcdef"])
    while True:
        try:
            assert next(pw_permuter) not in ["aa", "bb", "cc", "dd", "ee", "ff", "00", "11", "22", "33", "44", "55",
                                             "66", "77", "88", "99"]
        except StopIteration:
            break


def test_bruteforce_generator_product():
    pw_permuter = BruteforcePWGenerator(2, 2, combinatoric_iterator=itertools.product).use_generator(["abcdef"])
    assert next(pw_permuter) == "aa"
    pw_permuter = BruteforcePWGenerator(3, 8, combinatoric_iterator=itertools.product).use_generator(["bcdef"])
    assert next(pw_permuter) == "bbb"

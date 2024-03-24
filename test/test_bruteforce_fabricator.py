import itertools
import os
import pathlib

from src.conf.path_manager import paths
from src.passgen.bruteforce_fabricator import BruteforcePWFabricator


def test_bruteforce_filewriter():
    filename = "test123.txt"
    BruteforcePWFabricator(1, 4, filename=filename).use_filewriter(["abc0123"])
    assert pathlib.Path(os.path.join(paths["OUT_DIR"], filename)).resolve().is_file()
    os.remove(os.path.join(paths["OUT_DIR"], filename))
    assert pathlib.Path(os.path.join(paths["OUT_DIR"], filename)).exists() is False


def test_bruteforce_generator():
    bruteforce_pw_generator = BruteforcePWFabricator(2, 2, combinatoric_iterator=itertools.product).use_generator(["0123456789abcdef"])
    while True:
        try:
            assert next(bruteforce_pw_generator) is not None
        except StopIteration:
            break
        except Exception:
            assert False


def test_bruteforce_fabricator_permutation_fabricator():
    pw_permuter = BruteforcePWFabricator(2, 2, combinatoric_iterator=itertools.permutations).use_generator(["0123456789abcdef"])
    while True:
        try:
            assert next(pw_permuter) not in ["aa", "bb", "cc", "dd", "ee", "ff", "00", "11", "22", "33", "44", "55", "66", "77", "88", "99"]
        except StopIteration:
            break


def test_bruteforce_product_fabricator():
    pw_permuter = BruteforcePWFabricator(2, 2, combinatoric_iterator=itertools.product).use_generator(["abcdef"])
    assert next(pw_permuter) == "aa"
    pw_permuter = BruteforcePWFabricator(3, 8, combinatoric_iterator=itertools.product).use_generator(["bcdef"])
    assert next(pw_permuter) == "bbb"

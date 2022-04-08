import os
import pathlib

from src.conf import global_paths
from src.conf.global_paths import paths
from src.wordlist_fabricator import WordlistPWFabricator


def test_wordlist_filewriter():
    filename = "test_wordlist_passwords.txt"
    WordlistPWFabricator(filename=filename).use_filewriter(
        (
            ["admin", "Admin", "@dmin", "adm1n", "Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
            ["123", "1234"],
            ["!", "!1", "*"],
        )
    )
    assert pathlib.Path(os.path.join(paths["OUT_DIR"], filename)).resolve().is_file()
    os.remove(os.path.join(paths["OUT_DIR"], filename))
    assert pathlib.Path(os.path.join(paths["OUT_DIR"], filename)).exists() is False


def test_wordlist_generator():
    dictionary_map = WordlistPWFabricator().use_generator(
        (
            ["København", "københavn", "Copenhagen", "copenhagen"],
            ["!", "!1", "*", "123", "2600", "2600!"],
        )
    )
    while True:
        try:
            assert next(dictionary_map) is not None
        except StopIteration:
            break
        except Exception:
            assert False

import os
import pathlib

from src.conf.path_manager import PathManager
from src.passgen.wordlist_fabricator import WordlistPWFabricator


def test_wordlist_filewriter() -> None:
    pm = PathManager()
    filename = "test_wordlist_passwords.txt"
    WordlistPWFabricator(filename=filename).use_filewriter(
        (
            ["admin", "Admin", "@dmin", "adm1n", "Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
            ["123", "1234"],
            ["!", "!1", "*"],
        )
    )
    assert pathlib.Path(os.path.join(pm.out_root, filename)).resolve().is_file()
    os.remove(os.path.join(pm.out_root, filename))
    assert pathlib.Path(os.path.join(pm.out_root, filename)).exists() is False


def test_wordlist_generator() -> None:
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

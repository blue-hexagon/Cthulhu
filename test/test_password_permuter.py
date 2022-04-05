import pathlib

import filewriter_config
from password_permuter import PasswordPermuter

# def test_my_function(benchmark):
#     result = benchmark(test)


def test_bruteforce_filewriter():
    PasswordPermuter(4, 4, "hexdigits__4_4.txt").use_filewriter(["abcdefABCDEF0123456789"])
    assert pathlib.Path(filewriter_config.config["OUTPUT_DIR"] + "hexdigits__4_4.txt").resolve().is_file()


def test_bruteforce_generator():
    pw_permuter = PasswordPermuter(4, 4).use_generator(["abcdefABCDEF0123456789"])
    assert next(pw_permuter) is not None


def test_dictionary_filewriter():
    PasswordPermuter(4, 4, "dict_001.txt").use_filewriter(
        (
            ["123"],
            [" "],
            ["!", "!1", "*"],
            ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
            ["admin", "Admin", "@dmin", "adm1n"],
        )
    )
    assert pathlib.Path(filewriter_config.config["OUTPUT_DIR"] + "dict_001.txt").resolve().is_file()


def test_dictionary_generator():
    pw_permuter = PasswordPermuter().use_generator(
        (
            ["123"],
            [" "],
            ["!", "!1", "*"],
            ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
            ["admin", "Admin", "@dmin", "adm1n"],
        )
    )
    assert next(pw_permuter) is not None

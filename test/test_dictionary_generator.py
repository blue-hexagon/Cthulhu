# import pathlib
#
# from src.conf import filewriter
# from src.dictionary_generator import DictionaryPWGenerator
#
#
# def test_dictionary_filewriter():
#     DictionaryPWGenerator(filename="dict_001.txt").use_filewriter(
#         (
#             ["123"],
#             ["-"],
#             ["!", "!1", "*"],
#             ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
#             ["admin", "Admin", "@dmin", "adm1n"],
#         )
#     )
#     assert pathlib.Path(filewriter.config["OUTPUT_DIR"] + "dict_001.txt").resolve().is_file()
#
#
#
# def test_dictionary_generator():
#     pw_permuter = DictionaryPWGenerator().use_generator(
#         (
#             ["123"],
#             ["-"],
#             ["!", "!1", "*"],
#             ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
#             ["admin", "Admin", "@dmin", "adm1n"],
#         )
#     )
#     assert next(pw_permuter) is not None

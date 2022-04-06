import os
import sys
from typing import Generator, List, Set

from src.abstract_generator import PWGenerator
from src.conf import filewriter


class CharacterClass:
    """
    A collection of character groupings to be used as paramaters to <PasswordPermutator>.

    To make a collection you don't have to instantiate the class, simply reference it's class attributes.

    You can modify them for your own use adding language specific characters (such as ÆØÅæøå) to the ascii groups.

    You can also extend the groups by adding a new one, such as:
    BASE64=ASCII_LOWERCASE + ASCII_UPPERCASE  + "/+=".
    """

    WHITESPACE = " \t\n\r\v\f"
    ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE
    DIGITS = "0123456789"
    HEXDIGITS_LOWER = DIGITS + "abcdef"
    HEXDIGITS_UPPER = DIGITS + "ABCDEF"
    HEXDIGITS = DIGITS + "abcdef" + "ABCDEF"
    OCTDIGITS = "01234567"
    PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    PRINTABLE = DIGITS + ASCII_LETTERS + PUNCTUATION + WHITESPACE


class BruteforcePWGenerator(PWGenerator):
    def __init__(self, min_len: int, max_len: int, /, *, filename: str = None) -> None:
        super().__init__()
        if min_len > max_len:
            raise ValueError("Min length cannot be greater than max length.")
        self._min_len = min_len
        self._max_len = max_len
        if filename:
            self._filename = filename

    @staticmethod
    def _convert_lists_to_set(character_lists: List) -> Set:
        """Check if input is valid"""
        if not isinstance(character_lists, list):
            raise ValueError("Use List[str,str,...] or List[str] where len(str) > 1.")
        if len(character_lists) == 0:
            sys.exit("Choose at least one CharacterClass or character-list")

        """ Make the conversion """
        chars = set()
        for char_seq in character_lists:
            chars |= set(char_seq)
        return chars

    def use_filewriter(self, character_lists: List) -> None:
        """Check if filename was not set"""
        try:
            hasattr(self, self._filename)
        except AttributeError:
            print("A filename attribute is needed when using the `filewriter` method.")

        """ Calc & write min_len to max_len password combinations """
        character_set = self._convert_lists_to_set(character_lists)
        with open(os.path.join(filewriter.config["OUT_DIR"], self._filename), "w") as file_out:
            for password_length in range(self._min_len, self._max_len + 1):
                for perms in list(PWGenerator.CARTESIAN_PRODUCT(character_set, repeat=password_length)):
                    for perm in perms:
                        file_out.write(perm)
                    file_out.write("\n")

    def use_generator(self, character_lists: List) -> Generator:
        """Yield single permutations"""
        character_set = self._convert_lists_to_set(character_lists)
        for password_length in range(self._min_len, self._max_len + 1):
            for perms in list(PWGenerator.CARTESIAN_PRODUCT(character_set, repeat=password_length)):
                yield "".join(perms)

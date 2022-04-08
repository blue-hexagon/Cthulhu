import itertools
import os
import sys
from typing import Dict, Generator, List

from src.abstract_fabricator import PasswordFabricator
from src.conf import global_paths
from src.conf.global_paths import paths


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


class BruteforcePWFabricator(PasswordFabricator):
    def __init__(self, min_len: int, max_len: int, /, *, filename: str = None, combinatoric_iterator: callable = None) -> None:
        super().__init__()
        if min_len > max_len:
            raise ValueError("Min length cannot be greater than max length.")
        self._min_len = min_len
        self._max_len = max_len
        if combinatoric_iterator:
            self._combinatoric_iterator = combinatoric_iterator
        else:
            self._combinatoric_iterator = itertools.product
        if filename:
            self._filename = filename

    @staticmethod
    def __remove_list_duplicates(character_lists: List) -> List:
        """Check if input is valid and then proceed to remove any duplicates"""
        if not isinstance(character_lists, list):
            raise ValueError("Use List[str,str,...] or List[str] where len(str) > 1.")
        if len(character_lists) == 0:
            sys.exit("Choose at least one CharacterClass or character-list")

        character_set = set()
        for char_list in character_lists:
            character_set |= set(char_list)
        character_list_sorted = sorted(list(character_set))
        return character_list_sorted

    def __get_splat_arg(self, password_length) -> Dict[str, str]:
        """Itertools has four combinatoric iterator functions. This function returns the proper keyword-arguments for each of itertools combinatoric function"""
        if self._combinatoric_iterator is itertools.product:
            splat_arg = {"repeat": password_length}
        elif self._combinatoric_iterator is itertools.permutations:
            splat_arg = {"r": password_length}
        elif self._combinatoric_iterator is itertools.combinations:
            raise NotImplementedError(f"Callable `{self._combinatoric_iterator}` not implemented.")
        elif self._combinatoric_iterator is itertools.combinations_with_replacement:
            raise NotImplementedError(f"Callable `{self._combinatoric_iterator}` not implemented.")
        else:
            raise ValueError(f"Callable `{self._combinatoric_iterator}` not recognized.")
        return splat_arg

    def use_filewriter(self, character_lists: List) -> None:
        """Check if filename was not set"""
        try:
            hasattr(self, self._filename)
        except AttributeError:
            print("A filename attribute is needed when using the `filewriter` method.")

        """ Calc & write min_len to max_len password combinations """
        character_list_sorted = self.__remove_list_duplicates(character_lists)
        with open(os.path.join(paths["OUT_DIR"], self._filename), "w") as file_out:
            for password_length in range(self._min_len, self._max_len + 1):
                splat_arg = self.__get_splat_arg(password_length)
                for character_combination in list(self._combinatoric_iterator(character_list_sorted, **splat_arg)):
                    password = str()
                    for char in character_combination:
                        password += char
                    file_out.write(f"{password}\n")

    def use_generator(self, character_lists: List) -> Generator:
        """Yield permutations one by one"""
        character_list_sorted = self.__remove_list_duplicates(character_lists)
        for password_length in range(self._min_len, self._max_len + 1):
            splat_arg = self.__get_splat_arg(password_length)
            for perms in list(self._combinatoric_iterator(character_list_sorted, **splat_arg)):
                yield "".join(perms)

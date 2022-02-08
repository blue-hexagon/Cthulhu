import sys
from itertools import permutations
from typing import List, Set, Tuple


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
    HEXDIGITS = DIGITS + "abcdef" + "ABCDEF"
    OCTDIGITS = "01234567"
    PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    PRINTABLE = DIGITS + ASCII_LETTERS + PUNCTUATION + WHITESPACE


class PasswordGenerator:
    def __init__(self, min_len: int, max_len: int, /, filename: str):
        if min_len > max_len:
            raise ValueError("Min length cannot be greater than max length.")
        if not filename:
            raise ValueError("You must provide a filename")
        self._min_len = min_len
        self._max_len = max_len
        self._filename = filename

    def wordlist_permutator(self, word_list: Tuple[str, ...] | List[str]):
        if len(word_list) <= 1:
            sys.exit("You must choose add least two words for the permutator.")
        self._write_passwords(word_list)

    def character_permutator(self, characters: Set | List):
        character_set = set()
        for character_sequence in characters:
            character_set |= set(character_sequence)
        if len(characters) == 0:
            sys.exit("You must choose add least one CharacterClass for the permutator.")
        self._write_passwords(character_set)

    def _write_passwords(self, collection):
        with open(self._filename, "w") as file_out:
            for password_length in range(self._min_len, self._max_len + 1):
                perms = list(permutations(collection, password_length))
                for perm in perms:
                    for string in perm:
                        file_out.write(string)
                    file_out.write("\n")

    def _generate_passwords(self, collection):
        for password_length in range(self._min_len, self._max_len + 1):
            perms = list(permutations(collection, password_length))
            for perm in perms:
                yield perm


if __name__ == "__main__":
    # PasswordGenerator(1, 3, "digit_lower__1_3.txt").character_permutator(
    #     [CharacterClass.ASCII_LOWERCASE, CharacterClass.DIGITS])
    # PasswordGenerator(6, 6, "hexdigits__4_12.txt").wordlist_permutator(["abcdefABCDEF0123456789"])
    # PasswordGenerator(1, 3, "word-combo1.txt").wordlist_permutator(["123", "!"])
    x = PasswordGenerator(1, 4, "dsad")._generate_passwords(("!", "123"))
    for i in range(0, 100):
        print(x.__next__())

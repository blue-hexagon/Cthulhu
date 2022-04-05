import itertools
import sys
from itertools import permutations
from typing import Generator, List, Set, Tuple

import filewriter_config


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


class PasswordPermuter:
    def __init__(self, min_len: int = None, max_len: int = None, /, filename: str = None) -> None:
        if min_len and max_len:
            if min_len > max_len:
                raise ValueError("Min length cannot be greater than max length.")
            self._min_len = min_len
            self._max_len = max_len
        elif not min_len and not max_len:
            pass
        elif not min_len or not max_len:
            pass
        if filename:
            self._filename = filename

    def _parse_inputdata(self, input_data: Tuple | List) -> Set | List:
        if isinstance(input_data, list):
            """Handle character class permutations"""
            if len(input_data) == 0:
                sys.exit("You must choose at least one CharacterClass for the permutator.")
            return self._convert_list_to_set(input_data)
        elif isinstance(input_data, tuple):
            """Handle wordlist permutations"""
            if len(input_data) <= 1:
                sys.exit("You must choose at least two words for the permutator.")
            return self._get_shallow_product(input_data)
        else:
            raise ValueError("For character-level permutations use List[str,str,...]. For word-level permutations use Tuple[str,str,...]")

    @staticmethod
    def _convert_list_to_set(input_data) -> Set:
        # TODO: Can this be written as a list comprehension?
        # { seq for int} TODO
        character_set = set()
        for character_sequence in input_data:
            character_set |= set(character_sequence)
        return character_set

    @staticmethod
    def _get_shallow_product(data) -> List:
        nest_holder = list()
        for counter in range(len(data)):
            if isinstance(data[counter], list):
                nest_holder.append(data[counter].copy())
            elif isinstance(data[counter], str):
                nest_holder.append(data[counter])
            else:
                raise ValueError(f"You must quote any list-item in the word list you pass to the {PasswordPermuter}")
        # product =list(itertools.product(*nest_holder))
        # print(*product, sep="\n")
        return list(itertools.product(*nest_holder))

    def use_filewriter(self, input_data: Tuple | List) -> None:
        try:
            hasattr(self, self._filename)
        except AttributeError:
            print("<PasswordPermuter> needs a filename attribute in it's signature when using the filewriter() method.")
        input_data = self._parse_inputdata(input_data)
        self._write_passwords(input_data)

    def _write_passwords(self, data) -> None:
        """Calc & write min_len to max_len password permutations"""

        with open(filewriter_config.config["OUTPUT_DIR"] + self._filename, "w") as file_out:
            for password_length in range(self._min_len, self._max_len + 1):
                for perms in list(permutations(data, password_length)):
                    for perm in perms:
                        file_out.write(perm)
                    file_out.write("\n")

    def use_generator(self, input_data: Tuple | List) -> Generator:
        input_data = self._parse_inputdata(input_data)
        return self._yield_passwords(input_data)

    def _yield_passwords(self, data):
        """Yield single permutations"""
        for password_length in range(self._min_len, self._max_len + 1):
            for perms in list(permutations(data, password_length)):
                yield "".join(perms)


if __name__ == "__main__":
    PasswordPermuter(1, 3, "lower_hexdigits__1_3.txt").use_filewriter(
        [
            CharacterClass.ASCII_LOWERCASE,
            CharacterClass.DIGITS,
        ]
    )

    PasswordPermuter(4, 4, "hexdigits__4_4.txt").use_filewriter(["abcdefABCDEF0123456789"])
    dat = ()  # TODO: Replace with `data` param, when program is finished.
    prods = PasswordPermuter._get_shallow_product(dat)
    print(prods)
    PasswordPermuter(2, 5, "hahah.txt").use_filewriter(prods)
    # x = BruteforcePermuter(5, 5).return_generator(
    #     [
    #         ["123"],
    #         [" "],
    #         ["!", "!1", "*"],
    #         ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
    #         ["admin", "Admin", "@dmin", "adm1n"],
    #     ]
    # )
    # print(x)
    # while True:
    #     next(x)

import sys
from itertools import permutations
from typing import Generator, List, Set, Tuple


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
    def __init__(self, min_len: int, max_len: int, /, filename: str = None, bruteforce: bool = False) -> None:
        if min_len > max_len:
            raise ValueError("Min length cannot be greater than max length.")
        self._bruteforce = bruteforce
        self._min_len = min_len
        self._max_len = max_len
        if filename:
            self._filename = filename

    def _write_passwords(self, collection) -> None:
        with open(self._filename, "w") as file_out:
            for password_length in range(self._min_len, self._max_len + 1):
                perms = list(permutations(collection, password_length))
                for perm in perms:
                    for string in perm:
                        file_out.write(string)
                    file_out.write("\n")

    def _yield_passwords(self, collection):  # TODO: Type hint
        for password_length in range(self._min_len, self._max_len + 1):
            perms = list(permutations(collection, password_length))
            for perm in perms:
                yield "".join(perm)

    def _parse_inputdata(self, input_data: Tuple | List) -> Set:
        if isinstance(input_data, list):
            if len(input_data) == 0:
                sys.exit("You must choose add least one CharacterClass for the permutator.")
            return self._convert_list_to_set(input_data)

        elif isinstance(input_data, tuple):
            if len(input_data) <= 1:
                sys.exit("You must choose add least two words for the permutator.")
            return self._handle_tuples(input_data)
        else:
            raise ValueError("For character-level permutations use List[str,str,...]. For word-level permutations use Tuple[str,str,...]")

    @staticmethod
    def _convert_list_to_set(input_data) -> Set:
        character_set = set()
        for character_sequence in input_data:
            character_set |= set(character_sequence)
        return character_set

    @staticmethod
    def _handle_tuples(input_data) -> ...:
        from itertools import combinations

        coll = []
        for data in input_data:
            if isinstance(data, tuple):
                print("data", data)
                for dat in data:
                    print("dat: " + str(dat))
            else:
                coll.append(data)
                print("data: " + str(data))
        comb = combinations(["123", "!", ("admin", "Admin"), ("password", "Password")], 3)

        # Print the obtained combinations
        for i in list(comb):
            print(i)
        sys.exit(0)

    def run_filewriter(self, input_data: Tuple | List) -> None:
        try:
            hasattr(self, self._filename)
        except AttributeError:
            print("<PasswordPermuter> needs a filename attribute in it's signature when using the filewriter() method.")
        input_data = self._parse_inputdata(input_data)
        self._write_passwords(input_data)

    def return_generator(self, input_data: Tuple | List) -> Generator:
        input_data = self._parse_inputdata(input_data)
        return self._yield_passwords(input_data)

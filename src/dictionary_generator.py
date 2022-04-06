import itertools
import sys
from typing import Generator, List, Set, Tuple

from src.abstract_generator import PWGenerator
from src.bruteforce_generator import CharacterClass
from src.conf import filewriter


class DictionaryPWGenerator(PWGenerator):
    def __init__(self, min_len: int = None, max_len: int = None, /, *, filename: str = None) -> None:
        super().__init__()
        self.combinatorics_tool = PWGenerator.CARTESIAN_PRODUCT
        if min_len and max_len:
            if min_len > max_len:
                raise ValueError("Min length cannot be greater than max length.")
            self._min_len = min_len
            self._max_len = max_len
        elif not min_len and not max_len:
            pass
        if filename:
            self._filename = filename

    def _parse_inputdata(self, input_data: Tuple) -> List:
        """Handle wordlist permutations"""
        if not isinstance(input_data, tuple):
            raise ValueError("For character-level permutations use List[str,str,...]. For word-level permutations use Tuple[str,str,...]")
        if len(input_data) <= 1:
            sys.exit("You must choose at least two words for the permutator.")
        return self._get_shallow_product(input_data)

    @staticmethod
    def _convert_list_to_set(input_data) -> Set:
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
                raise ValueError(
                    f"You must quote any list-item in the word list you pass to the {DictionaryPWGenerator}")
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
        with open(filewriter.config["OUTPUT_DIR"] + self._filename, "w") as file_out:
            for password_length in range(self._min_len, self._max_len + 1):
                for perms in list(self.combinatorics_tool(data, repeat=password_length)):
                    for perm in perms:
                        file_out.write(perm)
                    file_out.write("\n")

    def use_generator(self, input_data: Tuple | List) -> Generator:
        input_data = self._parse_inputdata(input_data)
        return self._yield_passwords(input_data)

    def _yield_passwords(self, data):
        """Yield single permutations"""
        for password_length in range(self._min_len, self._max_len + 1):
            for perms in list(self.combinatorics_tool(data, repeat=password_length)):
                yield "".join(perms)


if __name__ == "__main__":
    DictionaryPWGenerator(3, 3, filename="hello.txt").use_filewriter(
        (
            ["admin", "@dmin"],
            ["123", "2027", "4800"],
            ["!"],
        )
    )
    bruteforce_map = DictionaryPWGenerator(3, 3, filename="hello.txt").use_generator(
        (
            ["admin", "@dmin"],
            ["123", "2027", "4800"],
            ["!"],
        )
    )

    while 1:
        try:
            print(next(bruteforce_map))
        except StopIteration:
            break

import itertools
import os
import sys
from typing import Generator, List, Tuple

from src.abstract_generator import PWGenerator
from src.conf import filewriter


class DictionaryPWGenerator(PWGenerator):
    def __init__(self, /, *, filename: str = None) -> None:
        super().__init__()
        self.combinatorics_tool = PWGenerator.CARTESIAN_PRODUCT
        self.__wordlist_length = None
        if filename:
            self._filename = filename

    def _parse_inputdata(self, input_data: Tuple) -> List:
        """Check if input is valid"""
        if not isinstance(input_data, tuple):
            raise ValueError("For word-level permutations use Tuple[[str,str],[str,str,str,str],[str]...]")
        if len(input_data) < 1:
            sys.exit("You must choose at least two words.")
        return self._get_shallow_product(input_data)

    def _get_shallow_product(self, data) -> List:
        nest_holder = list()
        self.__wordlist_length = len(data)
        for counter in range(len(data)):
            if isinstance(data[counter], list):
                nest_holder.append(data[counter].copy())
            elif isinstance(data[counter], str):
                nest_holder.append(data[counter])
            else:
                raise ValueError(f"You must quote any list-item in the word list you pass to the {DictionaryPWGenerator}")
        print(*list(itertools.product(*nest_holder)), sep="\n")
        return list(itertools.product(*nest_holder))

    def use_filewriter(self, word_lists: Tuple | List) -> None:
        """Check if filename was not set"""
        try:
            hasattr(self, self._filename)
        except AttributeError:
            print("A filename attribute is needed when using the `filewriter` method.")
        word_set = self._parse_inputdata(word_lists)
        """Calc & write min_len to max_len password permutations"""
        with open(os.path.join(filewriter.config["OUT_DIR"], self._filename), "w") as file_out:
            for password_length in range(self.__wordlist_length, self.__wordlist_length + 1):
                for perms in list(PWGenerator.CARTESIAN_PRODUCT(word_set, repeat=password_length)):
                    for perm in perms:
                        file_out.write(perm)
                    file_out.write("\n")

    def use_generator(self, word_lists: Tuple) -> Generator:
        words_set = self._parse_inputdata(word_lists)
        """Yield single permutations"""
        for password_length in range(self.__wordlist_length, self.__wordlist_length + 1):
            for perms in list(PWGenerator.CARTESIAN_PRODUCT(words_set, repeat=password_length)):
                yield "".join(perms)


if __name__ == "__main__":
    DictionaryPWGenerator(filename="hello.txt").use_filewriter(
        (
            ["admin", "@dmin"],
            ["123", "2027", "4800"],
            ["!"],
        )
    )
    bruteforce_map = DictionaryPWGenerator(filename="hello.txt").use_generator(
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

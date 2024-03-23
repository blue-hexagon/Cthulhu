import itertools
import os
import sys
from typing import Generator, List, Tuple

from src.conf.global_paths import paths
from src.passgen.abstract_fabricator import PasswordFabricator


class WordlistPWFabricator(PasswordFabricator):
    def __init__(self, /, *, filename: str = None) -> None:
        super().__init__()
        self.combinatorics_tool = itertools.product
        self.__wordlist_length = None
        if filename:
            self._filename = filename

    def __get_password_combinations(self, input_data: Tuple) -> List:
        """Check if input is valid"""
        if not isinstance(input_data, tuple):
            raise ValueError("For word-level permutations use Tuple[[str,str],[str,str,str,str],[str]...]")
        if len(input_data) < 1:
            sys.exit("You must choose at least two words.")

        password_collection = list()
        self.__wordlist_length = len(input_data)
        for counter in range(len(input_data)):
            if isinstance(input_data[counter], list):
                password_collection.append(input_data[counter].copy())
            elif isinstance(input_data[counter], str):
                password_collection.append(input_data[counter])
            else:
                raise ValueError(f"You must quote any list-item in the word list you pass to the {WordlistPWFabricator}")
        password_collection = list(itertools.product(*password_collection))
        password_collection = ["".join(password) for password in password_collection]
        return password_collection

    def use_filewriter(self, word_lists: Tuple | List) -> None:
        """Check if filename was not set"""
        try:
            hasattr(self, self._filename)
        except AttributeError:
            print("A filename attribute is needed when using the `filewriter` method.")

        """Calc & write min_len to max_len password combinations"""
        password_collection = self.__get_password_combinations(word_lists)
        with open(os.path.join(paths["OUT_DIR"], self._filename), "w") as file_out:
            for password in password_collection:
                file_out.write(f"{password}\n")

    def use_generator(self, word_lists: Tuple) -> Generator:
        """Yield permutations one by one"""
        password_collection = self.__get_password_combinations(word_lists)
        for password in password_collection:
            yield "".join(password)

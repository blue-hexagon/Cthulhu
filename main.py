import itertools
from typing import List

import password_generator
from password_generator import CharacterClass, PasswordPermuter


class ShallowProductOriginator:
    @staticmethod
    def get_shallow_product(data) -> List:
        list_counting = []
        nest_holder = list()

        for counter in range(len(data)):
            if isinstance(data[counter], list):
                list_counting.append(len(data[counter]))
                nest_holder.append(data[counter].copy())
            elif isinstance(data[counter], str):
                list_counting.append(1)
                nest_holder.append(data[counter])

            else:
                raise ValueError(
                    f"You must quote any list-item in the word list you pass to the {password_generator.PasswordPermuter}")

        product = list(itertools.product(*nest_holder))
        print(*product, sep="\n")
        return product


if __name__ == "__main__":
    # PasswordPermuter(1, 3, "lower_hexdigits__1_3.txt").run_filewriter(
    #     [
    #         CharacterClass.ASCII_LOWERCASE,
    #         CharacterClass.DIGITS,
    #     ]
    # )
    #
    # PasswordPermuter(4, 4, "hexdigits__4_4.txt").run_filewriter(["abcdefABCDEF0123456789"])
    dat = [  # TODO: Replace with `data` param, when program is finished.
        ["123", ],
        [" ", ],
        ["!", "!1", "*"],
        ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
        ["admin", "Admin", "@dmin", "adm1n"],
    ]
    prods = ShallowProductOriginator.get_shallow_product(dat)
    print(prods)
    # PasswordPermuter(2,5,"hahah.txt").run_filewriter(prods)
    # x = PasswordPermuter(1, 3).return_generator(
    #     [
    #         "123",
    #         "!",
    #         ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
    #         ["admin", "Admin"],
    #     ]
    # )

    # while input("Press any key to continue, <exit> to exit.") != "exit":
    #     try:
    #         print(next(x))
    #     except StopIteration("Generator exhausted"):
    #         sys.exit(0)

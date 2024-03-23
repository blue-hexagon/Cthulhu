import itertools

from src.passgen.bruteforce_fabricator import BruteforcePWFabricator, CharacterClass
from src.passgen.wordlist_fabricator import WordlistPWFabricator

if __name__ == "__main__":

    def use_bruteforce():
        BruteforcePWFabricator(4, 4, filename="hex_upper__4_4.txt", combinatoric_iterator=itertools.product).use_filewriter(
            [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
        )
        bruteforce_map = BruteforcePWFabricator(1, 3, combinatoric_iterator=itertools.permutations).use_generator(["abc"])
        while 1:
            try:
                print(next(bruteforce_map))
            except StopIteration:
                break

    def use_wordlist():
        WordlistPWFabricator(filename="wl_common__4_4.txt").use_filewriter((["app", "app-"], ["script"], ["-ch2", "-ch1"]))
        wordlist_generator = WordlistPWFabricator().use_generator(
            (
                ["København", "københavn", "Copenhagen", "copenhagen"],
                ["!", "!1", "*", "123", "2600", "2600!"],
            )
        )
        while 1:
            try:
                print(next(wordlist_generator))
            except StopIteration:
                break

    use_bruteforce()
    use_wordlist()

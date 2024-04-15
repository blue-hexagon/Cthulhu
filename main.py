import itertools
from threading import Thread

from src.cli.parser import Parser
from src.passgen.bruteforce_fabricator import BruteforcePWFabricator
from src.passgen.char_class import CharacterClass
from src.passgen.wordlist_fabricator import WordlistPWFabricator


def use_bruteforce():
    BruteforcePWFabricator(4, 4, filename="hex_upper__4_4.txt", combinatoric_iterator=itertools.product).use_filewriter(
        [CharacterClass.HEXDIGITS_UPPER]
    )
    bruteforce_map = BruteforcePWFabricator(4, 4, combinatoric_iterator=itertools.permutations).use_generator(
        [CharacterClass.DIGITS, "ABCDEF"]
    )
    while 1:
        try:
            print(next(bruteforce_map))
        except StopIteration:
            break


def use_wordlist():
    """Tip: Add an empty item to add permutations with and without the items of the array"""
    WordlistPWFabricator(filename="wl_common__4_4.txt").use_filewriter((["app", "app-"], ["script", ""], ["-ch2", "-ch1"]))
    wordlist_generator = WordlistPWFabricator().use_generator(
        (
            ["København", "københavn", "Copenhagen", "copenhagen"],
            ["!", "!1", "*", "123", "2600", "2600!", ""],
        )
    )
    while 1:
        try:
            print(next(wordlist_generator))
        except StopIteration:
            break


if __name__ == "__main__":

    if True:
        Parser().interpret()
    else:
        use_bruteforce()
        use_wordlist()

    # client = Parser('client')
    # server = Parser('server')
    # t2 =Thread(server.interpret()).run()
    # t1 =Thread(client.interpret()).run()

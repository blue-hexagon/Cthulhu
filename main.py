import itertools

from src.bruteforce_generator import BruteforcePWGenerator, CharacterClass

if __name__ == "__main__":
    BruteforcePWGenerator(4, 4, filename="hex_upper__4_4.txt", combinatoric_iterator=itertools.product).use_filewriter(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )
    bruteforce_map = BruteforcePWGenerator(1, 3, combinatoric_iterator=itertools.permutations).use_generator(["abc"])

    while 1:
        try:
            print(next(bruteforce_map))
        except StopIteration:
            break

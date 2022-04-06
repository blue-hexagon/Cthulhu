from src.bruteforce_generator import BruteforcePWGenerator, CharacterClass

if __name__ == "__main__":
    BruteforcePWGenerator(4, 4, filename="hello.txt").use_filewriter([CharacterClass.OCTDIGITS, CharacterClass.ASCII_LOWERCASE])
    bruteforce_map = BruteforcePWGenerator(3, 3, filename="test.txt").use_generator(["abc"])

    while 1:
        try:
            print(next(bruteforce_map))
        except StopIteration:
            break

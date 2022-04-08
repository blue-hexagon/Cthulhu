# Cthulhu

The distributed login-cracker with a module for creating word-lists and bruteforce lists.

## About

Cthulhu is a distributed login-cracker that can work on an endless (almost) number of clients. Cthulhu acts as
puppet-master which controls the clients and uses them to carry out a distributed login attack. All that is needed is
for Cthulhu's client software to be installed and Cthulhu will be able to connect to the client and use it in an attack.

Cthulhu is able to create bruteforce and dictionary lists of password.

## Usage
```python
import itertools

from src.bruteforce_generator import BruteforcePWGenerator, CharacterClass
from src.dictionary_generator import DictionaryPWGenerator


def use_bruteforce():
    BruteforcePWGenerator(4, 4, filename="hex_upper__4_4.txt", combinatoric_iterator=itertools.product).use_filewriter(
        [CharacterClass.DIGITS, CharacterClass.HEXDIGITS_UPPER]
    )
    bruteforce_map = BruteforcePWGenerator(1, 3, combinatoric_iterator=itertools.permutations).use_generator(["abc"])
    while 1:
        try:
            print(next(bruteforce_map))
        except StopIteration:
            break


def use_wordlist():
    DictionaryPWGenerator(filename="wl_common__4_4.txt").use_filewriter(
        (
            ["admin", "Admin", "@dmin", "adm1n", "Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
            ["123", "1234"],
            ["!", "!1", "*"],
        )
    )
    dictionary_map = DictionaryPWGenerator().use_generator(
        (
            ["København", "københavn", "Copenhagen", "copenhagen"],
            ["!", "!1", "*", "123", "2600", "2600!"],
        )
    )
    while 1:
        try:
            print(next(dictionary_map))
        except StopIteration:
            break


if __name__ == "__main__":
    use_bruteforce()
    use_wordlist()

```
# Goals
Support of:
 - Webform Authentication
 - SSH
 - FTP
# License

Not determined.

# DevNotes

`git commit --no-verify -m "match not supported by numpy, use this"`

`pre-commit run --all-files`

`pytest --cov`

`bandit -r my_sum`

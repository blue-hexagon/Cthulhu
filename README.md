# Cthulhu [WIP]

## About
Cthulhu is a project im currently developing that utilizes hosts to carry out distributed password cracking.

## Status
### Finished Features
- Can create bruteforce password lists saved as files or as a stream (with a generator)
  - Example: All combinations of lowercase alpha + numeric with length 6-10
  - Example: All hexcharacter combinations with length 8-12
- Can create word-list permutations saved as a file or used as a stream
- All itertools combinatoric iterators are supported, theese are:
  - [product](https://docs.python.org/3/library/itertools.html#itertools.product) (cartesian product) - this is what you most likely want to use
  - [permutations](https://docs.python.org/3/library/itertools.html#itertools.permutations)
  - [combinations](https://docs.python.org/3/library/itertools.html#itertools.combinations)
  - [combinations with replacement](https://docs.python.org/3/library/itertools.html#itertools.combinations_with_replacement)
- Object serialization/deserialization for packets in transit
- Simple form authentication attack
- SSH authentication attack

### Features in Progress
Currently working on the networking protocol and adding concurrency for the master node

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
# License
Undetermined.

import re

from src.bruteforce_generator import CharacterClass


def test_keyspace_constants():
    """Tests the character-class constants"""
    assert CharacterClass.WHITESPACE.isspace()
    assert CharacterClass.ASCII_LOWERCASE.islower()
    assert CharacterClass.ASCII_UPPERCASE.isupper()
    assert CharacterClass.ASCII_LETTERS.isalpha()
    assert CharacterClass.DIGITS.isdigit()
    assert bool(re.match(r"([^0-9a-f]+)", CharacterClass.HEXDIGITS_LOWER)) is False
    assert bool(re.match(r"([^0-9A-F]+)", CharacterClass.HEXDIGITS_UPPER)) is False
    assert bool(re.match(r"([^0-9a-fA-F]+)", CharacterClass.HEXDIGITS)) is False
    assert bool(re.match(r"([^0-7]+)", CharacterClass.OCTDIGITS)) is False
    assert bool(re.match(r"([0-9a-zA-Z])+", CharacterClass.PUNCTUATION)) is False
    assert bool(re.match(r"([\W]+)", CharacterClass.PRINTABLE)) is False

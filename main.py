from password_permuter import PasswordPermuter, CharacterClass

if __name__ == "__main__":
    PasswordPermuter(1, 3, "ascii_lower_and_octdigit__1_3.txt").use_filewriter(
        [
            CharacterClass.ASCII_LOWERCASE,
            CharacterClass.OCTDIGITS,
        ]
    )

    PasswordPermuter(4, 4, "hexdigits__4_4.txt").use_filewriter(["abcdefABCDEF0123456789"])
    # x = PasswordPermuter(4, 4).use_generator(
    #     (
    #         ["123"],
    #         [" "],
    #         ["!", "!1", "*"],
    #         ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
    #         ["admin", "Admin", "@dmin", "adm1n"],
    #     )
    # )
    # print(x)
    # try:
    #     while nxt := next(x):
    #         print(**nxt)
    # except StopIteration:
    #     print("---- Finished ----")

from password_permuter import PasswordPermuter

if __name__ == "__main__":
    # PasswordPermuter(1, 3, "lower_hexdigits__1_3.txt").run_filewriter(
    #     [
    #         CharacterClass.ASCII_LOWERCASE,
    #         CharacterClass.DIGITS,
    #     ]
    # )
    #
    # BruteforcePermuter(4, 4, "hexdigits__4_4.txt").run_filewriter(["abcdefABCDEF0123456789"])
    # dat = (  # TODO: Replace with `data` param, when program is finished.
    #
    # )
    # prods = BruteforcePermuter.get_shallow_product(dat)
    # print(prods)
    # PasswordPermuter(2,5,"hahah.txt").run_filewriter(prods)
    x = PasswordPermuter(4, 4).use_generator(
        (
            ["123"],
            [" "],
            ["!", "!1", "*"],
            ["Password", "password", "pa$$word", "Pa$$word", "p@$$w0rd"],
            ["admin", "Admin", "@dmin", "adm1n"],
        )
    )
    print(x)
    try:
        while nxt := next(x):
            print(**nxt)
    except StopIteration:
        print("---- Finished ----")

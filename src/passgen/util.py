import secrets

from src.passgen.char_class import CodePage


def generate_password() -> str:
    LENGTH = 32  # noqa. Default password length
    return "".join(secrets.choice(CodePage.CONTEXT_SAFE_CODEPAGE) for _ in range(LENGTH))

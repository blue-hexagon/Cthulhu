import http.client
import string
import threading
from enum import Enum
from typing import Tuple

import numpy as np


class AuthMethod(Enum):
    SIMPLE_FORM_METHOD = 0
    COMPLEX_FORM_AUTH = 1
    BASIC_HTTP_OR_NTLM_AUTH = 2
    MFA_OR_CAPTCHA_AUTH = 3


class WebAuthBruteforcer:
    def __init__(
        self,
        endpoint: str,
        target_host: str,
        target_port: int,
        username: Tuple[str | None, str | None] = None,
        email: Tuple[str | None, str | None] = None,
        password: Tuple[str | None, str | None] = None,
        auth_method: Enum = None,
    ):
        self.endpoint = endpoint
        self.target_host = target_host
        self.target_port = target_port
        self.username_name = username[0]
        self.username_val = username[1]
        self.email_name = email[0]
        self.email_val = email[1]
        self.password_name = password[0]
        self.password_val = password[1]
        self.perms_array = list(set(string.printable))
        self.auth_method = auth_method
        # MAX_THREADS = 100

        """ This determines the max amount of threads that the bruteforcer will run """
        if len(self.perms_array) > 100:
            self.perms_array = np.array_split(self.perms_array, 100)
        else:
            """Fallback for testing the program with single characters"""
            self.perms_array = np.array_split(self.perms_array, len(self.perms_array))

    def deploy_bruteforcer_threads(self) -> None:
        for perm_subset in self.perms_array:
            thread = threading.Thread(target=self.bruteforcer, args=[perm_subset])
            thread.start()

    def bruteforcer(self, perm_subset) -> None:
        for perm in perm_subset:
            # if b"auth_token" in data:
            # print("Found Token -> " + data.decode("utf-8"))
            # return
            ...

    def simple_form_auth(self):
        conn = http.client.HTTPSConnection(self.target_host)
        if self.username_val:
            payload = f"{self.username_name}={self.username_val}&{self.password_name}={self.password_val}"
        elif self.email_val:
            payload = f"{self.email_name}={self.email_val}&{self.password_name}={self.password_val}"
        else:
            raise KeyError("Missing email or username.")
        headers = {
            "Cache-Control": "no-cache",
            "Host": f"{self.target_host}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": len(payload),
        }
        conn.request(method="POST", url=f"{self.endpoint}", body=payload, headers=headers)
        res = conn.getresponse()
        data = res.read().decode()
        print(res.msg, res.version, res.status, res.reason, data)
        conn.close()

    def run(self) -> None:
        match self.auth_method:  # mypy: ignore
            case AuthMethod.SIMPLE_FORM_METHOD:
                self.simple_form_auth()
            case AuthMethod.COMPLEX_FORM_AUTH:
                raise NotImplementedError("Todo")
            case AuthMethod.MFA_OR_CAPTCHA_AUTH:
                raise NotImplementedError("Todo")
            case AuthMethod.BASIC_HTTP_OR_NTLM_AUTH:
                raise NotImplementedError("Todo")
            case _:
                raise KeyError("Authentication method not recognized.")


if __name__ == "__main__":
    # bruteforcer = RestAuthPasswordBruteforcer(
    #     endpoint="/auth/token/login/",
    #     target_ip="127.0.0.1",
    #     target_port=8000,
    #     username="dj",
    # )
    # bruteforcer.deploy_bruteforcer_threads()
    form_model = {"username": None, "email": "simpleForm@authenticationtest.com", "password": "pa$$w0rd"}
    bruteforcer = WebAuthBruteforcer(
        target_host="authenticationtest.com",
        endpoint="/login/?mode=simpleFormAuth",
        target_port=443,
        auth_method=AuthMethod.SIMPLE_FORM_METHOD,
        username=("username", None),
        email=("email", "simpleForm@authenticationtest.com"),
        password=("password", "pa$$w0rd"),
    )
    bruteforcer.run()

import random


def generate_random_string(length=lambda: random.randint(1, 1000)):
    """Generate a random string of given length."""
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length())).encode()
class Server():


    while True:
        try:
            data = s.recv(100)
            print(f"Server recieved: {data.decode()}")
            s.sendall(generate_random_string())
            time.sleep(1)
        except KeyboardInterrupt:
            exit(0)


class Client():


    while True:
        try:
            self.s.sendall(generate_random_string())
            data = self.s.recv(100)
            print(f"Client recieved: {data.decode()}")
            sleep(1)
        except KeyboardInterrupt:
            exit(0)
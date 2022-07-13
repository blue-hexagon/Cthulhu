# The Python Socket Library

## Sockets 101

Under any circumstance when you wish to work with sockets there is a few steps applicable to any project you undertake which you must take in order to accomplish socket communication.

*This guide doesn't go into full details about the socket library - it mainly concern TCP.*

*This guide assumes you have a basic understanding of packets, the workings of TCP and IP addressing.*

### Create a Socket Object

- Creating a socket is described below.
    - `s=socket.socket(socket.X, socket.Y)` - `s` is the returned socket object.
    - X must be: `AF_INET`
    - Y must be either: `SOCK_STREAM` or `SOCK_DGRAM`

1. Hence, to create a TCP socket you would use `s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
2. Hence, to create a UDP socket you would use `s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`

---

#### State of Our Program (0)

```python
import socket
import sys

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = "127.0.0.1"
    PORT = 1060

    if sys.argv[1:] == ["server"]:
        ...

    elif sys.argv[1:] == ["client"]:
        ...
    else:
        print("Usage: tcp.py server|client")
```

### Bind an Address to The Server Socket

Next up we must tell the server which IP address and port number to bind on. You are free to use eihter IPv4 or IPv6 addresses.

This involves the bind command: `s.bind((HOST, PORT))`<sup>(1)</sup> which binds the socket to the address specified in the two-tuple `(HOST,PORT)`.

<small>(1): Notice the extra set of parenthesis on `s.bind`. `s.bind()` takes a tuple as an argument; tuples are enclosed in an outer pair of parentheses.</small>

### Instruct The Server to Listen for Connections

Now we have created a socket object and told the socket object it's address and port - now we must instruct the socket to set itself up listening for connections.
This is done by the `listen` method on a sokcet object.

`listen()` enables the server to accept connections. `listen` can have an argument that specifies a queue-size for unaccepted connections. When the queue is full,
the system will refuse any more connections until the queued connections is below size of the queue once again.

The argument can either be omitted and it will use a default of 5, or it can be any int greater than or equal to 0.


#### State of Our Program (1)

```python
from datetime import datetime
import socket
import sys

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = "127.0.0.1"
    PORT = 1060


    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')


    def log(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')


    if sys.argv[1:] == ["server"]:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            sc, sockname = s.accept()

    elif sys.argv[1:] == ["client"]:
        ...
    else:
        print("Usage: tcp.py server|client")
```

#### Instruct The Client to Connect to The Server

`s.connect((HOST, PORT))`

#### Setup a Logger and Message Formatter
Next up we will add some logging capabilities. We will construct
Lastly, in the code below we are adding to `print_recv(...)` which is a message formatter that adds a time stamp, a sender and the reciever as a prefix to each message.
Similarly we'll add a `log(...)` for loging messages on both the client and the server.

It'll look something like this when we use it later:

```python
''' # Remove ticks, they are here temporaily because IDE formatting breaks up the strings
# log(...)
[10:53:16 – Node]: Client has been assigned socket name ('127.0.0.1', 4472)

# print_recv(...)
[10:53:19 – Client -> Server]:
Hello server!
'''

```

#### State of Our Program (2)

```python
from datetime import datetime
import socket
import sys

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = "127.0.0.1"
    PORT = 1060


    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')


    def log(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')


    if sys.argv[1:] == ["server"]:
        s.bind((HOST, PORT))
        s.listen()

    elif sys.argv[1:] == ["client"]:
        s.connect((HOST, PORT))
        log("Node", f"Client has been assigned socket name {s.getsockname()}")
    else:
        print("Usage: tcp.py server|client")
```

.
.
.
.

.

.

.

Example of a client-server program utilizing the `socket.makefile(..)` call.

- The `makefile` call lets us treat a socket as a fileobject.
    - This has the implication that you don't need to calculate the message size for each TCP packet you send across the wires. Or in the case of a fixed-length packetsize you aren't
      constrained by.. a fixed packetsize.

```python
import socket
import sys
from datetime import datetime
from time import sleep

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = sys.argv.pop() if len(sys.argv) == 3 else "127.0.0.1"
    PORT = 1060


    def print_recv(transmitter, reciever, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {transmitter} -> {reciever}]:\n{msg}')


    def print_host(host, msg):
        print(f'[{datetime.now().strftime("%H:%M:%S")} – {host}]: {msg}')


    def send(fd, cmd):
        fd.writelines(cmd + "\n")
        fd.flush()


    def read(fd) -> str:
        msg = fd.readline()
        return msg


    if sys.argv[1:] == ["server"]:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            print_host("Server", f"Listening at {s.getsockname()}")
            sc, sockname = s.accept()
            frw = sc.makefile('rw')

            print_host("Server", f"Accepted a connection from {sockname}")
            print_host("Server", f"Socket connects {sc.getsockname()} and {sc.getpeername()}")
            while True:
                print_recv(sc.getpeername(), "Server", reply := read(frw))
                send(frw, "Hello Node!")
                if reply in ['STOP', ""]:
                    frw.close()
                    frw.close()

    elif sys.argv[1:] == ["client"]:
        s.connect((HOST, PORT))
        frw = s.makefile('rw')
        print_host("Node", f"Client has been assigned socket name {s.getsockname()}")
        while True:
            send(frw, "Hello server!")
            print_recv(s.getpeername(), "Node", reply := read(frw))
            if reply == 'STOP':
                s.close()
            sleep(1)

    else:
        print(f"Usage: tcp_stream_as_a_fileobject.py server|client [host]")

```

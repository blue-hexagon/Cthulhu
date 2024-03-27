import socket

from src.net.protocol.ops import (
    CthulhuEndsSubjectConnection,
    CthulhuInstructsSubjectAboutAttackProtocol,
    CthulhuInstructsSubjectToSleepBetweenAuthAttempts,
    CthulhuTellsNodeToStopAuthAttack,
    CthulhuTellsSubjectToAttack,
    MakeAnyRepeatNextCommands,
    MakeAnySleepForDuration,
    SubjectAsksCthulhuForPasswords,
)
from src.net.tcp.socket import TcpSocket
from src.net.util import Utils


class TCPServer(TcpSocket):
    """Server code goes here"""

    def __init__(self, host: str, port: int, timeout=0) -> None:
        self.repeat: int = -1
        self.next_n_commands: int = -1
        self.pw_cache_limit: int = -1
        self.fire_attack_delay: int = -1
        self.stop_attack: bool = False
        super().__init__(host, port, timeout, server=True, client=False)
        while True:
            s: socket.socket = self.accept_incoming_connection()
            while True:
                try:
                    frame_sequence = TcpSocket.recv_all(s)
                except EOFError:
                    break
                # self.fprint(self.peername(host), frame_sequence)
                for frame in frame_sequence.frames:
                    op = frame.operation
                    op_type = type(frame.operation)
                    if op_type is MakeAnyRepeatNextCommands:
                        self.repeat = op.repeat
                        self.next_n_commands = op.next_n_commands
                        self.narrator.debug(f"Repeat {self.repeat} times the next {self.next_n_commands} commands.")

                    elif op_type is SubjectAsksCthulhuForPasswords:
                        self.pw_cache_limit = op.amount
                        self.narrator.debug(f"Password cache set to {self.pw_cache_limit}.")

                    elif op_type is CthulhuTellsSubjectToAttack:
                        self.fire_attack_delay = Utils.get_ms_delay(op.delay)
                        self.narrator.debug(f"Fire delay set to {op.delay}.")

                    elif op_type is CthulhuTellsNodeToStopAuthAttack:
                        self.stop_attack_delay = Utils.get_ms_delay(op.delay)
                        self.narrator.debug(f"Stop delay set to {op.delay}.")

                    elif op_type is MakeAnySleepForDuration:
                        self.narrator.info(f"Instructed to sleep for {op.delay}")

                    elif op_type is CthulhuInstructsSubjectToSleepBetweenAuthAttempts:
                        print("hit")

                    elif op_type is CthulhuInstructsSubjectAboutAttackProtocol:
                        print("hit")

                    elif op_type is CthulhuEndsSubjectConnection:
                        print("hit")

                    else:
                        self.narrator.error(f"Protocol operation not recognized. Ignoring: {op}.")
            s.close()

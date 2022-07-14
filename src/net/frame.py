import random
import time
from typing import List

from protocol_operation import (
    NodeFireAuthAttack,
    NodeRecievePasswords,
    NodeSetAuthProtocol,
    NodeSetSleep,
    NodeSleepBetweenAuthAttempts,
    NodeStopAuthAttack,
    ProtocolOperation,
    RepeatNextCommands,
)


class MessageIDHandler:
    def __init__(self) -> None:
        random.seed(time.time_ns())
        self.message_id = random.randint(1, 1000000000)
        self.sequence = 0

    def __next__(self) -> int:
        self.sequence += 1
        if self.sequence % 2 == 0:
            self.message_id += 1
        return self.message_id

    def __iter__(self):
        return self


class Frame:
    def __init__(self, operation: ProtocolOperation) -> None:
        self.message_id_handler = MessageIDHandler()
        self.operation = operation
        self.message_id = self.get_next_message_id()

    def get_next_message_id(self) -> int:
        return next(self.message_id_handler)

    def get_id(self) -> int:
        return self.message_id

    def get_operation(self) -> ProtocolOperation:
        return self.operation

    def __repr__(self) -> str:
        return f"Frame(message_id='{self.get_next_message_id()}', operation={repr(self.operation)}))"


class FrameSequence:
    def __init__(self, *frames: Frame) -> None:
        self.message_handler = MessageIDHandler()
        self.frames: List[Frame] = list(frames)

    def __repr__(self) -> List[str]:
        frames_representation = [(str(frame) + "\n") for frame in self.frames]
        return frames_representation


if __name__ == "__main__":
    packet_stream = FrameSequence(
        Frame(NodeSetSleep(time="3s")),
        Frame(NodeSetAuthProtocol(protocol="ssh")),
        Frame(RepeatNextCommands(repeat="5", next_n_commands="5")),
        Frame(NodeRecievePasswords(amount="25-100")),
        Frame(NodeFireAuthAttack(delay="10m")),
    )
    print(repr(packet_stream.frames))

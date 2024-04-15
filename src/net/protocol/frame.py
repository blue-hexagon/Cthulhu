import random
import time
from pprint import pprint
from typing import List

from src.net.protocol.operation import ProtocolOperation
from src.net.protocol.ops import (
    CthulhuInstructsSubjectAboutAttackProtocol,
    CthulhuTellsSubjectToAttack,
    MakeAnyRepeatNextCommands,
    MakeAnySleepForDuration,
    SubjectAsksCthulhuForPasswords,
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
    def __init__(self, *operations: ProtocolOperation) -> None:
        self.message_id_handler = MessageIDHandler()
        self.message_id = self.get_next_message_id()
        self.operations: List[ProtocolOperation] = list(operations)

    def get_next_message_id(self) -> int:
        return next(self.message_id_handler)

    def get_id(self) -> int:
        return self.message_id

    def get_operations(self) -> List[ProtocolOperation]:
        return self.operations

    def __repr__(self) -> str:
        return f"Frame(message_id='{self.get_next_message_id()}', operation={repr(self.operations)}))"


class FrameSequence:
    def __init__(self, *frames: Frame) -> None:
        self.message_handler = MessageIDHandler()
        self.frames: List[Frame] = list(frames)

    @property
    def frames_count(self):
        return len(self.frames)

    def __repr__(self) -> List[str]:
        frames_representation = [(str(frame) + "\n") for frame in self.frames]
        return frames_representation

    def __str__(self) -> str:
        return str(self.frames)


if __name__ == "__main__":
    packet_stream = FrameSequence(
        Frame(
            MakeAnySleepForDuration(time="3s"),
            MakeAnySleepForDuration(time="3s"),
        ),
        Frame(CthulhuInstructsSubjectAboutAttackProtocol(protocol="ssh")),
        Frame(MakeAnyRepeatNextCommands(repeat="5", next_n_commands="5")),
        Frame(SubjectAsksCthulhuForPasswords(amount="25-100")),
        Frame(CthulhuTellsSubjectToAttack(delay="10m")),
    )
    pprint(repr(packet_stream.frames))

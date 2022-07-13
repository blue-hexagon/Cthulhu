from dataclasses import dataclass

from protocol_operation import ProtocolOperation


class FrameSegment:
    def __init__(self, segment):
        self.segment_string = segment
        self.segment_length = len(segment)


@dataclass
class Frame:
    message_id: str
    operation: ProtocolOperation
    message: str

    def __len__(self):
        return len(self.message_id.encode("utf-8")) + len(repr(self.operation)) + len(self.message.encode("utf-8"))

    def get_id(self):
        return self.message_id

    def get_operation(self):
        return self.operation

    def get_message(self):
        return self.message

from dataclasses import dataclass


class FrameSegment:
    def __init__(self, segment):
        self.segment_string = segment
        self.segment_length = len(segment)


@dataclass
class Frame:
    frame_length: str
    message_id: str
    operation: str
    message: str

    def get_framelength(self):
        return self.frame_length

    def get_id(self):
        return self.message_id

    def get_operation(self):
        return self.operation

    def get_message(self):
        return self.message

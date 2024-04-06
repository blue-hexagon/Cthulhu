from dataclasses import dataclass, field
from typing import Any, Dict, List

import yaml

from src.conf.path_manager import PathManager
from src.net.protocol.frame import Frame, FrameSequence
from src.net.protocol.ops import OperationProxyFactory


@dataclass
class ProtocolOperation:
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.kwargs.items():
            setattr(self, key, value)


def load_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def yaml_to_dataclass(yaml_data):
    """
    This class uses the Frame and FrameSequence classes from src.net.protocol
    along with a ProxyFactory that creates ProtocolOperation subclasses.
    """
    ret_frames = []
    for frames in yaml_data["FrameSequence"]:
        operations = []
        for frame_list in frames.values():
            for frame in frame_list:
                operations.append(OperationProxyFactory(frame["ProtocolOperation"], *frame["args"]))
        ret_frames.append(Frame(operations))
    frame_sequence = FrameSequence(ret_frames)
    return frame_sequence


if __name__ == "__main__":
    frame_sequence_data = yaml_to_dataclass(load_yaml(PathManager().payload_profiles))
    for frame_sequence in frame_sequence_data:
        for frame in frame_sequence:
            for operation in frame.operations:
                print(f"Protocol Operation: {operation}")

from dataclasses import dataclass
from typing import Tuple, Any, Callable, List


@dataclass
class OperationResult:
    narrator: Callable
    narrative: str
    status: Tuple[int, str]
    change: List[Tuple[Callable, Any]] | None
    result: Any | None
    reply: List[Tuple[Callable, Any]] | None

    def narrate(self):
        self.narrator(self.narrative,self.status[0])

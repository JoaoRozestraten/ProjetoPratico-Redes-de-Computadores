from typing import Callable
from dataclasses import dataclass


@dataclass
class Monitor:
    cmd: str
    period: int
    next_time: float
    callback: Callable
    state: str = "PRONTO"

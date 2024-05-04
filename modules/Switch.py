# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

from .PC import PC
from .Coda import Coda
from .Frame import Frame

class Switch:
    def __init__(self, *args, buffer = "A") -> None:
        self.listaPC: list[PC] = list(args)
        self.buffer: Coda = buffer

    def __str__(self) -> str:
        string: str = "--- Switch ---\n"
        for pc in self.listaPC:
            string += f" - {pc}\n" 
        string += f"Buffer: {self.buffer}"
        return string

    def sendFrame(self, frame: Frame) -> None:
        self.buffer.push(frame)
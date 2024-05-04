# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

from .Coda import Coda

class PC:
    def __init__(self, id) -> None:
        self.id: str = id
        self.buffer: Coda = []

    def __str__(self) -> str:
        return f"PC {self.id} Buffer: {self.buffer}"
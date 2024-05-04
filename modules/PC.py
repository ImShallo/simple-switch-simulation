# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

from .Queue import Queue

class PC:
    def __init__(self, id):
        self.id: str = id
        self.buffer: Queue = []

    def __str__(self) -> str:
        return f"PC {self.id} Buffer: {self.buffer}"

    def receiveFrame(self, frame):
        self.buffer.append(frame)

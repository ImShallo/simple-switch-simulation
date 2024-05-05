# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

from __future__ import annotations
from typing import TYPE_CHECKING
from .Queue import Queue

if TYPE_CHECKING: # solve circular import
    from .Frame import Frame

class PC:
    def __init__(self, id):
        self.id: str = id
        self._buffer: Queue[Frame] = Queue()

    def __str__(self) -> str:
        
        return f"PC {self.id} Buffer: {self.buffer}"
    
    def receiveFrame(self, frame: Frame):
        self._buffer.append(frame)

    def totalFramesReceived(self) -> int:
        return self._buffer.lenght()

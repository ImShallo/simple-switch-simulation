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
        string = f"PC {self.id}"
        string += f"\n *Buffer size: {self._buffer.lenght()}"

        all_frames_type = self.get_frames_types()
        frame = self._buffer.peek()

        for priority, count in all_frames_type.items():
            string += f"\n *Frame {frame.PRIORITIES[priority]} (x{count})"

        if not all_frames_type:
            string += "Empty"

        return string
    
    def receiveFrame(self, frame: Frame):
        self._buffer.append(frame)

    def totalFramesReceived(self) -> int:
        return self._buffer.lenght()

    def get_frames_types(self) -> dict:
        all_frames_type = {}
        for frame in self._buffer:
            if frame.priority not in all_frames_type:
                all_frames_type[frame.priority] = 0
            all_frames_type[frame.priority] += 1

        return all_frames_type

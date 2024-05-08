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
        from .Frame import Frame

        string = f"PC {self.id}"
        string += f"\n *Buffer size: {len(self._buffer.lenght)}"

        all_frames_type = self.get_frames_type_count()

        for priority, count in all_frames_type.items():
            if count != 0:
                string += f"\n *Frame {Frame.PRIORITIES[priority]} (x{count})"

        if not all_frames_type:
            string += "Empty"

        return string
    
    def receiveFrame(self, frame: Frame):
        self._buffer.append(frame)

    def totalFramesReceived(self) -> int:
        return len(self._buffer)

    def get_frames_type_count(self) -> dict:
        from .Frame import Frame

        all_frames_type = {}

        for frame_type in Frame.PRIORITIES.keys():
            if frame_type not in all_frames_type:
                all_frames_type[frame_type] = 0

        for frame in self._buffer:
            all_frames_type[frame.priority] += 1

        return all_frames_type

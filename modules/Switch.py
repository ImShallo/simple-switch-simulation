# ----------------- # 
# Date: 04-05-2024
# Project: simple switch simulation
# ----------------- # 

from __future__ import annotations
from .PC import PC
from .Queue import Queue
from .Frame import Frame

class Switch:
    def __init__(self, *args, bufferSize = 100):
        self.listPCs: list[PC] = list(args)
        self._buffer: Queue[Frame] = Queue(int(bufferSize))
        self._bufferSizeHistory: list[int] = []

    def __str__(self) -> str:
        from .Frame import Frame

        string = "--- Switch ---\n"

        for pc in self.listPCs:
            string += f"- {pc}\n"
             
        string += f"Buffer size: {len(self._buffer)}\n"
        string += f"Buffer: "

        all_frames_type = self.get_frames_type_count()

        for priority, count in all_frames_type.items():
            if count != 0:
                string += f"\n *Frame {Frame.PRIORITIES[priority]} (x{count})"

        if not all_frames_type:
            string += "Empty"

        return string

    def add_to_buffer(self, frame: Frame):
        self._buffer.append(frame)

    def process_buffer(self) -> bool:
        if self._buffer.is_empty():
            return False
        
        self._sort_buffer()
        self._bufferSizeHistory.append(len(self._buffer))

        while not self._buffer.is_empty():
            frame = self._buffer.pop()
            frame.destination.receiveFrame(frame)
            
        return True
    
    def get_total_frames_processed(self) -> int:
        return sum(self._bufferSizeHistory)
    
    def calculate_buffer_average(self) -> float:
        average = self.get_total_frames_processed() / len(self._bufferSizeHistory)
        average = round(average, 2)

        return average if self._bufferSizeHistory else 0

    def connect_pc(self, pc: PC):
        self.listPCs.append(pc)

    def get_frames_type_count(self) -> dict:
        from .Frame import Frame

        all_frames_type = {}

        for frame_type in Frame.PRIORITIES.keys():
            if frame_type not in all_frames_type:
                all_frames_type[frame_type] = 0

        for frame in self._buffer:
            all_frames_type[frame.priority] += 1

        return all_frames_type

    def _sort_buffer(self) -> None:
        for i in range(len(self._buffer)):
            for j in range(i, len(self._buffer)):
                if self._buffer[i].priority < self._buffer[j].priority:
                    self._buffer[i], self._buffer[j] = self._buffer[j], self._buffer[i]
        
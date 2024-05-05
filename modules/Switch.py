# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

from .PC import PC
from .Queue import Queue
from .Frame import Frame

class Switch:
    def __init__(self, *args, bufferSize):
        self.listPCs: list[PC] = list(args)
        self._buffer: Queue[Frame] = Queue(int(bufferSize))
        self._bufferSizeHistory: list[int] = []

    def __str__(self) -> str:
        string: str = "--- Switch ---\n"
        for pc in self.listPCs:
            string += f"- {pc}\n" 
        string += f"Buffer size: {self._buffer.lenght()}\n"
        string += f"Buffer: "

        all_frames_type = self.get_frames_types()
        frame = self._buffer.peek()

        for priority, count in all_frames_type.items():
            string += f"\n | Frame {frame.PRIORITIES[priority]} (x{count})"

        if not all_frames_type:
            string += "Empty"

        return string

    def add_to_buffer(self, frame: Frame):
        self._buffer.append(frame)

    def process_buffer(self) -> bool:
        if self._buffer.is_empty():
            return False

        self._bufferSizeHistory.append(self._buffer.lenght())

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

    def get_frames_types(self) -> dict:
        all_frames_type = {}
        for frame in self._buffer:
            if frame.priority not in all_frames_type:
                all_frames_type[frame.priority] = 0
            all_frames_type[frame.priority] += 1

        return all_frames_type
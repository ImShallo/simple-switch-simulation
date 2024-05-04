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
            string += f" - {pc}\n" 
        string += f"Buffer size: {self._buffer.lenght()}\n"
        string += f"Buffer: "

        # * Possibile miglioramento per la formattazione #1 https://www.tldraw.com/r/fV9OGlrdxCvJ9nwrYMCEK?v=-4075,-1556,2187,1038&p=e4VFSbeoSGqjqzGHUQUVB
        for frame in self._buffer:
            string += f"\n\t| {frame}"

        return string

    def add_to_buffer(self, frame: Frame):
        self._buffer.append(frame)

    def process_buffer(self) -> bool:
        if self._buffer.is_empty():
            return False

        self._bufferSizeHistory.append(self._buffer.lenght())

        while not self._buffer.is_empty():
            # frame.destination.receiveFrame(frame) # * Da implementare
            self._buffer.pop()

        return True
    
    def get_total_frames_processed(self) -> int:
        return sum(self._bufferSizeHistory)
    
    def calculate_buffer_average(self) -> float:
        average = self.get_total_frames_processed() / len(self._bufferSizeHistory)
        average = round(average, 2)

        return average if self._bufferSizeHistory else 0
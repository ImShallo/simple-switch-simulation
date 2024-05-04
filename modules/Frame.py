# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

class Frame: 
    def __init__(self, destination, priority, processing_time) -> None:
        self.destination: int = destination
        self.priority: int = priority
        self.processing_time: float = processing_time

    def __str__(self) -> str:
        return f"Destination: {self.destination}, Priority: {self.priority}, Processing Time: {self.processing_time}"
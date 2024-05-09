# ----------------- # 
# Date: 04-05-2024
# Project: simple switch simulation
# ----------------- # 

from .PC import PC

class Frame: 
    PRIORITIES = {0: "Data", 1: "Video", 2: "Voice"}

    def __init__(self, destination, priority):
        self.destination: PC = self.set_destination(destination)
        self.priority: int = self.set_priority(priority)

    def __str__(self) -> str:
        return f"Frame: D-{self.destination.id}, P-{self.priority} ({self.PRIORITIES[self.priority]})"
    
    def set_priority(self, priority: int) -> int:
        if priority not in self.PRIORITIES:
            raise ValueError(f"Priority must be one of the following values: {list(self.PRIORITIES.keys())}")
        return priority

    def set_destination(self, destination: PC) -> PC:
        if not isinstance(destination, PC):
            raise ValueError("Destination must be a PC object")
        return destination
# ----------------- # 
# Date: 04-05-2024
# Project: undefined
# ----------------- # 

from .Queue import Queue

class PC:
    def __init__(self, id):
        self.id: str = id

    def __str__(self) -> str:
        return f"PC {self.id} Buffer: {self.buffer}"

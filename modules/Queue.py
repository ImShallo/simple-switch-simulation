# ----------------- # 
# Date: 04-05-2024
# Project: simple switch simulation
# ----------------- # 

class Queue:
    def __init__(self, max_size = None):
        self.items = []
        self.max_size = max_size
    
    def is_empty(self):
        return self.items == []
    
    def append(self, value) -> bool:
        if self.max_size is not None and len(self.items) >= self.max_size:
            raise Exception("<!> Coda piena")
        self.items.append(value)

    def pop(self):
        if self.is_empty():
            return "Coda vuota"
        return self.items.pop(0)

    def __str__(self):
        stringa = ""
        if self.is_empty():
            return "Coda vuota"
        
        for i in self.items:
            stringa += f"{i} -> "
    
        return stringa[:-3]

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)
    
    def __next__(self):
        return next(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def __setitem__(self, index, value):
        self.items[index] = value
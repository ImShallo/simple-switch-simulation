class Coda:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []
    
    def push(self, value):
        self.items.append(value)

    def pop(self):
        return self.items.pop(0)

    def __str__(self):
        stringa = ""
        if self.isEmpty():
            return "Coda vuota"
        
        for i in self.items:
            stringa += f"{i} -> "
    
        return stringa[:-3]

    def len(self):
        return len(self.items)

class Task():
    def __init__(self, name, x, y, color='blue', description='No description'):
        self.name = name
        self.completed = False
        self.color = color
        self.description = description
        self.x = x
        self.y = y
    
    def complete(self):
        self.completed = True
        print(f'{self.name} completed!')
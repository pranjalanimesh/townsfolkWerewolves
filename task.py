class Task():
    def __init__(self, name, color='blue', description='No description'):
        self.name = name
        self.completed = False
        self.color = color
        self.description = description
    
    def complete(self):
        self.completed = True
        print(f'{self.name} completed!')
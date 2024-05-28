import tkinter as tk
import random
from agent import Agent

class GameEnvironment:
    def __init__(self, master, rows=10, cols=10, size=50):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.size = size
        self.canvas = tk.Canvas(master, width=cols*size, height=rows*size)
        self.canvas.pack()
        self.agents = {}
        self.tasks = {'Task1': (8, 2), 'Task2': (9, 9)}
        self.draw_grid()
        self.master.after(1000, self.update_environment)  # Update every second

    def draw_grid(self):
        for i in range(self.rows + 1):
            self.canvas.create_line(0, i * self.size, self.cols * self.size, i * self.size)
        for j in range(self.cols + 1):
            self.canvas.create_line(j * self.size, 0, j * self.size, self.rows * self.size)

    def add_agent(self, agent, x, y):
        self.agents[agent.name] = (agent, x, y)
        self.draw_agent(agent, x, y)

    def add_task(self, task, x, y):
        self.tasks[task] = (x, y)
        self.draw_task(x, y)

    def move_agent(self, agent_name, new_x, new_y):
        agent, x, y = self.agents[agent_name]
        self.canvas.create_rectangle(x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size, fill="white")
        self.draw_agent(agent, new_x, new_y)
        self.agents[agent_name] = (agent, new_x, new_y)

    def draw_task(self, x, y):
        """Draws a task marker on the grid."""
        self.canvas.create_rectangle(x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size, fill='blue')
        self.canvas.create_text(x*self.size + self.size//2, y*self.size + self.size//2, text='Task', fill='white')

    def draw_agent(self, agent, x, y):
        self.canvas.create_rectangle(x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size, fill=agent.color)
        self.canvas.create_text(x*self.size+self.size//2, y*self.size+self.size//2, text=agent.name[0])

    def update_environment(self):
        # Updating the positions for the agents
        for agent_name, (agent, x, y) in self.agents.items():
            movement = agent.action(x, y)
            if movement:
                xNext, yNext = x + movement[0], y + movement[1]
                if(xNext<0):
                    xNext=0
                if(yNext<0):
                    yNext=0
                if(xNext>self.cols-1):
                    xNext=self.cols-1
                if(yNext>self.rows-1):
                    yNext=self.rows-1

                self.move_agent(agent_name, xNext, yNext)
        
        # Check if any agent has reached a task
        if any((x, y) in self.tasks.values() for (_, x, y) in self.agents.values()):
            print('Task completed!')

        # For each agent make them observe the next observations and happenings in the environment
        
        
    
        self.master.after(1000, self.update_environment)  # Schedule next update



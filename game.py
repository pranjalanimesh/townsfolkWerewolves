import tkinter as tk
import random
from agent import Agent
from task import Task
import numpy as np

class GameEnvironment:
    def __init__(self, master, rows=15, cols=15, size=50):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.size = size
        self.canvas = tk.Canvas(master, width=cols*size, height=rows*size)
        self.canvas.pack()
        self.agents = {}
        self.state = self.playground()
        self.tasks = {}
        self.draw_game()
        self.timestep = 2000
        self.master.after(self.timestep, self.update_environment)  # Update every timestep

    def playground(self):
        state = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            state[i][0] = '3'
            state[i][1] = '3'
            state[i][self.cols-1] = '3'
            state[i][self.cols-2] = '3'
        for j in range(self.cols):
            state[0][j] = '3'
            state[1][j] = '3'
            state[self.rows-1][j] = '3'
            state[self.rows-2][j] = '3'
        return state

    def add_agent(self, agent, x, y):
        self.agents[agent.name] = (agent, x, y)
        self.state[y][x] = '1' + agent.name  # '1' + first letter of agent name to distinguish from tasks '2`'
        print(f'Agent {agent.name} added at {x},{y}')
        self.draw_agent(agent, x, y)

    def add_task(self, task, x, y):
        self.tasks[task.name] = (task, x, y)
        self.state[y][x] = '2' + task.name # '2' + first letter of task name to distinguish from agents '1'
        print(f'Task {task.name} added at {x},{y}')
        self.draw_task(task,x, y)

    def draw_grid(self):
        for i in range(self.rows + 1):
            self.canvas.create_line(0, i * self.size, self.cols * self.size, i * self.size)
        for j in range(self.cols + 1):
            self.canvas.create_line(j * self.size, 0, j * self.size, self.rows * self.size)

    def draw_game(self):
        self.draw_grid()
        for row in range(self.rows):
            for col in range(self.cols):
                if self.state[row][col][0] == '1':
                    agent_name = self.state[row][col][1:]
                    self.draw_agent(self.agents[agent_name][0], col, row)

                elif self.state[row][col][0] == '2':
                    task_name = self.state[row][col][1:]
                    self.draw_task(self.tasks[task_name][0],col, row)

                elif self.state[row][col][0] == '3':
                    self.canvas.create_rectangle(col*self.size, row*self.size, (col+1)*self.size, (row+1)*self.size, fill="black")
                else:
                    self.canvas.create_rectangle(col*self.size, row*self.size, (col+1)*self.size, (row+1)*self.size, fill="white")

    def draw_task(self, task, x, y):
        """Draws a task marker on the grid."""
        self.canvas.create_rectangle(x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size, fill=task.color)
        self.canvas.create_text(x*self.size + self.size//2, y*self.size + self.size//2, text=task.name, fill='white')

    def draw_agent(self, agent, x, y):
        self.canvas.create_rectangle(x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size, fill=agent.color)
        self.canvas.create_text(x*self.size+self.size//2, y*self.size+self.size//2, text=agent.name[:2])

    # def observe(self):
    #     # Implement agent observation of the environment
    #     for agent_name, (agent, x, y) in self.agents.items():
    #         print(x,y)
    #         square = np.array(self.state)
    #         square = np.array(square[max(0, y-1):min(self.rows, y+2), max(0, x-1):min(self.cols, x+2)])
    #         print(f'{agent_name} observes: \n{square}')
    #         if(x==0):
    #             square = [['0' for _ in range(3)], agent[0], agent[1]]
    #             print("Wall on the west")
    #         if(y==0):
    #             print("Wall on north")
    #         if(x==self.cols-1):
    #             print("Wall on the east")
    #         if(y==self.rows-1):
    #             print("Wall at the south")

    # def move_agent(self, agent_name, new_x, new_y):
    #     agent, x, y = self.agents[agent_name]
    #     self.agents[agent_name] = (agent, new_x, new_y)
    #     state = self.initial_state

    #     for agent_name, (agent, x, y) in self.agents.items():
    #         state[y][x] = '1' + agent_name
    #     for task, (task, x, y) in self.tasks.items():
    #         state[y][x] = '2' + task.name
    #     self.state = state

    def move_agents(self):
        state = self.playground()
        for task, (task, x, y) in self.tasks.items():
            state[y][x] = '2' + task.name
        for agent_name, (agent, x, y) in self.agents.items():
            state[y][x] = '1' + agent_name
        self.state = state

    def vision_matrix(self, x, y, vision_range=1):
        # Implement agent observation of the environment
        square = np.array(self.state)
        square = np.array(square[max(0, y-vision_range):min(self.rows, y+vision_range+1), max(0, x-vision_range):min(self.cols, x+vision_range+1)])
        
        print(f'Agent at {x},{y} with vision range {vision_range} observes: \n{square}')
        return square

    def update_environment(self):
        # Updating the positions for the agents
        # Action needs threading to be implemented
        for agent_name, (agent, x, y) in self.agents.items():
            vision_matrix = self.vision_matrix(x, y, agent.vision_range)
            movement = agent.action(x, y, vision_matrix)
            if movement:
                xNext, yNext = x + movement[0], y + movement[1]
                if(xNext<2):
                    xNext=2
                if(yNext<2):
                    yNext=2
                if(xNext>self.cols-3):
                    xNext=self.cols-3
                if(yNext>self.rows-3):
                    yNext=self.rows-3
                self.agents[agent_name] = (agent, xNext, yNext)

        self.move_agents()

        self.draw_game()

        self.master.after(self.timestep , self.update_environment)  # Schedule next update



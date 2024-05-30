import tkinter as tk
import random
from agent import Agent
from task import Task
import numpy as np
from threading import Thread

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

    def add_agent(self, agent):
        self.agents[agent.name] = agent
        self.state[agent.y][agent.x] = '1' + agent.name  # '1' + first letter of agent name to distinguish from tasks '2`'
        print(f'Agent {agent.name} added at {agent.x},{agent.y}')
        self.draw_agent(agent)

    def add_task(self, task):
        self.tasks[task.name] = task
        self.state[task.y][task.x] = '2' + task.name # '2' + first letter of task name to distinguish from agents '1'
        print(f'Task {task.name} added at {task.x},{task.y}')
        self.draw_task(task)

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
                    self.draw_agent(self.agents[agent_name])

                elif self.state[row][col][0] == '2':
                    task_name = self.state[row][col][1:]
                    self.draw_task(self.tasks[task_name])

                elif self.state[row][col][0] == '3':
                    self.canvas.create_rectangle(col*self.size, row*self.size, (col+1)*self.size, (row+1)*self.size, fill="black")
                else:
                    self.canvas.create_rectangle(col*self.size, row*self.size, (col+1)*self.size, (row+1)*self.size, fill="white")

    def draw_task(self, task):
        """Draws a task marker on the grid."""
        self.canvas.create_rectangle(task.x*self.size, task.y*self.size, (task.x+1)*self.size, (task.y+1)*self.size, fill=task.color)
        self.canvas.create_text(task.x*self.size + self.size//2, task.y*self.size + self.size//2, text=task.name, fill='white')

    def draw_agent(self, agent):
        self.canvas.create_rectangle(agent.x*self.size, agent.y*self.size, (agent.x+1)*self.size, (agent.y+1)*self.size, fill=agent.color)
        self.canvas.create_text(agent.x*self.size+self.size//2, agent.y*self.size+self.size//2, text=agent.name[:2])

    def move_agents(self):
        print('Moving agents...')
        # Updating the positions for the agents simultaneously with multi-threading
        threads = []
        for agent_name, agent in self.agents.items():
            thread = Thread(target=self.act_agent, args=(agent_name,))
            threads.append(thread)
            thread.start()
            print(f'{agent_name} is moving...')
            
        for thread in threads:
            thread.join()
            print(f'{thread} joined...')

        # Updating the state of the game
        state = self.playground()
        for task_name, task in self.tasks.items():
            state[task.y][task.x] = '2' + task.name

        for agent_name, agent in self.agents.items():
            state[agent.y][agent.x] = '1' + agent_name
        self.state = state

    def act_agent(self, agent_name):
        agent= self.agents[agent_name]
        vision_matrix = self.vision_matrix(agent)
        movement = agent.action(vision_matrix, self.tasks)
        if movement:
            xNext, yNext = agent.x + movement[0], agent.y + movement[1]
            if(xNext<2):
                xNext=2
            if(yNext<2):
                yNext=2
            if(xNext>self.cols-3):
                xNext=self.cols-3
            if(yNext>self.rows-3):
                yNext=self.rows-3
            self.agents[agent_name].x = xNext
            self.agents[agent_name].y = yNext

    def vision_matrix(self, agent):
        # Implement agent observation of the environment
        square = np.array(self.state)
        square = np.array(square[max(0, agent.y-agent.vision_range):min(self.rows, agent.y+agent.vision_range+1), max(0, agent.x-agent.vision_range):min(self.cols, agent.x+agent.vision_range+1)])
        
        print(f'{agent.name} ({agent.role}) at {agent.x},{agent.y} with vision range {agent.vision_range} observes: \n{square}')
        return square

    def update_environment(self):

        self.move_agents()

        self.draw_game()

        self.master.after(self.timestep , self.update_environment)  # Schedule next update



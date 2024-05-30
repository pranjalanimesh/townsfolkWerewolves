import tkinter as tk
# import random
# from agent import Agent
# from task import Task
from PIL import Image, ImageTk
import numpy as np
from threading import Thread
from collections import deque


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
        self.num_agents = 0
        self.num_tasks = 0
        self.num_completed_tasks = 0
        self.directions = {(0, 1): 'down', (1, 0):'right', (0, -1):'up', (-1, 0):'left', (1, 1):'right down', (1, -1):'right up', (-1, 1):'left down', (-1, -1):'left up'}
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
        self.num_agents += 1
        self.draw_agent(agent)

    def add_task(self, task):
        self.tasks[task.name] = task
        self.state[task.y][task.x] = '2' + task.name # '2' + first letter of task name to distinguish from agents '1'
        print(f'Task {task.name} added at {task.x},{task.y}')
        self.num_tasks += 1
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
        self.canvas.create_image(agent.x*self.size, agent.y*self.size, anchor=tk.NW, image = agent.image)
        # self.canvas.create_rectangle(agent.x*self.size, agent.y*self.size, (agent.x+1)*self.size, (agent.y+1)*self.size, fill=agent.color)
        # self.canvas.create_text(agent.x*self.size+self.size//2, agent.y*self.size+self.size//2, text=agent.name[:2])
        self.canvas.create_text(agent.x*self.size+self.size//4 * 3, agent.y*self.size+self.size//4 * 3, text=agent.role[0].upper(),  fill='red' if agent.role == 'werewolf' else 'green')

    def move_agents(self):
        print('Moving agents...')
        # Updating the positions for the agents simultaneously with multi-threading
        threads = []
        for agent_name, agent in self.agents.items():
            thread = Thread(target=self.act_agent, args=(agent_name,))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()

        # Updating the state of the game
        state = self.playground()
        for task_name, task in self.tasks.items():
            state[task.y][task.x] = '2' + task.name

        for agent_name, agent in self.agents.items():
            state[agent.y][agent.x] = '1' + agent_name
        self.state = state

    def act_agent(self, agent_name):
        agent = self.agents[agent_name]
        task_chosen = agent.task_chosen

        # if no completed tasks, choose a task
        if self.num_completed_tasks == 0:
            if agent.task_chosen == 'explore':
                agent.choose_task(self.tasks)

        # task completion logic
        # There is no movement while completing a task 
        if task_chosen not in ['explore', 'hunt']:
            if self.tasks[task_chosen].x == agent.x and self.tasks[task_chosen].y == agent.y:
                if not self.tasks[task_chosen].completed:
                    self.tasks[task_chosen].complete()
                    agent.complete_task(task_chosen)
                    self.num_completed_tasks += 1
                    if self.num_completed_tasks == self.num_tasks:
                        print('All tasks completed!')
                        print('Game Over!')
                        print('Townsfolk Win!')
                        print('Exiting...')
                        self.master.quit()
                    return
                
                agent.record_memory(f'{task_chosen} is already completed')
                agent.choose_task(self.tasks)
                return

        vision_matrix = self.vision_matrix(agent)

        next_direction_for_task = None

        if(agent.role == 'townsfolk'):
            shortest_path_length, shortest_path = self.bfs_shortest_path_task(agent)
            next_step_for_task = (shortest_path[1][0]-shortest_path[0][0], shortest_path[1][1]-shortest_path[0][1])
            next_direction_for_task = self.directions[next_step_for_task]
        # The llm logic will be implemented here
        movement = agent.action(vision_matrix, self.tasks, next_direction_for_task)

        print(f'{agent.name} ({agent.role}) at {agent.x},{agent.y} chooses to move {movement}')
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

    def bfs_shortest_path_task(self, agent):

        start = (agent.x, agent.y)
        grid = self.state
        goal = (self.tasks[agent.task_chosen].x, self.tasks[agent.task_chosen].y)
        rows, cols = len(grid), len(grid[0])
        # Including diagonal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # right, down, left, up, and four diagonals

        queue = deque([(start, [start])])  # (current_position, path_to_current_position)
        visited = set()
        visited.add(start)

        while queue:
            (current_row, current_col), path = queue.popleft()

            # Check if we've reached the goal
            if (current_row, current_col) == goal:
                print(path)
                return len(path) - 1, path  # length of path and the path itself

            # Explore neighbors
            for dr, dc in directions:
                new_row, new_col = current_row + dr, current_col + dc
                new_pos = (new_row, new_col)
                if 2 <= new_row < rows-2 and 2 <= new_col < cols-2 and grid[new_row][new_col] != 3 and new_pos not in visited:
                    queue.append((new_pos, path + [new_pos]))
                    visited.add(new_pos)

        return None, []  # No path found

    def update_environment(self):

        self.move_agents()

        self.draw_game()

        self.master.after(self.timestep , self.update_environment)  # Schedule next update



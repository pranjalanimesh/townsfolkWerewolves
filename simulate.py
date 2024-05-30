import tkinter as tk
import random
from agent import Agent
from task import Task
from game import GameEnvironment

# Setting up the game
root = tk.Tk()
game = GameEnvironment(root)

# Adding agents
werewolf = Agent('Samarth', 2, 2, 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.')
townsfolk1 = Agent('Aditya', 5, 5, 'townsfolk', 'green','You start your day in the village, aware of the lurking danger of a hidden werewolf among you. Your goal is to work together with your fellow townsfolk to complete daily tasks and stay vigilant to any odd behavior, aiming to identify and eliminate the threat for the safety of the village')
townsfolk2 = Agent('Arun', 9, 10, 'townsfolk', 'green','You start your day in the village, aware of the lurking danger of a hidden werewolf among you. Your goal is to work together with your fellow townsfolk to complete daily tasks and stay vigilant to any odd behavior, aiming to identify and eliminate the threat for the safety of the village')

game.add_agent(werewolf)
game.add_agent(townsfolk1)
game.add_agent(townsfolk2)

# Adding tasks
task1 = Task('Task1', 8, 2, 'blue','You must collect the sacred herbs from the forest to prepare the antidote for the villagers.')
task2 = Task('Task2', 9, 9, 'blue','You must light the signal fire on the hilltop to alert the neighboring villages of the werewolf threat.')

game.add_task(task1)
game.add_task(task2)

root.mainloop()

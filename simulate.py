import tkinter as tk
import random
from agent import Agent
from task import Task
from game import GameEnvironment

# Setting up the game
root = tk.Tk()
game = GameEnvironment(root)

# Adding agents
werewolf = Agent('Samarth', 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.')
townsfolk1 = Agent('Aditya', 'townsfolk', 'green','You start your day in the village, aware of the lurking danger of a hidden werewolf among you. Your goal is to work together with your fellow townsfolk to complete daily tasks and stay vigilant to any odd behavior, aiming to identify and eliminate the threat for the safety of the village')
townsfolk2 = Agent('Arun', 'townsfolk', 'green','You start your day in the village, aware of the lurking danger of a hidden werewolf among you. Your goal is to work together with your fellow townsfolk to complete daily tasks and stay vigilant to any odd behavior, aiming to identify and eliminate the threat for the safety of the village')

game.add_agent(werewolf, 2, 2)
game.add_agent(townsfolk1, 5, 5)
game.add_agent(townsfolk2, 9, 10)

# Adding tasks
task1 = Task('Task1', 'blue','You must collect the sacred herbs from the forest to prepare the antidote for the villagers.')
task2 = Task('Task2', 'blue','You must light the signal fire on the hilltop to alert the neighboring villages of the werewolf threat.')

game.add_task(task1, 8, 2)
game.add_task(task2, 9, 9)

root.mainloop()

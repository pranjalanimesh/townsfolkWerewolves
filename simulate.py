import tkinter as tk
import random
from agent import Agent
from task import Task
from game import GameEnvironment

# Setting up the game
root = tk.Tk()
game = GameEnvironment(root)

# Adding agents
werewolf = Agent('Samarth', 2, 2, 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.',agent_image_path="./assets/samarth.png")

townsfolk1 = Agent('Aditya', 5, 5, 'townsfolk', 'green','You are the village healer, known for your knowledge of medicinal herbs and remedies. You are always ready to help those in need.',agent_image_path="./assets/aditya.png")

townsfolk2 = Agent('Arun', 9, 10, 'townsfolk', 'green','You are the village blacksmith, known for your skill in crafting weapons and tools. You are always ready to help your fellow villagers.',agent_image_path="./assets/arun.png")

game.add_agent(werewolf)
game.add_agent(townsfolk1)
game.add_agent(townsfolk2)

# Adding tasks
task1 = Task('Task1', 8, 2, 'blue','You must collect the sacred herbs from the forest to prepare the antidote for the villagers.')
task2 = Task('Task2', 9, 9, 'blue','You must forge a powerful weapon to protect the village from the werewolf.')
task3 = Task('Task3', 3, 8, 'blue','You must gather the rare minerals from the mines to strengthen the village defenses.')

game.add_task(task1)
game.add_task(task2)
game.add_task(task3)

root.mainloop()

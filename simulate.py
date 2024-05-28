import tkinter as tk
import random
from agent import Agent
from gameEnv import GameEnvironment

# Setting up the game
root = tk.Tk()
game = GameEnvironment(root)
werewolf = Agent('Werewolf', 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.')
townsfolk1 = Agent('Townsfolk1', 'townsfolk', 'green','You start your day in the village, aware of the lurking danger of a hidden werewolf among you. Your goal is to work together with your fellow townsfolk to complete daily tasks and stay vigilant to any odd behavior, aiming to identify and eliminate the threat for the safety of the village')
townsfolk2 = Agent('Townsfolk2', 'townsfolk', 'green','You start your day in the village, aware of the lurking danger of a hidden werewolf among you. Your goal is to work together with your fellow townsfolk to complete daily tasks and stay vigilant to any odd behavior, aiming to identify and eliminate the threat for the safety of the village')
game.add_agent(werewolf, 1, 1)
game.add_agent(townsfolk1, 5, 5)
game.add_agent(townsfolk2, 2, 8)
game.add_task('Task1', 8, 2)
game.add_task('Task2', 9, 9)
root.mainloop()

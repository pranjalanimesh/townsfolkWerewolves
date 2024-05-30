import openai
from datetime import datetime
import random
import json
from PIL import Image, ImageTk
from llm import model, completion

class Agent:
    def __init__(self, name, x, y,  role, color, initial_memory, agent_image_path):
        self.name = name
        self.role = role
        self.color = color
        self.x = x
        self.y = y
        self.memory = []
        self.initialize_memory(initial_memory)
        self.vision_range = 1
        self.task_chosen = 'explore'
        self.tasks_completed = []
        self.agent_image_path = agent_image_path
        self.image = self.load_and_resize_image(agent_image_path)
        if role == 'werewolf':
            self.vision_range = 2
            self.task_chosen = 'hunt'

    def initialize_memory(self, initial_memory):
        self.record_memory(initial_memory)

    def record_memory(self, event):
        self.memory.append({
            'timestamp': datetime.now().isoformat(),
            'event': event
        })
    
    def load_and_resize_image(self, image_path, width=50, height=50):
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    def retrieve_memory(self, query):
        # Implement retrieval based on relevance, recency, and importance
        # Simple example: Retrieve the most recent relevant memory
        relevant_memories = [m for m in self.memory if query.lower() in m['event'].lower()]
        if relevant_memories:
            return relevant_memories[-1]['event']  # Most recent
        return None

    def reflect(self):
        # Process memories to make high-level inferences
        # Example: Use GPT to summarize or infer from memories
        last_memory = self.memory[-1] if self.memory else None
        prompt= f"Reflect on this situation: {last_memory['event']}"
        if last_memory:
            
            completion =self.apiCall(prompt)
            return completion.to_dict()["choices"][0]["message"]["content"]
        return None

    def plan(self, reflection):
        prompt = f"Given that {reflection}, what should I do next as a {self.role}?"
        
        completion =self.apiCall(prompt)
        return completion.to_dict()["choices"][0]["message"]["content"]

    def apiCall(self, messages, acceptable_responses=None, max_tokens=50, temperature=0.5):
        result = ''
        if (acceptable_responses):
            if(len(acceptable_responses)>0):
                while(result.strip() not in acceptable_responses):
                    messages['system'] += f"Acceptable responses: '" + "', '".join(acceptable_responses) + "'"
                    messages['system'] += "\nDO NOT output anything else than the values given"

                    result = completion(messages, max_tokens=max_tokens, temperature=temperature)
                    # print(f"response: {result.strip().lower()}")
                    print(f"api response: {result.strip()}")
                return result.strip()

        response = completion(messages, max_tokens=max_tokens, temperature=temperature)

        return response
    
    def action(self, vision_matrix, tasks=None, next_direction_for_task=None):
        # Implement agent behavior based on role and environment
        if self.role == 'werewolf':
            return self.werewolf_action(vision_matrix, tasks)
        elif self.role == 'townsfolk':
            return self.townsfolk_action(vision_matrix, tasks, next_direction_for_task)
        else:
            return (0, 0)
        
    def werewolf_action(self,vision_matrix, tasks):
        system_prompt = f"You are playing a game. You are a werewolve in a townsfolk and werewolves game.  Use logical reasoning and give logical response to the situations."

        # vision_matrix = ((json.dumps(vision_matrix.__str__()).replace("], ", "]\n")).replace("[","")).replace("]","").replace('"','')

        nl_vision = self.vision_to_nl_range1(vision_matrix, tasks)

        print(f"nl_vision for {self.name} ({self.role}): \n{nl_vision}")

        user_prompt = f"Werewolves have to catch the townfolks and eliminate them. Werewolves has to catch all the townfolks to win the game. You can see the things below: \n{nl_vision} \n. Think critically step by step to decide your next move"

        acceptable_responses = ['up', 'down', 'left', 'right']

        messages = {}

        messages['user'] = user_prompt
        messages['system'] = system_prompt + ' Think step by step and then only give the response. Dont assume anything'

        # print(f"Prompt by {self.name} \n",messages)

        movement_discussion = self.apiCall(messages, max_tokens=200, temperature=0.0)
        # print(movement_discussion)

        messages['user'] += f"Discussion on the movement: \n{movement_discussion}, where should you move next?"
        movement = self.apiCall(messages,acceptable_responses, max_tokens=100, temperature=0.0)

        dir = [0, 0]
        if 'up' in movement.lower():
            dir[1] = -1
        if 'down' in movement.lower():
            dir[1] = 1
        if 'left' in movement.lower():
            dir[0] = -1
        if 'right' in movement.lower():
            dir[0] = 1

        return dir
        
        # Implement werewolf behavior
        # return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    
    def townsfolk_action(self, vision_matrix, tasks, next_direction_for_task):
        task_name = tasks[self.task_chosen].name if self.task_chosen != 'explore' else None
        task_info = ''
        if task_name:
            task_info += f'You have to complete the task {task_name} at x={tasks[self.task_chosen].x} and y={tasks[self.task_chosen].y}'

        system_prompt = f"You are playing a game. You are a townfolk character in a townsfolk and werewolves game. Use logical reasoning and give logical response to the situations."

        # vision_matrix = ((json.dumps(vision_matrix.__str__()).replace("], ", "]\n")).replace("[","")).replace("]","").replace('"','')

        nl_vision = self.vision_to_nl_range1(vision_matrix, tasks)

        print(f"nl_vision for {self.name}: \n{nl_vision}")

        user_prompt = f"Townsfolk have to complete tasks to win the game and find the werewolf. You can see the things below: \n{nl_vision} \n. You can move in the direction '{next_direction_for_task}' to move towards the task with shortest path. Think critically step by step to decide your next move"

        # acceptable_responses = ['up', 'down', 'left', 'right']

        messages = {}

        messages['user'] = user_prompt
        messages['system'] = system_prompt + ' Think step by step.'

        # print(f"Prompt by {self.name} \n",messages)

        movement_discussion = self.apiCall(messages, max_tokens=200, temperature=0.0)
        # print(movement_discussion)

        messages['user'] += f"Discussion on the movement: {movement_discussion}, where should you move next?"
        messages['system'] = system_prompt + 'Given the discussion on the movement, where should you move next? Only ouput in terms of directions up down left right. Do not output anything else. Example: "up", "down", "left", "right", "up right", "down left" "up left" "down right". Do not output anything else.'

        movement = self.apiCall(messages, max_tokens=100, temperature=0.0)

        dir = [0, 0]
        if 'up' in movement.lower() and 'down' not in movement.lower():
            dir[1] = -1
        if 'down' in movement.lower() and 'up' not in movement.lower():
            dir[1] = 1
        if 'left' in movement.lower() and 'right' not in movement.lower():
            dir[0] = -1
        if 'right' in movement.lower() and 'left' not in movement.lower():
            dir[0] = 1

        return dir
    
    def complete_task(self, task_name):
        self.tasks_completed.append(task_name)
        print(f'{self.name} completed {task_name}!')

    def choose_task(self, tasks):
        # Implement task selection based on role and environment
        if self.role == 'werewolf':
            self.task_chosen = 'hunt'
            return
        elif self.role == 'townsfolk':
            self.task_chosen = self.choose_townsfolk_task(tasks)
            return
        else:
            return 'explore'

    def choose_townsfolk_task(self, tasks):
        available_tasks = [task for task_name, task in tasks.items() if task.completed == False]
        
        # Implement task selection logic for townsfolk
        query = f"What should be the next task for {self.name}? Expecting one task from the following:\n" + "\n".join([f"{task.name} at x={task.x} and y={task.y} with description {task.description}" for task in available_tasks])

        context = f"Imagine yourself as {self.name} a townsfolk character in a hypothetical game.\n Important information : {self.memory[0]}. Which task best matches?"

        messages = {}
        messages['user'] = query
        messages['system'] = context

        task_chosen = self.apiCall(messages, acceptable_responses=[task.name for task in available_tasks], max_tokens=100, temperature=0.0)

        print(f'{self.name} chose {task_chosen}!')
        return task_chosen

    def vision_to_nl_range1(self, vision_matrix, tasks):
        # Implement conversion of vision matrix to natural language description
        
        # Werewolves see a 5x5 matrix
        # Townsfolk see a 3x3 matrix
        # The matrix is centered around the agent

        num_players = 0
        num_tasks = 0
        coords_to_direction = {
            (0, -1): 'up',
            (0, 1): 'down',
            (-1, 0): 'left',
            (1, 0): 'right',
            (0, 0): 'center',
            (1,1): 'right down',
            (1,-1): 'right up',
            (-1,1): 'left down',
            (-1,-1): 'left up',
            (0,2): 'down down',
            (0,-2): 'up up',
            (2,0): 'right right',
            (-2,0): 'left left',
            (1,2): 'right down down',
            (1,-2): 'right up up',
            (-1,2): 'left down down',
            (-1,-2): 'left up up',
            (2,1): 'right right down',
            (2,-1): 'right right up',
            (-2,1): 'left left down',
            (-2,-1): 'left left up',
        }

        nl_description = ''

        player_description = ''
        for y, row in enumerate(vision_matrix):
            for x, cell in enumerate(row):
                if x==self.vision_range and y==self.vision_range:
                    continue
                if cell[0] == '1':
                    player_description += f'You can see {cell[1:]} at {coords_to_direction[(x-self.vision_range,y-self.vision_range)]}.\n'
                    num_players += 1
        nl_description += f'You can see {num_players} players in your vision.\n'
        if player_description!='':
            nl_description += f"{player_description}\n"


        task_description = ''
        if self.role == 'werewolf':
            task_description += 'You are a werewolf. Your goal is to catch the townsfolk alone.\n'
            task_description += 'You can destroy the task progress by going to a completed task location.\n'
            task_description += 'You can wait at an incomplete task location for a townsfolk.\n'

        elif self.role == 'townsfolk':
            task_description += 'You are a townsfolk. Your goal is to complete the tasks.\n'

        for y, row in enumerate(vision_matrix):
            for x, cell in enumerate(row):
                if cell[0] == '2':
                    num_tasks += 1
                    task = tasks[cell[1:]]
                    if task.completed:
                        task_description += f'A completed {task.name} at {coords_to_direction[(x-self.vision_range,y-self.vision_range)]}.\n'
                    else:
                        if task.name == self.task_chosen:
                            task_description += f'Your current task {task.name} is at {coords_to_direction[(x-self.vision_range,y-self.vision_range)]}\n'
                        else:
                            task_description += f'An incomplete {task.name} at {coords_to_direction[(x-self.vision_range,y-self.vision_range)]}.\n'
        nl_description += f'You can see {num_tasks} tasks in your vision.\n{task_description}\n'

        wall_description = ''
        if self.vision_range == 1:
            if all([x == '3' for x in vision_matrix[0]]):
                wall_description += 'There is a wall on your upside.\n'
            if all([x == '3' for x in vision_matrix[2]]):
                wall_description += 'There is a wall on your downside.\n'
            if all([vision_matrix[i][0]=='3' for i in range(3)]):
                wall_description += 'There is a wall on your left side.\n'
            if all([vision_matrix[i][2]=='3' for i in range(3)]):
                wall_description += 'There is a wall on your right side.\n'

        if self.vision_range == 2:
            if all([x == '3' for x in vision_matrix[1]]):
                wall_description += 'There is a wall on your upside.\n'
            elif all([x == '3' for x in vision_matrix[0]]):
                wall_description += 'There is a wall on your upside at a distance 1.\n'

            if all([x == '3' for x in vision_matrix[3]]):
                wall_description += 'There is a wall on your downside.\n'
            elif all([x == '3' for x in vision_matrix[4]]):
                wall_description += 'There is a wall on your downside at distance 1.\n'

            if all([vision_matrix[i][1]=='3' for i in range(5)]):
                wall_description += 'There is a wall on your left side.\n'
            elif all([vision_matrix[i][0]=='3' for i in range(5)]):
                wall_description += 'There is a wall on your left side at a distance of 1.\n'
            
            if all([vision_matrix[i][3]=='3' for i in range(5)]):
                wall_description += 'There is a wall on your right side.\n'
            elif all([vision_matrix[i][4]=='3' for i in range(5)]):
                wall_description += 'There is a wall on your right side at a distance of 1.\n'
        nl_description += wall_description

        return nl_description
        

if __name__ == "__main__":
    a = Agent('Samarth', 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.')
    print('lkjdflkjdj')
    print(a.apiCall(
        {
            'user': 'Sun rises in west?',
            'system': ''
        }, acceptable_responses=['Correct', 'Incorrect'], max_tokens=100, temperature=0.0, 
    ))
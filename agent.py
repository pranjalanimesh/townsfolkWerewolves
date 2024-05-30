import openai
from datetime import datetime
import random
import json
from llm import model, completion

class Agent:
    def __init__(self, name, x, y,  role, color, initial_memory):
        self.name = name
        self.role = role
        self.color = color
        self.x = x
        self.y = y
        self.memory = []
        self.position = (random.randint(0, 9), random.randint(0, 9))
        self.initialize_memory(initial_memory)
        self.client = model
        self.vision_range = 1
        if role == 'werewolf':
            self.vision_range = 2

    def initialize_memory(self, initial_memory):
        self.record_memory(initial_memory)

    def record_memory(self, event):
        self.memory.append({
            'timestamp': datetime.now().isoformat(),
            'event': event
        })

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
                while(result.strip().lower() not in acceptable_responses):
                    messages['system'] += f"Acceptable responses: '" + "', '".join(acceptable_responses) + "'"
                    messages['system'] += "\nDO NOT output anything else than the values given"

                    result = completion(messages, max_tokens=max_tokens, temperature=temperature)
                    # print(f"response: {result.strip().lower()}")
                return result.strip().lower()

        response = completion(messages, max_tokens=max_tokens, temperature=temperature)

        return response
    
    def action(self, vision_matrix, tasks=None):
        # Implement agent behavior based on role and environment
        if self.role == 'werewolf':
            return self.werewolf_action(vision_matrix, tasks)
        elif self.role == 'townsfolk':
            return self.townsfolk_action(vision_matrix, tasks)
        else:
            return (0, 0)
        
    def werewolf_action(self,vision_matrix, tasks):
        system_prompt = f"You are playing a game. You are a character in a townsfolk and werewolves game.\nIn the environment \n0 means empty cell\n1[townfolk_name] means a townsfolk is there \n2[task_name] means a task which is to be completed\n3 means an obstacle Give to the point response to game situations."

        vision_matrix = ((json.dumps(vision_matrix.__str__()).replace("], ", "]\n")).replace("[","")).replace("]","").replace('"','')

        user_prompt = f"You are {self.name} and you are playing as a {self.role}. Werewolves have to catch townsfolk to win the game. You are in a 2d world. You can see a 5x5 matrix as an environment around you.You are in the center of vision matrix. \n You are at {self.x}, {self.y}.\nGiven the vision matrix as\n{vision_matrix}, analyse and think with directions up down left right and in step by step to find where should you move next"

        acceptable_responses = ['up', 'down', 'left', 'right']

        messages = {}

        messages['user'] = user_prompt
        messages['system'] = system_prompt

        # print(f"Prompt by {self.name} \n",messages)

        movement_discussion = self.apiCall(messages, max_tokens=200, temperature=0.0)
        # print(movement_discussion)

        messages['user'] += f"Discussion on the movement: \n{movement_discussion}, where should you move next?"
        movement = self.apiCall(messages,acceptable_responses, max_tokens=100, temperature=0.0)

        if movement=='up':
            return (0,-1)
        elif movement=='down':
            return (0,1)
        elif movement=='left':
            return (-1,0)
        elif movement=='right':
            return (1,0)
        else:
            return (0,0)
        
        # Implement werewolf behavior
        # return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    
    def townsfolk_action(self, vision_matrix, tasks):
        task_info = ''

        for task_name, task in tasks.items():
            task_info += f'{task.name} at {task.x}, {task.y}\n'

        system_prompt = f"You are playing a game. You are a character in a townsfolk and werewolves game.Townsfolk need to explore the environment to find the werewolves and complete the tasks. \nIn the environment \n0 means empty cell\n1[townfolk_name] means a townsfolk is there \n2[task_name] means a task which is to be completed\n3 means an obstacle.\n Give to the point response to game situations."

        vision_matrix = ((json.dumps(vision_matrix.__str__()).replace("], ", "]\n")).replace("[","")).replace("]","").replace('"','')

        user_prompt = f"You are {self.name} and you are playing as a {self.role}. Townsfolk have to complete tasks to win the game. You are in a 2d world. You can see a 3x3 matrix as an environment around you. You are in the center of vision matrix. \n You are at {self.x}, {self.y}. y increases when we go down and x increases when we go right. The tasks are \n{task_info}\nGiven the vision matrix as\n{vision_matrix}, analyse and think with directions up down left right and in step by step to find where should you move next"

        acceptable_responses = ['up', 'down', 'left', 'right']

        messages = {}

        messages['user'] = user_prompt
        messages['system'] = system_prompt

        # print(f"Prompt by {self.name} \n",messages)

        movement_discussion = self.apiCall(messages, max_tokens=200, temperature=0.0)
        # print(movement_discussion)

        messages['user'] += f"Discussion on the movement: {movement_discussion}, where should you move next?"
        movement = self.apiCall(messages,acceptable_responses, max_tokens=100, temperature=0.0)

        if movement=='up':
            return (0,-1)
        elif movement=='down':
            return (0,1)
        elif movement=='left':
            return (-1,0)
        elif movement=='right':
            return (1,0)
        else:
            return (0,0)
        # Implement townsfolk behavior
        # return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    
if __name__ == "__main__":
    a = Agent('Samarth', 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.')
    print('lkjdflkjdj')
    print(a.apiCall(
        {
            'user': 'Sun rises in west?',
            'system': ''
        }, acceptable_responses=['Correct', 'Incorrect'], max_tokens=100, temperature=0.0, 
    ))
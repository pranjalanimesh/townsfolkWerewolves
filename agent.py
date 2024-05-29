import openai
from datetime import datetime
import random
import json
from llm import model, completion

class Agent:
    def __init__(self, name,role,color, initial_memory):
        self.name = name
        self.role = role
        self.color = color
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
        if (acceptable_responses):
            messages['system'] += f"""
            Acceptable responses: '
            """ + "', '".join(acceptable_responses) + "'"
            messages['system'] += "\nDO NOT output anything else than the values given"

        response = completion(messages, max_tokens=max_tokens, temperature=temperature)

        return response
    
    def action(self, x, y, vision_matrix):
        # Implement agent behavior based on role and environment
        if self.role == 'werewolf':
            return self.werewolf_action(x, y, vision_matrix)
        elif self.role == 'townsfolk':
            return self.townsfolk_action(x, y, vision_matrix)
        else:
            return (0, 0)
        
    def werewolf_action(self, x, y, vision_matrix):
        system_prompt = f"In a townsfolk and werewolves game situation, give to the point response to query."

        user_prompt = f"You are {self.name} and you are playing as a {self.role}. Werewolves have to catch townsfolk alone to win the game. You are in a 2d world. You can see a 5x5 matrix in the environment Given the vision matrix {vision_matrix}, what should I do next as a {self.role}?"
        # Implement werewolf behavior
        return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    
    def townsfolk_action(self, x, y, vision_matrix):
        # Implement townsfolk behavior
        return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    
if __name__ == "__main__":
    a = Agent('Samarth', 'werewolf', 'red','You awaken under the pale moonlight, your senses sharper than ever. You recall your mission: to blend in with the townsfolk during the day and covertly eliminate them one by one at night. You must be cautious, as getting discovered could lead to your downfall.')
    print('lkjdflkjdj')
    print(a.apiCall(
        {
            'user': 'Sun rises in west?',
            'system': ''
        }, acceptable_responses=['Correct', 'Incorrect'], max_tokens=100, temperature=0.0, 
    ))
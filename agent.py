from datetime import datetime
import random

class Agent:
    def __init__(self, name,role,color, initial_memory):
        self.name = name
        self.role = role
        self.color = color
        self.memory = []
        self.position = (random.randint(0, 9), random.randint(0, 9))
        self.initialize_memory(initial_memory)

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

    def apiCall(self, prompt):
        completion = self.client.chat.completions.create(
            model="GPT35-turboA",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion
    
    def action(self, x, y):
        # Implement agent behavior based on role and environment
        if self.role == 'werewolf':
            return self.werewolf_action(x, y)
        elif self.role == 'townsfolk':
            return self.townsfolk_action(x, y)
        else:
            return (0, 0)
        
    def werewolf_action(self, x, y):
        # Implement werewolf behavior
        return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    
    def townsfolk_action(self, x, y):
        # Implement townsfolk behavior
        return (random.choice([-1, 1, 0]), random.choice([-1, 1, 0]))
    

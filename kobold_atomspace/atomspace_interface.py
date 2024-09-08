import random
from collections import defaultdict

class AtomSpaceInterface:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def update_with_text(self, text):
        # In a real implementation, this would use NLP techniques to extract entities and relationships
        # For this example, we'll use a simple word-based approach
        words = text.lower().split()
        for word in words:
            if len(word) > 3:  # Only add words with more than 3 characters as nodes
                self.nodes.add(word)
        
        # Create edges between adjacent words
        for i in range(len(words) - 1):
            if len(words[i]) > 3 and len(words[i+1]) > 3:
                self.edges[words[i]].add(words[i+1])
                self.edges[words[i+1]].add(words[i])

    def get_context(self):
        # In a real implementation, this would query the AtomSpace for relevant context
        # For this example, we'll return a random selection of nodes
        return " ".join(random.sample(self.nodes, min(5, len(self.nodes))))

    def get_graph_data(self):
        nodes = [{"id": node} for node in self.nodes]
        links = []
        for source, targets in self.edges.items():
            for target in targets:
                links.append({"source": source, "target": target})
        
        return {"nodes": nodes, "links": links}

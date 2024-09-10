import random

class KoboldInterface:
    def __init__(self):
        # In a real implementation, you would initialize the KoboldAI model here
        pass

    def generate_text(self, prompt, context=None):
        # In a real implementation, this would use the KoboldAI model to generate text
        # For this example, we'll use a simple random text generator
        
        base_phrases = [
            "Once upon a time",
            "In a land far, far away",
            "It was a dark and stormy night",
            "The adventure began when",
            "Little did they know",
        ]
        
        actions = [
            "a brave hero embarked on a quest",
            "a mysterious stranger arrived in town",
            "an ancient prophecy was revealed",
            "a long-lost artifact was discovered",
            "two rival kingdoms went to war",
        ]
        
        if context:
            # Use the context to influence the generation
            context_words = context.split()
            if len(context_words) > 2:
                context_phrase = " ".join(random.sample(context_words, 2))
                actions.append(f"the {context_phrase} changed everything")
        
        beginning = random.choice(base_phrases)
        middle = random.choice(actions)
        end = f"And so, {prompt.lower()} became the central theme of the story."
        
        return f"{beginning}, {middle}. {end}"

    def generate_what_if(self, nodes):
        # In a real implementation, this would use the KoboldAI model to generate a what-if scenario
        # For this example, we'll use a simple random text generator
        
        what_if_templates = [
            "What if {concept1} and {concept2} were combined?",
            "Imagine a world where {concept1} replaced {concept2}.",
            "How would the story change if {concept1} never existed, but {concept2} was twice as powerful?",
            "What if the roles of {concept1} and {concept2} were reversed?",
            "In a parallel universe, {concept1} and {concept2} are mortal enemies. What happens next?",
        ]
        
        template = random.choice(what_if_templates)
        concept1, concept2 = random.sample(nodes, min(2, len(nodes)))
        
        what_if_scenario = template.format(concept1=concept1, concept2=concept2)
        
        return what_if_scenario

    def generate_creative_prompt(self, nodes):
        # In a real implementation, this would use the KoboldAI model to generate a creative prompt
        # For this example, we'll use a simple random text generator
        
        prompt_templates = [
            "Write a story where {concept1} and {concept2} interact in an unexpected way.",
            "Describe a world where {concept1} is the most valuable resource.",
            "Create a character who embodies the qualities of both {concept1} and {concept2}.",
            "Imagine a future technology that combines {concept1} and {concept2}.",
            "Write a dialogue between personified versions of {concept1} and {concept2}.",
        ]
        
        template = random.choice(prompt_templates)
        concept1, concept2 = random.sample(nodes, min(2, len(nodes)))
        
        creative_prompt = template.format(concept1=concept1, concept2=concept2)
        
        return creative_prompt

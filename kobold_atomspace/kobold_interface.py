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

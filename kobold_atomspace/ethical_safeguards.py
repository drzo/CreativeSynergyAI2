import re
from profanity_check import predict_prob
import joblib  # Import joblib directly

class EthicalSafeguards:
    def __init__(self):
        self.sensitive_topics = ['violence', 'hate speech', 'explicit content']
        self.ethical_guidelines = [
            "Respect for persons",
            "Beneficence",
            "Justice",
            "Non-maleficence"
        ]

    def check_content(self, text):
        # Check for profanity
        profanity_score = predict_prob([text])[0]
        
        # Check for sensitive topics
        sensitive_topic_found = any(topic in text.lower() for topic in self.sensitive_topics)
        
        # Check for potential personal information (e.g., email addresses, phone numbers)
        personal_info_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        personal_info_found = bool(re.search(personal_info_pattern, text))

        return {
            'is_appropriate': profanity_score < 0.5 and not sensitive_topic_found and not personal_info_found,
            'profanity_score': profanity_score,
            'sensitive_topic_found': sensitive_topic_found,
            'personal_info_found': personal_info_found
        }

    def apply_ethical_guidelines(self, text):
        # This is a simplified implementation. In a real-world scenario, 
        # you might use more sophisticated NLP techniques to ensure 
        # the generated content adheres to ethical guidelines.
        guideline_adherence = all(guideline.lower() in text.lower() for guideline in self.ethical_guidelines)
        return guideline_adherence

    def moderate_content(self, text):
        content_check = self.check_content(text)
        ethical_check = self.apply_ethical_guidelines(text)

        if not content_check['is_appropriate']:
            return False, "Content violates moderation guidelines."
        elif not ethical_check:
            return False, "Content does not adhere to ethical guidelines."
        else:
            return True, "Content is appropriate and adheres to ethical guidelines."

document.addEventListener('DOMContentLoaded', () => {
    const storyIdeaInput = document.getElementById('story-idea');
    const generateBtn = document.getElementById('generate-btn');
    const generatedText = document.getElementById('generated-text');

    generateBtn.addEventListener('click', async () => {
        const storyIdea = storyIdeaInput.value;
        if (!storyIdea) {
            alert('Please enter a story idea.');
            return;
        }

        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ story_idea: storyIdea }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate text');
            }

            const data = await response.json();
            generatedText.textContent = data.text;
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating text. Please try again.');
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        }
    });
});

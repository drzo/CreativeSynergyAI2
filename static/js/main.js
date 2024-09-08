document.addEventListener('DOMContentLoaded', () => {
    const storyIdeaInput = document.getElementById('story-idea');
    const generateBtn = document.getElementById('generate-btn');
    const generatedText = document.getElementById('generated-text');
    const startNodeInput = document.getElementById('start-node');
    const endNodeInput = document.getElementById('end-node');
    const stepsInput = document.getElementById('steps');
    const topNInput = document.getElementById('top-n');
    const maxDepthInput = document.getElementById('max-depth');
    const bidirectionalSearchBtn = document.getElementById('bidirectional-search-btn');
    const discoverComplexConnectionsBtn = document.getElementById('discover-complex-connections-btn');
    const findBridgingConceptsBtn = document.getElementById('find-bridging-concepts-btn');
    const findUnexpectedRelationshipsBtn = document.getElementById('find-unexpected-relationships-btn');
    const findDiversePathsBtn = document.getElementById('find-diverse-paths-btn');
    const concept1Input = document.getElementById('concept1');
    const concept2Input = document.getElementById('concept2');
    const analysisResult = document.getElementById('analysis-result');

    // ... (keep existing event listeners)

    findDiversePathsBtn.addEventListener('click', async () => {
        const startConcept = concept1Input.value;
        const endConcept = concept2Input.value;
        const numPaths = parseInt(topNInput.value) || 3;
        const maxDepth = parseInt(maxDepthInput.value) || 5;
        if (!startConcept || !endConcept) {
            alert('Please enter both start and end concepts.');
            return;
        }

        try {
            const response = await fetch('/find_diverse_paths', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_concept: startConcept,
                    end_concept: endConcept,
                    num_paths: numPaths,
                    max_depth: maxDepth
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to find diverse paths');
            }

            const data = await response.json();
            if (data.paths && data.paths.length > 0) {
                analysisResult.innerHTML = `
                    <h3>Diverse Paths</h3>
                    <p>Found ${data.paths.length} diverse paths between "${startConcept}" and "${endConcept}":</p>
                    <ul>
                        ${data.paths.map((path, index) => `
                            <li>
                                <strong>Path ${index + 1}:</strong> ${path.join(' -> ')}
                            </li>
                        `).join('')}
                    </ul>
                    <p>These paths represent different ways of connecting the two concepts, potentially revealing novel and unexpected relationships.</p>
                `;
            } else {
                analysisResult.innerHTML = `
                    <h3>No Diverse Paths Found</h3>
                    <p>No diverse paths were found between "${startConcept}" and "${endConcept}" within the specified depth.</p>
                `;
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while finding diverse paths. Please try again.');
        }
    });
});

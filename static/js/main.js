document.addEventListener('DOMContentLoaded', () => {
    const storyIdeaInput = document.getElementById('story-idea');
    const generateBtn = document.getElementById('generate-btn');
    const generatedText = document.getElementById('generated-text');
    const addNodeBtn = document.getElementById('add-node-btn');
    const addEdgeBtn = document.getElementById('add-edge-btn');
    const newNodeInput = document.getElementById('new-node-input');
    const newEdgeSource = document.getElementById('new-edge-source');
    const newEdgeTarget = document.getElementById('new-edge-target');
    const genreSelect = document.getElementById('genre-select');
    const toneSelect = document.getElementById('tone-select');
    const applyGuidanceBtn = document.getElementById('apply-guidance');

    let currentStoryIdea = '';

    generateBtn.addEventListener('click', () => generateStory(storyIdeaInput.value));

    addNodeBtn.addEventListener('click', async () => {
        const nodeName = newNodeInput.value.trim();
        if (nodeName) {
            try {
                const response = await fetch('/add_node', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ node: nodeName }),
                });

                if (!response.ok) {
                    throw new Error('Failed to add node');
                }

                alert('Node added successfully');
                newNodeInput.value = '';
                location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while adding the node. Please try again.');
            }
        } else {
            alert('Please enter a node name');
        }
    });

    addEdgeBtn.addEventListener('click', async () => {
        const source = newEdgeSource.value.trim();
        const target = newEdgeTarget.value.trim();
        if (source && target) {
            try {
                const response = await fetch('/add_edge', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ source, target }),
                });

                if (!response.ok) {
                    throw new Error('Failed to add edge');
                }

                alert('Edge added successfully');
                newEdgeSource.value = '';
                newEdgeTarget.value = '';
                location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while adding the edge. Please try again.');
            }
        } else {
            alert('Please enter both source and target node names');
        }
    });

    document.addEventListener('nodeSelected', (event) => {
        const selectedNode = event.detail;
        currentStoryIdea = `Tell a story about ${selectedNode.id}`;
        storyIdeaInput.value = currentStoryIdea;
    });

    document.addEventListener('linkSelected', (event) => {
        const selectedLink = event.detail;
        currentStoryIdea = `Tell a story that connects ${selectedLink.source.id} and ${selectedLink.target.id}`;
        storyIdeaInput.value = currentStoryIdea;
    });

    applyGuidanceBtn.addEventListener('click', () => {
        const genre = genreSelect.value;
        const tone = toneSelect.value;
        const guidedStoryIdea = `${currentStoryIdea} in the ${genre} genre with a ${tone} tone`;
        generateStory(guidedStoryIdea);
    });

    async function generateStory(prompt) {
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ story_idea: prompt }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate text');
            }

            const data = await response.json();
            generatedText.textContent = data.generated_text;
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating text. Please try again.');
        }
    }

    // Add graph analysis functionality
    const findConnectionsBtn = document.getElementById('find-connections-btn');
    const findPathBtn = document.getElementById('find-path-btn');
    const bidirectionalSearchBtn = document.getElementById('bidirectional-search-btn');
    const randomWalkBtn = document.getElementById('random-walk-btn');
    const importantNodesBtn = document.getElementById('important-nodes-btn');
    const discoverNovelConnectionsBtn = document.getElementById('discover-novel-connections-btn');
    const findDiversePathsBtn = document.getElementById('find-diverse-paths-btn');

    findConnectionsBtn.addEventListener('click', () => performGraphAnalysis('find_connections'));
    findPathBtn.addEventListener('click', () => performGraphAnalysis('find_path'));
    bidirectionalSearchBtn.addEventListener('click', () => performGraphAnalysis('bidirectional_search'));
    randomWalkBtn.addEventListener('click', () => performGraphAnalysis('random_walk'));
    importantNodesBtn.addEventListener('click', () => performGraphAnalysis('important_nodes'));
    discoverNovelConnectionsBtn.addEventListener('click', () => performGraphAnalysis('discover_novel_connections'));
    findDiversePathsBtn.addEventListener('click', () => performGraphAnalysis('find_diverse_paths'));

    async function performGraphAnalysis(analysisType) {
        const startNode = document.getElementById('start-node').value;
        const endNode = document.getElementById('end-node').value;
        const steps = document.getElementById('steps').value;
        const topN = document.getElementById('top-n').value;
        const concept1 = document.getElementById('concept1').value;
        const concept2 = document.getElementById('concept2').value;
        const maxDepth = document.getElementById('max-depth').value;

        try {
            const response = await fetch(`/graph_analysis/${analysisType}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    start_node: startNode,
                    end_node: endNode,
                    steps: steps,
                    top_n: topN,
                    concept1: concept1,
                    concept2: concept2,
                    max_depth: maxDepth
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to perform graph analysis');
            }

            const data = await response.json();
            document.getElementById('analysis-result').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while performing graph analysis. Please try again.');
        }
    }
});

// ... (keep existing code)

let selectedNodes = new Set();

function initializeGraph(data) {
    graphData = data;
    
    // ... (keep existing graph initialization code)

    // Update interactive buttons
    const interactiveControls = d3.select("#interactive-controls");

    interactiveControls.select("#generate-what-if-btn")
        .on("click", generateWhatIf);

    interactiveControls.select("#cluster-concepts-btn")
        .on("click", clusterConcepts);

    interactiveControls.select("#generate-story-path-btn")
        .on("click", generateStoryPath);

    interactiveControls.select("#generate-creative-prompt-btn")
        .on("click", generateCreativePrompt);

    // ... (keep existing time travel controls)

    // Update node click behavior
    node.on("click", nodeClicked);
}

function nodeClicked(event, d) {
    if (event.ctrlKey || event.metaKey) {
        if (selectedNodes.has(d)) {
            selectedNodes.delete(d);
            d3.select(this).attr("stroke", null);
        } else {
            selectedNodes.add(d);
            d3.select(this).attr("stroke", "red").attr("stroke-width", 2);
        }
    } else {
        selectedNodes.clear();
        node.attr("stroke", null);
        selectedNodes.add(d);
        d3.select(this).attr("stroke", "red").attr("stroke-width", 2);
    }
    updateInteractiveControls();
}

async function generateCreativePrompt() {
    if (selectedNodes.size < 1) {
        alert('Please select at least one node to generate a creative prompt.');
        return;
    }

    const nodeIds = Array.from(selectedNodes).map(n => n.id);
    try {
        const response = await fetch('/generate_creative_prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nodes: nodeIds })
        });

        if (!response.ok) throw new Error('Failed to generate creative prompt');

        const data = await response.json();
        displayGeneratedContent(data.creative_prompt);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while generating the creative prompt.');
    }
}

function updateInteractiveControls() {
    const whatIfBtn = d3.select("#generate-what-if-btn");
    const storyPathBtn = d3.select("#generate-story-path-btn");
    const creativePromptBtn = d3.select("#generate-creative-prompt-btn");

    whatIfBtn.property("disabled", selectedNodes.size < 2);
    storyPathBtn.property("disabled", selectedNodes.size < 2);
    creativePromptBtn.property("disabled", selectedNodes.size < 1);
}

function displayGeneratedContent(content) {
    const outputContainer = document.getElementById('generated-text');
    outputContainer.textContent = content;
}

// ... (keep the rest of the existing code)

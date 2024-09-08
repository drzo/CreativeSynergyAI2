from flask import Flask, render_template, request, jsonify
from kobold_atomspace import KoboldInterface, AtomSpaceInterface

app = Flask(__name__)

kobold = KoboldInterface()
atomspace = AtomSpaceInterface()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    story_idea = request.json['story_idea']
    
    # Generate text using KoboldAI
    generated_text = kobold.generate_text(story_idea)
    
    # Update AtomSpace with generated text
    atomspace.update_with_text(generated_text)
    
    # Query AtomSpace for context
    context = atomspace.get_context()
    
    # Generate text again with context
    final_text = kobold.generate_text(story_idea, context)
    
    return jsonify({'text': final_text})

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/graph_data')
def graph_data():
    return jsonify(atomspace.get_graph_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

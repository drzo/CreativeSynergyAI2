from flask import Flask, render_template, request, jsonify
from kobold_atomspace import KoboldInterface, AtomSpaceInterface

app = Flask(__name__)

kobold = KoboldInterface()
atomspace = AtomSpaceInterface()

# ... (keep existing routes)

@app.route('/find_diverse_paths', methods=['POST'])
def find_diverse_paths():
    start_concept = request.json['start_concept']
    end_concept = request.json['end_concept']
    num_paths = request.json.get('num_paths', 3)
    max_depth = request.json.get('max_depth', 5)
    paths = atomspace.find_diverse_paths(start_concept, end_concept, num_paths, max_depth)
    return jsonify({'paths': paths})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

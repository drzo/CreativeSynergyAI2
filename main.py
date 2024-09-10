from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
import os
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from kobold_atomspace import KoboldInterface, AtomSpaceInterface

kobold = KoboldInterface()
atomspace = AtomSpaceInterface()

# ... (keep existing routes and functions)

@app.route('/graph')
@login_required
def graph():
    nodes = atomspace.get_user_nodes(current_user.id)
    links = atomspace.get_user_edges(current_user.id)

    # Get the earliest and latest timestamps
    start_time = min(node['timestamp'] for node in nodes)
    end_time = max(node['timestamp'] for node in nodes + links)

    graph_data = {
        'nodes': nodes,
        'links': links,
        'start_time': start_time,
        'end_time': end_time
    }

    return render_template('graph.html', graph_data=graph_data)

@app.route('/generate_what_if', methods=['POST'])
@login_required
def generate_what_if():
    nodes = request.json['nodes']
    what_if_scenario = kobold.generate_what_if(nodes)
    return jsonify({'what_if_scenario': what_if_scenario})

@app.route('/cluster_concepts', methods=['POST'])
@login_required
def cluster_concepts():
    clusters = atomspace.cluster_user_concepts(current_user.id)
    return jsonify({'clusters': clusters})

@app.route('/generate_story_path', methods=['POST'])
@login_required
def generate_story_path():
    nodes = request.json['nodes']
    path, story = atomspace.generate_story_path(current_user.id, nodes)
    return jsonify({'path': path, 'story': story})

@app.route('/generate_creative_prompt', methods=['POST'])
@login_required
def generate_creative_prompt():
    nodes = request.json['nodes']
    creative_prompt = kobold.generate_creative_prompt(nodes)
    return jsonify({'creative_prompt': creative_prompt})

# ... (keep the rest of the existing code)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
import os
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up logging
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from kobold_atomspace import KoboldInterface, AtomSpaceInterface

kobold = KoboldInterface()
atomspace = AtomSpaceInterface()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info(f"Login route accessed. Method: {request.method}")
    app.logger.info(f"Current user authenticated: {current_user.is_authenticated}")
    
    if current_user.is_authenticated:
        app.logger.info(f"User already authenticated. Redirecting to personal_knowledge_space.")
        return redirect(url_for('personal_knowledge_space'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app.logger.info(f"Login attempt for user: {username}")
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            app.logger.info(f"User {username} logged in successfully")
            
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('personal_knowledge_space')
            
            app.logger.info(f"Redirecting to: {next_page}")
            return redirect(next_page)
        else:
            app.logger.warning(f"Failed login attempt for user {username}")
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    app.logger.info(f"User {current_user.username} accessed the index page")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    story_idea = request.json['story_idea']
    generated_text = kobold.generate_text(story_idea)
    atomspace.add_node(story_idea, current_user.id)
    atomspace.add_node(generated_text, current_user.id)
    atomspace.add_edge(story_idea, generated_text, current_user.id)
    return jsonify({'generated_text': generated_text})

@app.route('/find_diverse_paths', methods=['POST'])
@login_required
def find_diverse_paths():
    start_concept = request.json['start_concept']
    end_concept = request.json['end_concept']
    num_paths = request.json.get('num_paths', 3)
    max_depth = request.json.get('max_depth', 5)
    paths = atomspace.find_diverse_paths(start_concept, end_concept, current_user.id, num_paths, max_depth)
    return jsonify({'paths': paths})

@app.route('/graph')
@login_required
def graph():
    nodes = atomspace.get_user_nodes(current_user.id)
    edges = atomspace.get_user_edges(current_user.id)
    return render_template('graph.html', nodes=nodes, edges=edges)

@app.route('/graph_data')
@login_required
def graph_data():
    nodes = atomspace.get_user_nodes(current_user.id)
    edges = atomspace.get_user_edges(current_user.id)
    return jsonify({
        'nodes': [{'id': node, 'label': node} for node in nodes],
        'links': [{'source': source, 'target': target} for source, target in edges]
    })

@app.route('/personal_knowledge_space')
@login_required
def personal_knowledge_space():
    summary = atomspace.get_user_graph_summary(current_user.id)
    return render_template('personal_knowledge_space.html', summary=summary)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

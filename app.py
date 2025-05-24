from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure MongoDB Atlas - explicitly include database name in URI
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://99210041514:kareKARE@cluster0.8nxoygo.mongodb.net/conference_db?retryWrites=true&w=majority&appName=Cluster0")

# Make sure the database name is included in the URI
if "conference_db" not in mongo_uri:
    # Insert database name before query parameters
    if "?" in mongo_uri:
        parts = mongo_uri.split("?", 1)
        mongo_uri = f"{parts[0]}/conference_db?{parts[1]}"
    else:
        mongo_uri = f"{mongo_uri}/conference_db"

print(f"Connecting to MongoDB with URI: {mongo_uri.replace(mongo_uri.split('@')[0], '[CREDENTIALS HIDDEN]')}")

app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Collections
proceedings = mongo.db.proceedings
conference_state = mongo.db.conference_state

# Routes
@app.route('/')
def index():
    # Get conference state
    state = conference_state.find_one({"id": "main"})
    if not state:
        state = {"id": "main", "is_launched": False}
        conference_state.insert_one(state)
    
    # Get all proceedings
    all_proceedings = list(proceedings.find().sort("timestamp", -1))
    
    return render_template('index.html', state=state, proceedings=all_proceedings)

@app.route('/admin')
def admin():
    # Get conference state
    state = conference_state.find_one({"id": "main"})
    if not state:
        state = {"id": "main", "is_launched": False}
        conference_state.insert_one(state)
    
    # Get all proceedings
    all_proceedings = list(proceedings.find().sort("timestamp", -1))
    
    return render_template('admin.html', state=state, proceedings=all_proceedings)

@app.route('/launch', methods=['POST'])
def launch_conference():
    conference_state.update_one(
        {"id": "main"}, 
        {"$set": {"is_launched": True, "launched_at": datetime.now()}}
    )
    
    # If AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True})
    
    # Otherwise redirect to home page instead of admin
    return redirect(url_for('index'))

@app.route('/unlaunch', methods=['POST'])
def unlaunch_conference():
    conference_state.update_one(
        {"id": "main"}, 
        {"$set": {"is_launched": False, "unlaunched_at": datetime.now()}}
    )
    
    # If AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True})
    
    # Otherwise redirect back to admin
    return redirect(url_for('admin'))

@app.route('/add_proceeding', methods=['POST'])
def add_proceeding():
    title = request.form.get('title')
    content = request.form.get('content')
    author = request.form.get('author')
    
    proceedings.insert_one({
        "title": title,
        "content": content,
        "author": author,
        "timestamp": datetime.now()
    })
    
    return redirect(url_for('admin'))

@app.route('/api/proceedings')
def get_proceedings():
    # For auto-refresh functionality
    all_proceedings = list(proceedings.find().sort("timestamp", -1))
    # Convert ObjectId to string for JSON serialization
    for proc in all_proceedings:
        proc['_id'] = str(proc['_id'])
    
    return jsonify(all_proceedings)

@app.route('/api/state')
def get_state():
    # For checking if conference is launched
    state = conference_state.find_one({"id": "main"})
    if state:
        state['_id'] = str(state['_id'])
    else:
        state = {"id": "main", "is_launched": False}
    
    return jsonify(state)

@app.route('/launch-page')
def launch_page():
    # Get conference state
    state = conference_state.find_one({"id": "main"})
    if not state:
        state = {"id": "main", "is_launched": False}
        conference_state.insert_one(state)
    
    # If already launched, redirect to admin
    if state.get('is_launched', False):
        return redirect(url_for('admin'))
    
    return render_template('launch.html', state=state)

if __name__ == '__main__':
    # Use PORT environment variable for compatibility with Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
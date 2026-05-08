import os
import threading
import uuid
import asyncio
from flask import Flask, render_template, request, jsonify, send_from_directory
from main import run_pipeline

app = Flask(__name__)

# Configuration
OUTPUT_FOLDER = 'output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# In-memory task status storage
tasks = {}

def pipeline_worker(task_id, subreddit, ai_enabled, overrides):
    try:
        tasks[task_id]['status'] = 'processing'
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        video_path = loop.run_until_complete(run_pipeline(
            subreddit_override=subreddit, 
            ai_override=ai_enabled,
            **overrides
        ))
        loop.close()

        if video_path and os.path.exists(video_path):
            tasks[task_id]['status'] = 'completed'
            tasks[task_id]['video_url'] = f'/download/{os.path.basename(video_path)}'
        else:
            tasks[task_id]['status'] = 'failed'
            tasks[task_id]['error'] = 'Pipeline failed to generate video.'
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    subreddit = data.get('subreddit', 'AmItheAsshole')
    ai_enabled = data.get('ai_enabled', True)
    
    # Extract optional overrides
    overrides = {
        'reddit_client_id': data.get('reddit_client_id'),
        'reddit_client_secret': data.get('reddit_client_secret'),
        'reddit_user_agent': data.get('reddit_user_agent'),
        'openai_api_key': data.get('openai_api_key'),
        'instagram_username': data.get('instagram_username'),
        'instagram_password': data.get('instagram_password')
    }
    # Remove None values
    overrides = {k: v for k, v in overrides.items() if v}

    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'queued'}
    
    thread = threading.Thread(target=pipeline_worker, args=(task_id, subreddit, ai_enabled, overrides))
    thread.start()
    
    return jsonify({'success': True, 'task_id': task_id})

@app.route('/status/<task_id>')
def status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    # Bind to 0.0.0.0 for external access
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

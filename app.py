from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from datetime import datetime

app = Flask(__name__)
RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('audio_data')
    if not file:
        return jsonify({'error': 'No file received'}), 400

    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    filename = f"recording_{timestamp}{os.path.splitext(file.filename)[1] or '.webm'}"
    file.save(os.path.join(RECORDINGS_DIR, filename))
    return jsonify({'ok': True, 'filename': filename})

@app.route('/list')
def list_recordings():
    files = sorted(os.listdir(RECORDINGS_DIR), reverse=True)
    return jsonify(files)

@app.route('/recordings/<path:filename>')
def download(filename):
    return send_from_directory(RECORDINGS_DIR, filename, as_attachment=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 locally if PORT not set
    app.run(host="0.0.0.0", port=port)

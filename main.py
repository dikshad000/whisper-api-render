from flask import Flask, request, jsonify
import openai
import os
from werkzeug.utils import secure_filename
import tempfile

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Whisper + GPT API is live!"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        audio_file = open(temp.name, "rb")

        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return jsonify({'transcription': transcript['text']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

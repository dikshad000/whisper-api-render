from flask import Flask, request, jsonify
import openai
import os
import tempfile
import requests

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Whisper + GPT API is live!"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    if not data or 'mp4_url' not in data:
        return jsonify({'error': 'No mp4_url provided'}), 400

    mp4_url = data['mp4_url']

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            response = requests.get(mp4_url)
            temp_file.write(response.content)
            temp_file_path = temp_file.name
    except Exception as e:
        return jsonify({'error': f'Failed to download file: {str(e)}'}), 500

    with open(temp_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return jsonify({'transcription': transcript['text']})
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

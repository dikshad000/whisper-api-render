@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    print("📥 Incoming Request:", data)  # 👈 LOG input

    if not data or 'mp4_url' not in data:
        print("❌ Error: No mp4_url provided")
        return jsonify({'error': 'No mp4_url provided'}), 400

    mp4_url = data['mp4_url']
    print("🔗 Downloading from URL:", mp4_url)  # 👈 LOG URL

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            response = requests.get(mp4_url)
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        print("✅ File downloaded to:", temp_file_path)  # 👈 LOG success
    except Exception as e:
        print("❌ Download error:", str(e))
        return jsonify({'error': f'Failed to download file: {str(e)}'}), 500

    try:
        with open(temp_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print("✅ Transcription success")
    except Exception as e:
        print("❌ Transcription error:", str(e))
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

    return jsonify({'transcription': transcript['text']})

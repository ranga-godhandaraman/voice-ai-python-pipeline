#=================================
# Import Section
#=================================
from flask import Flask, request, jsonify, send_file
import whisper
from gtts import gTTS
import os
import uuid
#=================================
# Flask Initialization
#=================================

app = Flask(__name__)

#=================================
# Load Whisper model 
#=================================

model = whisper.load_model("base")

#=================================
# Setup-up Local Path
#=================================

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#=================================
#Route to Home
#=================================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Speech AI API!"})

#=================================
# Speech-to-Text API
#=================================
@app.route("/api/speech-to-text", methods=["POST"])
def speech_to_text():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.wav")
    audio_file.save(filename)

    try:
        result = model.transcribe(filename)
        text = result["text"]
        return jsonify({"transcription": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filename)  # Clean up

#=================================
# Text-to-Speech API
#=================================
@app.route("/api/text-to-speech", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        tts = gTTS(text)
        output_path = os.path.join(OUTPUT_FOLDER, f"{uuid.uuid4()}.mp3")
        tts.save(output_path)

        return send_file(output_path, mimetype="audio/mpeg", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/health")
def health():
    return "OK", 200

    
#=================================
# Script Initialization - main()
#=================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5040 ,debug= True)

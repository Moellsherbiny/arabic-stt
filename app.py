from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # تفعيل CORS

# إذا كنت تستخدم Vosk
from vosk import Model, KaldiRecognizer
model = Model("models/vosk-ar-mgb2-0.4")  # تأكد أن المسار صحيح

@app.route("/stt", methods=["POST"])
def speech_to_text():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400
    
    # حفظ الملف مؤقتًا
    file_path = "temp_audio.wav"
    file.save(file_path)
    
    # معالجة الصوت باستخدام Vosk
    recognizer = KaldiRecognizer(model, 16000)
    with open(file_path, "rb") as f:
        recognizer.AcceptWaveform(f.read())
    
    result = recognizer.FinalResult()
    os.remove(file_path)  # حذف الملف بعد الانتهاء
    
    return jsonify({"text": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
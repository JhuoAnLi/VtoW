from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    recognizer = sr.Recognizer()

    if "audio" not in request.files:
        return jsonify({"error": "未上傳"})

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "未選擇文件"})

    allowed_extensions = {"wav", "mp3"}
    if audio_file.filename.split(".")[-1].lower() not in allowed_extensions:
        return jsonify({"error": "無效的文件格式"})

    # 存檔的位置
    temp_audio_path = "temp_audio.wav"  # 應為絕對路徑
    audio_file.save(temp_audio_path)

    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="zh-TW")
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "無法識別語音"})


if __name__ == "__main__":
    app.run(debug=True)

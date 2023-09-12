from flask import Flask, render_template
import speech_recognition as sr

app = Flask(__name__)

r = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    with sr.Microphone() as source:
        print("請開始說話...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='zh-TW')
        return text
    except sr.UnknownValueError:
        return "無法辨識您的語音"
    except sr.RequestError as e:
        return "無法連線至Google語音辨識服務：{0}".format(e)

if __name__ == '__main__':
    app.run(debug=True) # debug mode

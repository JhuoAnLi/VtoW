from flask import Flask, render_template, request, jsonify

# from google.cloud import aiplatform_v1
# import vertexai
# from vertexai.language_models import TextGenerationModel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json  # Assuming the data sent is in JSON format
    # Process the data here
    print(data)
    result = {'message': 'Data received and processed successfully',
              'original_text': data['original_text'],
              'command': data['command'],              
              'new_text': process_command(data)
              }
    
    return jsonify(result)

def process_command(data):
    # Process the data here
    orignal_text = data['original_text']
    command = data['command']

    new_text = orignal_text
    if '清除' in command:
        new_text = ''
    else:
        new_text = orignal_text
    print(new_text)
    return new_text


def LLM_handling():
    # vertexai.init(project="robust-team-393105", location="us-central1")
    # parameters = {
    #     "candidate_count": 1,
    #     "max_output_tokens": 256,
    #     "temperature": 0.2,
    #     "top_p": 0.8,
    #     "top_k": 40
    # }
    # model = TextGenerationModel.from_pretrained("text-bison@001")
    # response = model.predict(
    #     """請根據指令句A，修改指令句B的句子，產生句子C。例子如下:

    # A: [刪除]你好嗎?
    # B: 你好嗎? 我很好
    # C: 我很好

    # A: 在文章後面[新增]我很好
    # B: 一段乍看之下像是文章，但仔細一瞧全無道理的文字組合。
    # C: 一段乍看之下像是文章我很好，但仔細一瞧全無道理的文字組合。

    # A: 在文字錄入比賽（打字比賽）中，最公平的比賽用文本就是隨機文本
    # B: 把公平[替換成]老公公
    # C: 在文字錄入比賽（打字比賽）中，最老公公的比賽用文本就是隨機文本

    # 則根據此A、B句，對應的句子C應為何?
    # A: 嘉義新港地震 氣象局研判因板塊擠壓無關梅山斷層 未來2週防規模4以上餘震
    # B: [刪除]氣象局
    # C:""",
    #     **parameters
    # )
    # print(f"Response from Model: {response.text}")
    pass


if __name__ == '__main__':
    # app.run(debug=True)
    LLM_handling()

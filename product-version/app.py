from flask import Flask, render_template, request, jsonify


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
    return 0



if __name__ == '__main__':
    app.run(debug=True)

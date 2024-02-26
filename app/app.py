from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    input_string = data.get('input_string', '')
    
    result = process(input_string)
    
    return jsonify({'result': result})

def process(input_string):
    return input_string

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    
    return "This is homepage, Navigate to http://127.0.0.1:5000/api to view data.jso"

@app.route('/api')
def get_data():
    
    with open('data.json', 'r') as datafile:
        data = json.load(datafile)

    return jsonify(data)


if __name__ == '__main__':

    app.run(debug=True)
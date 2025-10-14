from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
client = pymongo.MongoClient(mongo_url)

db = client.devopstuto

collection = db['flask-tuto']


app = Flask(__name__)

@app.route('/')
def home():

    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    print(current_time)

    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/time')
def time():
    current_time = datetime.now().strftime('%H:%M:%S')

    return current_time

@app.route('/submit', methods=['POST'])
def submit():

    formdata = dict(request.form)
    collection.insert_one(formdata)
    # fname = request.form.get('firstName')
    # lname = request.form.get('lastName')
    # mail = request.form.get('email')
    # phoneno = request.form.get('phone')
    #return 'Hello, ' + fname + ' ' + lname + ' Your Email: ' + mail + ' Your Phone No.: ' + phoneno
    
    return "Data stored Successfully..."

@app.route('/view')
def view():
    data = collection.find()

    data = list(data)

    for item in data:
        del item['_id']

        print(item)

    data = {
        'data': data
    }
        

    return data


# @app.route('/api')
# def name():

#     name = request.values.get('name')
#     age = request.values.get('age')

#     result = {
#         'name' : name,
#         'age' : age

#     }

#     return result

if __name__ == '__main__':

    app.run(debug=True)
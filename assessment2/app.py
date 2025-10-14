from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

app = Flask(__name__)

# Connect to MongoDB Atlas
try:
    mongo_url = os.getenv('MONGO_URL')
    client = pymongo.MongoClient(mongo_url)
    db = client.assessmentdb
    collection = db['flasktutorial']
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    collection = None


@app.route('/')
def home():
    """Main form page"""
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)


@app.route('/submit', methods=['POST'])
def submit():
    """Insert form data into MongoDB"""
    formdata = dict(request.form)
    try:
        if collection is not None:
            collection.insert_one(formdata)
            return redirect(url_for('success'))
        else:
            return render_template('index.html', error="Database not connected")
    except Exception as e:
        return render_template('index.html', error=f"Error inserting data: {e}")


@app.route('/success')
def success():
    """Success page"""
    return render_template('success.html')


@app.route('/view')
def view():
    """View all stored data from MongoDB"""
    try:
        if collection is not None:
            data = list(collection.find({}, {'_id': 0}))
            return render_template('view.html', data=data)
        else:
            return render_template('view.html', data=[], error="Database not connected")
    except Exception as e:
        return render_template('view.html', data=[], error=f"Error fetching data: {e}")


if __name__ == '__main__':
    app.run(debug=True)

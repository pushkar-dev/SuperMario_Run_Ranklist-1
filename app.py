from flask import Flask, render_template
from pandas import read_csv
from db_access import *

MAINTAINANCE=False

# making flask app
app = Flask(__name__)

def load_users(batch):
    user_details = []
    if (batch != 2019 and batch != 2020 and batch != 2021 and batch != 2018):
        details = db.show_data()
    else :
        details = db.show_yearwise(batch)
    for j in range(len(details)):
        user = {}
        user["s_no"] = j + 1
        user["name"] = details[j][0]
        user["roll_no"] = details[j][1]
        user["codeforces_handle"] = details[j][3]
        user["questions_solved"] = details[j][4]
        user["rating"] = details[j][5]
        user_details.append(user)
    return user_details

@app.route('/')
def home():
    if MAINTAINANCE:
        return render_template('maintainance.html')
    user_details=load_users(2000)
    return render_template('index.html', lists = user_details)

@app.route('/dev')
def dev():
    user_details=load_users()
    return render_template('index.html', lists = user_details)

@app.route('/<int:year>')
def batch(year):
    user_details=load_users(year)
    return render_template('index.html', lists = user_details)

if __name__ == '__main__':
    app.run(debug = False)
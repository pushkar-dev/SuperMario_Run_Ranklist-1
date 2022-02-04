from flask import Flask, render_template
from pandas import read_csv

MAINTAINANCE=False

# making flask app
app = Flask(__name__)

def load_users():
    data=read_csv('handles')
    user_details = []
    for i in range(len(data["Codeforces Handle"])):
        user = {}
        user["s_no"] = i + 1
        user["name"] = data["Name"][i]
        user["roll_no"] = data["Roll No."][i]
        user["codeforces_handle"] = data["Codeforces Handle"][i]
        user["questions_solved"] = data["Questions_Solved"][i]
        user["rating"] = data["ratings"][i]
        user_details.append(user)
    return user_details

@app.route('/')
def home():
    if MAINTAINANCE:
        return render_template('maintainance.html')
    user_details=load_users()
    return render_template('index.html', lists = user_details)

@app.route('/dev')
def dev():
    user_details=load_users()
    return render_template('index.html', lists = user_details)

if __name__ == '__main__':
    app.run(debug = False)
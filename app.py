from flask import Flask, redirect, render_template, request
from db_access import Database
import re
import requests
from datetime import datetime

MAINTAINANCE=False
TIME_STAMP = 1643913000
END_TIME = 1645813800
db=Database()

proxy = {
'http' : '',
'https' : ''
}

def validate(roll:str,name:str,handle:str)->bool:
    if len(roll)!=6:
        return False
    b1=(roll[0]=='B' and roll[1:].isnumeric() and len(roll)==6)
    b2=(len(name)>0)
    b3=(re.match("[a-zA-Z0-9_.-]+",handle) is not None)
    return b1 and b2 and b3

# making flask app
app = Flask(__name__)

def load_users(batch):
    user_details = []
    if (batch != 2019 and batch != 2020 and batch != 2021 and batch != 2018):
        details = db.show_data()
    else :
        details = db.show_yearwise(batch)
    k = 1
    for j in range(len(details)):
        if (j > 0):
            if (user_details[len(user_details) - 1]["codeforces_handle"] != details[j][3]):
                user = {}
                user["s_no"] = k
                user["name"] = details[j][0]
                user["roll_no"] = details[j][1]
                user["codeforces_handle"] = details[j][3]
                user["questions_solved"] = details[j][4]
                user["rating"] = details[j][5]
                user_details.append(user)
                k = k + 1
        else:
            user = {}
            user["s_no"] = k
            user["name"] = details[j][0]
            user["roll_no"] = details[j][1]
            user["codeforces_handle"] = details[j][3]
            user["questions_solved"] = details[j][4]
            user["rating"] = details[j][5]
            user_details.append(user)
            k = k + 1


    return user_details

@app.route('/', methods=['POST','GET'])
def home():
    if MAINTAINANCE:
        return render_template('maintainance.html')
    year = 2000
    if request.method=='POST':
        year = request.form['year']
    user_details=load_users(int(year))
    return render_template('index.html', lists = user_details)

@app.route('/dev')
def dev():
    user_details=load_users()
    return render_template('index.html', lists = user_details)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['Name']
        roll=request.form['Roll']
        handle=request.form['Handle']
        yr=int(request.form['Year'])

        if validate(roll,name,handle):
            if len(db.show(handle))!=0:
                render_template('Error_form.html')
            # try:
            url = "https://codeforces.com/api/user.info?handles="+handle
            r = requests.get(url, proxies=proxy)
            json_data = r. json()
            rating  = json_data["result"][0]["rating"]
            db.add_u(roll, name, handle, yr, rating)
            return render_template("Success.html")
            # except:
            #     return render_template("Error_form.html")
        else:
            return render_template('Error_form.html')
    else:
        return redirect('/') 
            
@app.route('/<user>')
def user_details(user):
    url = "https://codeforces.com/api/user.status?handle="+user+"&from=1&count=100000"
    r = requests.get(url, proxies=proxy)
    json_data = r. json()
    user_questions = []
    try:
        k = 1
        for j in range(len(json_data["result"])):
            try:

                rating_user = list(db.show(user)[0])[5]
                if (json_data["result"][j]["verdict"] == "OK" and 
                    json_data["result"][j]["problem"]["rating"] >= max (rating_user, 1200) and
                    json_data["result"][j]["creationTimeSeconds"]>=TIME_STAMP and
                    json_data["result"][j]["creationTimeSeconds"] <= END_TIME and
                    json_data["result"][j]["author"]["ghost"]==False):
                    que = {}
                    que["s_no"] = k
                    que["contest"] = json_data["result"][j]["problem"]["contestId"]
                    que["index"] = json_data["result"][j]["problem"]["index"]
                    que["submission"] = json_data["result"][j]["id"]
                    que["rating"] = json_data["result"][j]["problem"]["rating"]
                    que["name"] = json_data["result"][j]["problem"]["name"]
                    que["time"] = str(datetime.utcfromtimestamp(json_data["result"][j]["creationTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S'))
                    k += 1
                    user_questions.append(que)
                    render_template('user_questions.html', lists = user_questions)
                if (json_data["result"][j]["creationTimeSeconds"] < TIME_STAMP):
                    break
            except:
                pass
    except:
        pass
    return render_template('user_questions.html', lists = user_questions, user = user)


if __name__ == '__main__':
    app.run(debug = True)
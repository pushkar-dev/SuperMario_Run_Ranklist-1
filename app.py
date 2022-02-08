from flask import Flask, redirect, render_template, request
from db_access import Database
import re
import requests

MAINTAINANCE=False
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
            


if __name__ == '__main__':
    app.run(debug = True)
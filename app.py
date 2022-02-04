from flask import Flask, render_template
from pandas import read_csv

MAINTAINANCE=False

<<<<<<< HEAD
# counting the number of Questions for a particular user
def helper(r, i):
    count = 0
    json_data = r. json()
    try:
        for j in range(len(json_data["result"])):
            try:
                if (json_data["result"][j]["verdict"] == "OK" and 
                    json_data["result"][j]["problem"]["rating"] >= max (data['ratings'][i], 1200)):
                    count += 1
            except:
                pass
    except:
        pass
    return count
=======
>>>>>>> 3c7f0ad394a5d923eb777e5e91a7c33117f96a83
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
<<<<<<< HEAD
    # Scheduler #2
    scheduler.add_job(id = 'Scheduled Task', func = update_sheet, trigger="interval", seconds = 300)
    scheduler.start()
    # running the app
    app.run(debug = True)
=======
    app.run(debug = False)
>>>>>>> 3c7f0ad394a5d923eb777e5e91a7c33117f96a83

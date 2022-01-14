import atexit
from flask_apscheduler import APScheduler
from flask import Flask, render_template
import pandas
import requests as re

proxy = {
'http' : '',
'https' : ''
}
# reading the existing data
data = pandas.read_csv("handles")

# counting the number of Questions for a particular user
def helper(r, i):
    count = 0
    json_data = r. json()
    try:
        for j in range(len(json_data["result"])):
            try:
                if (json_data["result"][j]["verdict"] == "OK" and 
                    json_data["result"][j]["problem"]["rating"] >= max (data['ratings'][i], 1000)):
                    count += 1
            except:
                pass
    except:
        pass
    return count
# making flask app
app = Flask(__name__)

#schedule #1
scheduler = APScheduler()
def update_sheet():
    for i in range(len(data["Name"])):
        url = "https://codeforces.com/api/user.status?handle="+data["Codeforces Handle"][i]+"&from=1&count=100000"
        r = re.get(url, proxies=proxy)
        data['Questions_Solved'][i] = helper(r, i)
        d = data.sort_values('Questions_Solved', ascending= False)
        d.to_csv('handles', index = False)
        print(i)

@app.route('/')
def home():
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

    #passing the data to frontend
    return render_template('index.html', lists = user_details)

if __name__ == '__main__':
    # Scheduler #2
    scheduler.add_job(id = 'Scheduled Task', func = update_sheet, trigger="interval", hours = 2)
    scheduler.start()
    # running the app
    app.run(debug = True)
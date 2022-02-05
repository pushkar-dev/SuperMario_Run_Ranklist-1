from apscheduler.schedulers.blocking import BlockingScheduler
import pandas
import requests as re
from db_access import *

scheduler = BlockingScheduler()
TIME_STAMP = 1643913000 #unix time stamp for 4th feb 2022
proxy = {
'http' : '',
'https' : ''
}
# reading the existing data
data = pandas.read_csv("handles")

# counting the number of Questions for a particular user
def helper(r, i, handle):
    temp = handle
    for x in temp.split("/")[-1].split(" "):
        if len(x):
            handle = x
    if(handle == "ANYTHING"):
        handle = ""

    try:
        s = set()
        json_data = r. json()
        try:
            for j in range(len(json_data["result"])):
                try:
                    if (json_data["result"][j]["verdict"] == "OK" and 
                        json_data["result"][j]["problem"]["rating"] >= max (data['ratings'][i], 1200) and
                        json_data["result"][j]["creationTimeSeconds"]>=TIME_STAMP and
                        json_data["result"][j]["author"]["ghost"]==False):
                        s.add(str(json_data["result"][j]["problem"]["name"]))
                except:
                    pass
            count = len(list(s))
        except:
            count = list(db.show(handle))[0][4]
            pass
    except:
        count = list(db.show(handle))[0][4]
    return count

#schedule 1
@scheduler.scheduled_job('interval',minutes = 1)
def update_sheet():
    print ("hello")
    for i in range(len(data["Name"])):
        url = "https://codeforces.com/api/user.status?handle="+data["Codeforces Handle"][i]+"&from=1&count=100000"
        r = re.get(url, proxies=proxy)
        db.update(helper(r, i, data["Codeforces Handle"][i]), data["Codeforces Handle"][i])
        print(i)

scheduler.start()
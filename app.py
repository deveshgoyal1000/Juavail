from flask import Flask
import psycopg2
from datetime import time, timedelta, datetime

from flask_cors import CORS

#cecid68764@horsgit.com
#Odint@2515

connection = psycopg2.connect("postgres://qjeqdubt:puPAcyhyc5JaLatA32l4ZuMXqNw0zSLB@rain.db.elephantsql.com/qjeqdubt")

def get_lec(room):
    lecs = []
    for i in range(1, len(room)):
        if(len(room[i].strip()) == 0):
            lecs.append("lec"+str(i))
    return lecs

def time_in_range(start, end, current):
    return start <= current <= end

def get_curr_lec():
    lec_time = {
        "lec1": (time(8,0,0), time(8,49,0)),
        "lec2": (time(8,50,0), time(9,39,0)),
        "lec3": (time(9,40,0), time(10,29,0)),
        "lec4": (time(10,30,0), time(11,19,0)),
        "lec5": (time(11,20,0), time(12,4,0)),
        "lec6": (time(12,5,0), time(12,49,0)),
    }

    for i in lec_time:
        if time_in_range(lec_time[i][0], lec_time[i][1], datetime.now().time()):
            return (i, lec_time[i])

    return (False, False)

app = Flask(__name__)

CORS(app)

@app.route("/days")
def get_all_days():
    res = []
    with connection:
        with connection.cursor() as cursor:
            days = ['monday', 'tuesday', 'wednesday', 'friday', 'saturday']
            for d in days:
                cursor.execute(f"select * from {'time_' + d[:3]};")
                tmp_data = cursor.fetchall()
                rooms = []
                for t in tmp_data:
                    rooms.append(
                        {
                            "room": t[0],
                            "lecs": get_lec(t)
                        }
                    )
                res.append(
                    {
                        "day": d,
                        "rooms": rooms
                    }
                )
    
    return res

@app.route("/avail")
def get_curr_avail():
    curr_day = datetime.now().strftime("%A").lower()
    curr_lec = get_curr_lec()[0]
    curr_lec_time = get_curr_lec()[1]

    if curr_day == "sunday":
        return {
            "Message": "Today is sunday"
        }

    if curr_lec == False:
        return{
            "Message": "All classes ended"
        }
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT room FROM time_{curr_day[:3]} WHERE {curr_lec} = ''")
            rooms = cursor.fetchall()
    return {
        "day": curr_day,
        "lec": curr_lec,
        "time": str(curr_lec_time[0]) +"-"+ str(curr_lec_time[1]),
        "empty_rooms": rooms
    }
    
if __name__ == "__main__":
    app.run(port=9999, debug=True,host="0.0.0.0")

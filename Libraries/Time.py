from datetime import datetime

Time = datetime.now()

def Time_update():
    global Time
    Time = datetime.now()

def Get_Time_text():
    global Time
    Time_update()
    return Time.strftime('%H:%M:%S.%f')
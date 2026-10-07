from datetime import datetime
import time

Time = datetime.now()

def Time_update():
    global Time
    Time = datetime.now()

def Get_Time_text():
    global Time
    Time_update()
    return Time.strftime('%H:%M:%S.%f')

def Start_Measureing_Elapsed_Time():
    return time.perf_counter()

def Time_Elapsed_Since_Start(start):
    return (time.perf_counter() - start)
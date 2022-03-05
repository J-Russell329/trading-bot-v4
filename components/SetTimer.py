from datetime import datetime, timedelta, date
import time

def SetTimer(seconds, startTimestamp, collectionTimestamp):
    # print(f"startTimestamp: {startTimestamp}")
    # print(f"collectionTimestamp: {collectionTimestamp}")
    # print(f"seconds: {seconds}")
    timerTime = (startTimestamp - collectionTimestamp).total_seconds()
    # print(f"timerTime: {timerTime}")
    # print(f"sleep for Time: {seconds-timerTime}")
    time.sleep(max(seconds-timerTime,0))

def GetTimer(currentTimestamp, getDataTimestamp):
    time.sleep(max((getDataTimestamp-currentTimestamp).total_seconds(),0.0050))

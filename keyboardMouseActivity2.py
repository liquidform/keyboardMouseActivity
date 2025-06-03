#!/usr/bin/env python3

# One way to monitor keyboard and mouse activity in real time is run this program in a separate terminal window resized just large enough for the output of an interval and always have that window be on top. With gnome terminal, right click the top window border aka title bar and click "Always on Top". Another way is to send the output as a notification but this will probably be more distracting. There's probably more sophisticated ways to do this such as printing to the system tray.

import aw_client
import aw_core
import socket
from datetime import datetime, date, timedelta, timezone
import time


# sum keyboard and mouse activity. To see what apps were used with presses and clicks just look at the Timeline tab in the web ui in conjunction w/ the output file created by this program
def sumActivity(oldEventTime, prevIntervalEvent, events):
    totalPresses = 0
    totalClicks = 0
    totalPressesAndClicks = 0
    totalDeltaX = 0
    totalDeltaY = 0
    totalMousePixels = 0
    totalScrollX = 0
    totalScrollY = 0
    totalScrollPixels = 0

    for event in events[0]:
        if event["id"] != prevIntervalEvent["id"]:
            presses = event["data"]["presses"]
            clicks = event["data"]["clicks"]
            pressesAndClicks = presses + clicks
            deltaX = event["data"]["deltaX"]
            deltaY = event["data"]["deltaY"]
            mousePixels = deltaX + deltaY
            scrollX = event["data"]["scrollX"]
            scrollY = event["data"]["scrollY"]
            scrollPixels = scrollX + scrollY

            totalPresses += presses
            totalClicks += clicks
            totalPressesAndClicks += pressesAndClicks
            totalDeltaX += deltaX
            totalDeltaY += deltaY
            totalMousePixels += mousePixels
            totalScrollX += scrollX
            totalScrollY += scrollY
            totalScrollPixels += scrollPixels

    print(oldEventTime, totalPresses, totalClicks, totalPressesAndClicks)
    print()
    print()
    print()


def interval(seconds, prevIntervalEvent, client, bucket_id): 
    if isinstance(prevIntervalEvent, aw_core.models.Event):
        oldEventTime = prevIntervalEvent["timestamp"]
        timeperiods = [(oldEventTime, oldEventTime+timedelta(seconds=60))] 
        print("timeperiods: ", timeperiods)
        print()
    else:
        eventTime = prevIntervalEvent["timestamp"]
        format = '%Y-%m-%dT%H:%M:%S.%f+00:00'
        oldEventTime = datetime.strptime(eventTime, format).replace(tzinfo=timezone.utc)
        oldEventDuration = prevIntervalEvent["duration"]
        startOfInterval = oldEventTime+timedelta(seconds=oldEventDuration)
        timeperiods = [(startOfInterval, startOfInterval+timedelta(seconds=60))] 
        print("timeperiods: ", timeperiods)
        print()

    query = 'RETURN = query_bucket("{}");'.format(bucket_id)

    time.sleep(seconds)

    events = client.query(query, timeperiods=timeperiods)

    print("events:")
    print(events)
    print()

    newEvent = events[0][0]
    print("newEvent: ", newEvent)
    print()

    sumActivity(oldEventTime, prevIntervalEvent, events)

    return newEvent
      
  
if __name__ == "__main__":

    client = aw_client.ActivityWatchClient("testclient")

    bucket_id = "aw-watcher-input_{}".format(socket.gethostname())

    prevEventList = client.get_events(bucket_id, limit=1)
    prevEvent = prevEventList[0]
    while True:
        prevEvent = interval(60, prevEvent, client, bucket_id) 

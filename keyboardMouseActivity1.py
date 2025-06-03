#!/usr/bin/env python3

# One way to monitor keyboard and mouse activity in real time is run this program in a separate terminal window resized just large enough for the output of an interval and always have that window be on top. With gnome terminal, right click the top window border aka title bar and click "Always on Top". Another way is to send the output as a notification but this will probably be more distracting.

import aw_client
import socket
import time


def interval(seconds, event, client, bucket_id): 
    # ensures most recent event in the previous interval isn't included in the current interval
    while(True):
        oldEvent = client.get_events(bucket_id, limit=1)
        if oldEvent[0].id == event.id and oldEvent[0].data["presses"] == event.data["presses"]:
            continue
        else:
            oldEventTime = oldEvent[0].timestamp
            break
    
    time.sleep(seconds) 

    events = client.get_events(bucket_id, start=oldEventTime)

    print(events)

    newEventTime = events[0].timestamp
    newEvent = events[0]

    print(oldEventTime)
    print(newEventTime)

    totalPresses = 0
    totalClicks = 0
    totalPressesAndClicks = 0
    totalDeltaX = 0
    totalDeltaY = 0
    totalMousePixels = 0
    totalScrollX = 0
    totalScrollY = 0
    totalScrollPixels = 0

    # sum keyboard and mouse activity. To see what apps were used with presses and clicks just look at the Timeline tab in the web ui in conjunction w/ the output file created by this program
    for event in events:
        presses = event.data["presses"]
        clicks = event.data["clicks"]
        pressesAndClicks = presses + clicks
        deltaX = event.data["deltaX"]
        deltaY = event.data["deltaY"]
        mousePixels = deltaX + deltaY
        scrollX = event.data["scrollX"]
        scrollY = event.data["scrollY"]
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

    return newEvent
      
  
if __name__ == "__main__":

    client = aw_client.ActivityWatchClient("testclient")

    bucket_id = "aw-watcher-input_{}".format(socket.gethostname())

    prevEventList = client.get_events(bucket_id, limit=1)
    prevEvent = prevEventList[0]
    while True:
        # Intervals start during an approximately 5 sec. event most of the time when typing sentences during the interval so to get a more accurate representation of chars/min, words/min, clicks/min, etc. then subtract 5 sec. from your chosen interval in seconds. Otherwise your intervals will be about 5 sec. more than you intended on avg.
        prevEvent = interval(55, prevEvent, client, bucket_id) 

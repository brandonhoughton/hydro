from pywemo import discover_devices
import time
import json
from pathlib import Path

def minSec(minutes, seconds):
    return minutes * 60 + seconds

def shouldBeQuiet(hour):
    if hour <= 8 or 22 <= hour:
        return True
    else:
        return False

def runFor(sec, device):
    if device.get_state() == 0:
        print('Switching device on')
        device.toggle()
        pass
    else:
        print('Device ' + device.name + ' set to run for ' + str(sec) + ' seconds but device is allready on!')
        #print('Last change was ', device.last_change)

    time.sleep(duration)

    if device.get_state() == 1:
        print('Switching device off')
        device.toggle()
    else:
        print('Device ' + device.name + ' set to run for ' + str(sec) + ' seconds but was turned off prematurly!')
        #print('Last change was ', device.last_change)


#Try to load last flood time from disk
lastFlood = 12
interval = 2

quietDuration = minSec(1,5)
minDuration  = minSec(1,25)
fullDuration = minSec(3,0)

my_file = Path("./info.json")
if my_file.is_file():
    x = json.load(my_file)
    lastFlood = x['lastFlood']
    interval = x['interval']
    quietDuration = x['quietDuration']
    minDuration  =  x['minDuration']
    fullDuration =  x['fullDuration']



pump = None
devices = []
while True:
    devices = discover_devices()
    if len(devices) == 0:
        continue
    else:
        print("Found devices: ", devices)
        for dev in devices:
            print( "Checking device: ", dev.name)
            if dev.name == 'Hydroponic Pump':
                print( "Found pump: ", dev.name)
                pump = dev
                break
        if pump != None:
            break
print('Using device:')
print(pump)
try:
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min

    if hour % interval == 0 and lastFlood != hour:
        print('Flooding tubes', time.strftime("%c"))
        duration = minDuration
        if hour % (interval * 2) == 0:
            print('Running longer')
            duration = fullDuration
        if shouldBeQuiet(hour):
            print('Quiet mode enabled')
            duration = quietDuration
        runFor(duration, pump)
        lastFlood = hour
    else:
        print('Waiting ... ', time.strftime("%c"))

    if pump.get_state() == 1:
        print('Switching device off')
        pump.toggle()
except Exception as exp:
    print(exp)
    pass


dat = {}
dat['lastFlood'] = lastFlood
dat['interval'] = interval
dat['quietDuration'] = quietDuration
dat['minDuration'] = minDuration
dat['fullDuration'] = fullDuration
json.dump(dat, my_file.open('w'))
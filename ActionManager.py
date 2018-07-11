from pywemo import discover_devices
import time

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


lastFlood = 0
interval = 2

quietDuration = minSec(1,5)
fullDuration  = minSec(1,25)

while True:
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
        while True:
            hour = time.localtime().tm_hour
            minute = time.localtime().tm_min

            #print("Interval hour:", hour % interval == 0)
            #print("Flooded this hour:", lastFlood == hour)

            if hour % interval == 0 and lastFlood != hour:
                print('Flooding tubes h', hour, 'm', minute)
                duration = fullDuration
                if shouldBeQuiet(hour):
                    print('Quiet mode enabled')
                    duration = quietDuration
                runFor(duration, pump)
                lastFlood = hour
            time.sleep(10)

            if pump.get_state() == 1:
                print('Switching device off')
                pump.toggle()
    except Exception as exp:
        print(exp)
        pass

# pump = devices[0]

# print(pump)
# print(pump.list_services())
# print(pump.get_state())

# #url = 'http://%s:%i/setup.xml' % (address, port)
# #discovery.device_from_description(url, None)

# print(devices)
# print(devices[0].list_services())



# print(devices[0].get_state())
# print(devices[0].last_change())


# #devices[0].toggle()
# #devices[0].toggle()
import bluetooth
import time
import RPi.GPIO as GPIO
from bt_rssi import BluetoothRSSI

search_time = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
THRESHOLD = (-13, 38)
# You can hardcode the desired device ID here as a string to skip the discovery stage
addr = "F4:AF:E7:72:CB:19"
b = BluetoothRSSI(addr=addr)

print("Welcome to the Bluetooth Detection Demo! \nMake sure your desired Bluetooth-capable device is turned on and "
      "discoverable.")

try:
    if addr is None:
        try:
            input("When you are ready to begin, press the Enter key to continue...")
        except SyntaxError:
            pass

        print("Searching for devices...")

        nearby_devices = bluetooth.discover_devices(duration=search_time, flush_cache=True, lookup_names=True)

        if len(nearby_devices) > 0:
            print("Found %d devices!" % len(nearby_devices))
        else:
            print("No devices found! Please check your Bluetooth device and restart the demo!")
            exit(0)

        i = 0  # Just an incrementer for labeling the list entries
        # Print out a list of all the discovered Bluetooth Devices
        for addr, name in nearby_devices:
            print("%s. %s - %s" % (i, addr, name))
            i = + 1

        device_num = input("Please specify the number of the device you want to track: ")

        # extract out the useful info on the desired device for use later
        addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]

    print("The script will now scan for the device %s." % addr)
    print("Feel free to move near and far away from the BeagleBone to see the state change on "
      "the LED.\nUse Ctrl+c to exit...")

    while True:
        # Try to gather information from the desired device.
        # We're using two different metrics (readable name and data services)
        # to reduce false negatives.
        rssi = b.get_rssi()
        state = bluetooth.lookup_name(addr, timeout=20)
        services = bluetooth.find_service(address=addr)
        # Flip the LED pin on or off depending on whether the device is nearby
        if THRESHOLD[0] < rssi < THRESHOLD[1]:
            GPIO.output(17, 1)
        else:
            GPIO.output(17, 0)
        # Arbitrary wait time
        time.sleep(1)
except:
    print("Exited...")
finally:
    GPIO.cleanup()

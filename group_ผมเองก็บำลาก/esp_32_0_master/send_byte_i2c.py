import network
import time

def connect(net):
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.connect(net['name'], net['password']) # connect to an AP
    retry_count = 0
    while wlan.isconnected()  == False:
        time.sleep(10)
        retry_count+=1
        print("trying to reconnect")
        wlan.connect(net['name'], net['password'])
        if retry_count == 10:
            return []

    return [ wlan ]

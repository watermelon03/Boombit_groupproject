from machine import Pin, I2C, UART
from send_byte_i2c import connect

import neopixel
from time import sleep
from class_tower import Tower_pixel

import socket
import time
import _thread
import random



random.seed(time.ticks_ms())
i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)
net = dict()
net['name'] = 'onlyme'
net['password'] = '403403403'
wlan = connect(net)[0]

np = neopixel.NeoPixel(Pin(12), 64)
button = Pin(13, Pin.IN)

url = 'tcp://0.tcp.ap.ngrok.io'
PORT = 12560

# uart1 = UART(1, 9600)                      # init with given baudrate
# uart1.init(9600, bits=8, parity=None, stop=1)

class Game():
    def __init__(self , game_mode,i2c_a , l_uart):
        self.failed_count = 0
        #initial timer for easy mode = 10 min
        self.timer_limit = 300
        self.start_time = time.time()
        self.failed_limit = 3
        self.mode_game = game_mode
        self.game_state = []
        #self.pass_state = [1,1,0,0]
        #self.i2c_address = [0x50 , 0 , 0 , 0]
        self.mcu = []
        self.my_serial = 47
        self.exit = False
        self.req_test(url)
        self.init_mcu(i2c_a , l_uart)
        #print(i2c.scan())

    
    def p(self):
        print(self.mode_game)
        
    def req_get(self , url):
        if wlan.isconnected():
            s = socket.socket()
            try :
                usplit  = url.split('/')
                host = usplit[2]
                path = usplit[3]
                s.connect((host, 80))
                req = bytes('GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n' % (path,host), 'utf8')
                s.send(req)
                print(str(s.recv(500), 'utf8'), end = '')
            finally:
                s.close()
                
    def req_test(self , url):
        if wlan.isconnected():
            s = socket.socket()
            try :
                usplit  = url.split('/')
                host = usplit[2]
                #path = usplit[3]
                s.connect((host, PORT))
                #req = bytes(str('hello:',self.my_serial) , 'utf8')
                msg = 'hello:'+str(self.my_serial)
                s.sendall(bytes(msg , 'utf8'))
                res = str(s.recv(500), 'utf8')
                print("try update game")
                self.update_game(res , 1)
            finally:
                s.close()
                
    def req_end(self,time_left , p):
        if wlan.isconnected():
            s = socket.socket()
            try :
                usplit  = url.split('/')
                host = usplit[2]
                #path = usplit[3]
                s.connect((host, PORT))
                msg = "bro im done:"+str(self.my_serial)+":"+str(time_left)+":"+p
                req = bytes(msg , 'utf8')
                s.send(req)
                res = str(s.recv(500), 'utf8')
                self.update_game(res , 1)
            finally:
                s.close()
        
    def update_game(self , res , u ):
        r = res.split(':') 
        if len(r) == 2:
            if(r[1] == '1'):
                print("update game")
                self.game_state.append(0)
                self.mode_game = 1
                uart = UART(u,9600)
                uart.init(9600 , bits = 8 , parity = None, stop = 1)
                m = [1 , uart , True]
                self.mcu.append(m)
#                 i = 0
#                 while i == 0 or not m[2]:
#                     print("try jaaaa", i)
#                     try :
#                         m[1].write(b'\x45')
#                         m[2] = True
#                     except Exception as err :
#                         m[2] = False
#                         print("init uart error ",err )
#                     i = i+1
#                     time.sleep(1)
        else :
            print("error")
    
                
    def timer_start(self):
        while(time.time() - self.start_time < self.timer_limit and (not self.check_exit())):
            print("timer decreased",time.time() - self.start_time)
            time.sleep_ms(100)
            if self.check_exit() :
                break
        self.timer_limit = -1
        _thread.exit()

                


#class Game_4(Game):
#    def __init__(self , game_mode):
#        self.mode_game = 4
#        self.game_state = [0,0,0,0]
#        self.pass_state = [1,1,0,0]
#        self.i2c_address = [0x52 , 0x54 , 0 , 0]
        #self.init_mcu()
        
            
    
#     def init_board_0(self) :
#         #self.read_address[0] = address
#         #print("board 0 address:",address)
#         # 0xFF means initial succesfull
#         i2c.writeto(self.i2c_address[0], b'\x05')
#         print("init success read data is ",i2c.readfrom(self.i2c_address[0], 1))
        
     
    def init_mcu(self , i2c_ad , l_uart):
        for i2c in i2c_ad:
            self.mcu.append([ 0 , i2c])
            self.game_state.append(0)
        for u in l_uart:
            uart = UART(u,9600)
            uart.init(9600 , bits = 8 , parity = None, stop = 1)
            self.mcu.append([1 , uart])
            self.game_state.append(0)
        self.game_state.append(0)
        print(self.mcu)
    
    
    def start_mcu(self):
        
        for mcu in self.mcu:
            if mcu[0] == 0:
                mcu.append(True)
                i = 0
                while i == 0 or not mcu[2]:
                    print("try jaaaa", i)
                    try :
                        t = random.random()%200/1000
                        print("time is ",t)
                        time.sleep(t)
                        i2c.writeto(mcu[1], b'\x45')
                        mcu[2] = True
                    except Exception as err :
                        mcu[2] = False
                        print(mcu[1], " init error ",err)
                    i = i+1
                    time.sleep(1)
            elif mcu[0] == 1:
                mcu.append(True)
                i = 0
                while i == 0 or not mcu[2]:
                    print("try jaaaa", i)
                    try :
                        #time.sleep(float(random()%200/1000))
                        t = random.random()%200/1000
     

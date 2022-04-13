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


#wifi ssid
net['name'] = ''
#wifi password
net['password'] = ''

wlan = connect(net)[0]

np = neopixel.NeoPixel(Pin(12), 64)
button = Pin(13, Pin.IN)


#socket url
url = 'tcp://0.tcp.ap.ngrok.io'
#socket port
PORT = 12560

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
                        print("time is ",t)
                        time.sleep(t)
                        mcu[1].write(b'\x45')
                        mcu[2] = True
                    except Exception as err :
                        mcu[2] = False
                        print("init uart error ",err )
                    i = i+1
                    time.sleep(1)
                
    
    def mcu_polling(self):
        i = 0
        for mcu in self.mcu  :
            Byte = ''
            #state = self.game_state[i]
            if mcu[2] and not self.check_exit() :
                if mcu[0] == 0:
                    try:
                        Byte = i2c.readfrom(mcu[1] , 1)
                        poll = int.from_bytes(Byte , "big")
                    except:
                        poll  = self.game_state[i]
                elif mcu[0] == 1:
                    print("any = ",mcu[1].any())
                    try:
                        if (mcu[1].any()):
                            Byte = mcu[1].read()
                            poll = int.from_bytes(Byte , "little")
                            
                        else :
                            poll = self.game_state[i]
                            if(i == 3):
                                poll = self.game_state[4]
                    except:
                        poll = self.game_state[i]
                        
                print('mcu',mcu[0] ,' ', mcu[1],'poll got : ',poll)
                if poll == 255:
                    self.failed_count += 1
                    poll = self.game_state[i]
                if(i == 3):
                    self.game_state[4] = poll
                else:
                    self.game_state[i] = poll
#                self.verify_end()
                i+=1
                print(self.game_state, " failed count = ",self.failed_count)
                
    def my_polling(self, tower) :
        tower_state = tower.check_state()
        print("---", tower_state, "---")
        if tower_state == -1 :
            self.failed_count += 1
            tower_state = tower.set_state()
        elif tower_state == 1 :
            if self.mode_game == 1 :
                len_state = len(self.game_state)
                self.game_state[len_state-2] = 1 
            else :
                self.game_state[-1] = 1         
        self.verify_end()
                
                    
    
#     def mcu_polling(self):
#         present_state = self.game_state
#         for i in range(len(self.i2c_address)):
#             state = self.game_state[i]
#             if self.i2c_address[i] != 0:
#                 try:
#                     #print("address ",self.i2c_address[i], " get ",state)
#                     kuy = i2c.readfrom(0x50 , 1)
#                     #i2c.readfrom(0x50 , 1)
#                     state = int.from_bytes(kuy , "big")
#                     #state = i2c.readfrom(0x50 , 2)
#                     #print(state)
#                     #print("address ",0x50, " get ",state)
#                     #i2c.writeto(0x50 , b'\x01')
#                     print("i'm not failed")
#                 except:
#                     state = self.game_state[i]
#                     print("failed to polling")
#                 #print("address ",self.i2c_address[i], " get ",state)    
#                 #state = 0
#                 print(state)
#                 if state == 255:
#                     self.failed_count += 1
#                     self.game_state[i] = 0
#                     if self.failed_count == self.failed_limit:
#                         print("Boom bitches!")
#                 else :
#                     self.game_state[i] = state
#                 self.verify_end()
#         #change it to victory method soon!        


    
    def notify_ending(self ):
        for mcu in self.mcu:
            if mcu[2]:
                if mcu[0] == 0:
                    i = 0
                    flag = False 
                    while i < 5 and not flag: 
                        try:
                            i2c.writeto(mcu[1] , b'\x2F' )
                            flag = True
                        except Exception as err :
                            print(mcu[1]," error while notify ending" ,err)
                        i+=1
                        time.sleep(0.1)
                elif mcu[0] ==  1:
                    i = 0
                    flag = False
                    while not flag and i < 5:
                        try :
                            mcu[1].write(b'\x2F')
                            flag = True
                        except Exception as err:
                            print(mcu[1], " error while notify ending", err)
                        i+=1
                        time.sleep(0.1)
                        
            
        
    
    def verify_end(self):
        t = time.time() - self.start_time 
        if self.game_state.count(0) == 0 and time.time() - self.start_time <= self.timer_limit > 0:
            print("you pass")
            self.notify_ending()
            self.req_end(t, '1')
            self.exit = True
            _thread.exit()
        if self.failed_count >= self.failed_limit or self.timer_limit == -1:
            self.notify_ending()
            self.req_end(t, '0')
            self.exit = True
            _thread.exit()
            
            
    def game_start(self):
        self.start_mcu()
        tower = Tower_pixel(np, button)
        _thread.start_new_thread(tower.start_game_tower,([g]))
        while(self.check_exit() == False):
            time.sleep(0.2)
            print("playing")
            self.mcu_polling()
            self.my_polling(tower)
            self.verify_end()
            if self.check_exit() :
                break
        _thread.exit()
            
            
        
    def check_exit(self):
        return self.exit
     
        
def start_game(game):
    game.game_start()
    
def timer_thread(game ):
     print("start timer ")
     game.timer_start()
    
       
       

if __name__ == "__main__":
    g = Game(0,[0x50 , 0x51],[2])
    
    _thread.start_new_thread(timer_thread ,([g]))
    _thread.start_new_thread(start_game , ([g]))
    while( not g.check_exit() ):
        print("still there")
        time.sleep(1)
    print("end")
    
    


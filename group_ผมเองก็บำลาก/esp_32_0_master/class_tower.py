from machine import Pin
import neopixel
from random import randint
from time import sleep
import _thread

class Tower_pixel():
    def __init__(self, np, button):
        self.np = np
        self.button = button
        self.cur_base_line = 7
        self.arr_root_base = []
        self.arr_block = []
        self.btn = 0
        self.game_pass = 0
        self.game_state = 0
        self.game_stop = False

    def wait_pin_change(self):
        cur_value = self.button.value()
        active = 0
        while active < 20:
            if self.button.value() != cur_value:
                active += 1
            else:
                active = 0
            sleep(0.001)
            
    def button_thread(self) :
        while True :
            self.wait_pin_change()
            self.btn = 1
            self.wait_pin_change()
            break

    def clearAll_pixel(self) :
        for i in range(0,64) :
            self.np[i] = (0, 0, 0)
            self.np.write()
            
    def clearLine_pixel(self, line) :
        start = line*8
        for i in range(0,8) :
            self.np[start+i] = (0, 0, 0)
            self.np.write()
            
    def print_pixel(self, arr, r, g, b):
        for i in arr :
            self.np[i] = (r, g, b)
            self.np.write()
            
    def set_state(self):
        self.game_state = 0
        return self.game_state
    
    def check_state(self):
        return self.game_state
    
    def init_tower(self) :
        self.set_state()
        self.clearAll_pixel()
        arr_base = []
        self.arr_root_base = []
        self.cur_base_line = 7
        start_base = self.cur_base_line*8
        start_dot = randint(1, 4)
        for i in range(3) :
            self.arr_root_base.append(start_dot+i)
            arr_base.append(start_dot+i+start_base)
        self.print_pixel(arr_base, 40, 0, 0)
    
    def block_slide(self, g) :
        self.btn = 0
        count = 0
        next_dot = 1
        left = randint(0, 5) - 1
        center = left+1
        right = left+2
        _thread.start_new_thread(self.button_thread, ())
        self.game_stop = g.check_exit()
        while self.btn == 0 and not self.game_stop :
            if right > 6 :
                next_dot = 0
            elif left < 1 :
                next_dot = 1
            if next_dot :
                left = left+1
                center = center+1
                right = right+1
            else :
                left = left-1
                center = center-1
                right = right-1
            self.clearLine_pixel(0)
            self.arr_block = [left, center, right]
            self.print_pixel(self.arr_block, 0, 40, 0)
            count = count+1
            if not self.game_stop :
                self.game_stop = g.check_exit()
            sleep(0.25)
    
    def block_drop(self, g) :
        line = 0
        self.game_stop = g.check_exit()
        while line < self.cur_base_line-1 and not self.game_stop :
            self.clearLine_pixel(line)
            arr_drop = []
            line = line+1
            start_base = line*8
            for i in self.arr_block :
                arr_drop.append(i+start_base)
            self.print_pixel(arr_drop, 0, 0, 40)
            sleep(0.2)
            if not self.game_stop :
                self.game_stop = g.check_exit()
        self.cur_base_line = line
     
    def check_logic_tower(self) :
        self.game_pass = 0
        center_base = self.arr_root_base[1]
        center_root = self.arr_block[1]
        if center_root == center_base-1 or center_root == center_base or center_root == center_base+1 :
            self.game_pass = 1
        
    def emo_smile(self) :
        self.clearAll_pixel()
        arr_yellow = [2,3,4,5,9,10,11,12,13,14,16,19,20,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,43,44,46,47,49,50,53,54,58,59,60,61]
        self.print_pixel(arr_yellow, 32, 28, 0)
        arr_black = [17,18,21,22,42,45,51,52]
        self.print_pixel(arr_black, 20, 20, 20)
    
    def emo_sad(self) :
        self.clearAll_pixel()
        arr_yellow = [2,3,4,5,9,10,11,12,13,14,16,19,20,23,26,25,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,45,46,47,49,51,52,54,58,59,60,61]
        self.print_pixel(arr_yellow, 32, 28, 0)
        arr_blue = [24,31]
        self.print_pixel(arr_blue, 0, 10, 32)
        arr_black = [17,18,21,22,43,44,50,53]
        self.print_pixel(arr_black, 20, 20, 20)
    
    def emo_angry(self) :
        self.clearAll_pixel()
        arr_red = [0,2,3,4,5,7,9,10,11,12,13,14,16,19,20,23,24,25,27,28,30,31,32,33,34,35,36,37,38,39,40,41,42,45,46,47,49,51,52,54,58,59,60,61]
        self.print_pixel(arr_red, 32, 5, 0)
        arr_black = [17,18,21,22,26,29,43,44,50,53]
        self.print_pixel(arr_black, 20, 20, 20)

    def start_game_tower(self, g) :
        self.init_tower()
        self.game_stop = g.check_exit()
        while self.cur_base_line-1 > 0 and not self.game_stop:
            self.block_slide(g)
            if not self.game_stop :
                self.game_stop = g.check_exit()
            if self.game_stop :
                break
            sleep(0.3)
            self.block_drop(g)
            if not self.game_stop :
                self.game_stop = g.check_exit()
            if self.game_stop :
                break
            self.check_logic_tower()
            print(self.game_pass)
            if self.game_pass == 0 :
                self.game_state = -1
                if not self.game_stop :
                    self.game_stop = g.check_exit()
                if self.game_stop :
                    break
                self.emo_sad()
                sleep(2)
                self.init_tower()
            sleep(0.8)
            if not self.game_stop :
                self.game_stop = g.check_exit()
        sleep(0.5)
        if self.game_stop :
            self.emo_angry()
            print("You are Loser")
        else :
            self.game_state = 1
            self.emo_smile()
            print("You are Winner")
        sleep(5)
        self.clearAll_pixel()
        _thread.exit()




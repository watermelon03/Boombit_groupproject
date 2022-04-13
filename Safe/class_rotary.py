from time import sleep, ticks_ms 
from machine import I2C, Pin, UART
import _thread
from random import randint

from rotary_irq_esp import RotaryIRQ
from i2c_lcd import I2cLcd 

class Rotary_game() :
    def __init__(self, r, sw, lcd, uart):
        self.r = r
        self.sw = sw
        self.lcd = lcd
        self.uart = uart
        self.rval_old = r.value()
        self.rval_new = self.rval_old
        self.answer = 0
        self.count_pass = 0
        self.btn = 0
        self.game_state = b'\x00'
        self.game_start = False
        self.game_stop = False

        self.top = [[],[]]
        self.down = [[],[]]
        self.right = [[],[]]
        self.left = [[],[]]
        self.top[0] = [2,6,10,12,18,22,24]
        self.top[1] = [2,6,8,20,22,26]
        self.down[0] = [4,6,8,18,24,28]
        self.down[1] = [2,6,8,12,18,20,24]
        self.right[0] = [2,4,8,10,20,24]
        self.right[1] = [2,8,10,20,22,24,28]
        self.left[0] = [2,6,10,18,24,26,28]
        self.left[1] = [6,8,12,20,24,26]
      
    def wait_sw_change(self):
        cur_value = self.sw.value()
        active = 0
        while active < 20 and not self.game_stop :
            if self.sw.value() != cur_value :
                active += 1
            else:
                active = 0
            sleep(0.001)
            
    def sw_thread(self) :
        while True :
            self.wait_sw_change()
            self.btn = 1
            self.wait_sw_change()
            break
        _thread.exit()
        
    def clear_lcd(self) :
        self.lcd.clear()
    
    def print_same_lcd(self, arr, ch) :   #lcd16*2
        for i in arr :
            row = 0
            col = i
            if i > 15 :
                row = 1
                col = i - 16
            self.lcd.move_to(col, row)
            self.lcd.putchar(ch)

    def rotary_to_lcd(self) :
        set_logic = randint(0, 1)
        self.clear_lcd()
        sleep(0.5)
        print(self.answer, set_logic)
        arr_border = [0,1,13,14,15,16,17,29,30,31]
        self.print_same_lcd(arr_border, '#')
        if self.answer == 0 :
            self.print_same_lcd(self.top[set_logic], 'X')
        elif self.answer == 1 :
            self.print_same_lcd(self.right[set_logic], 'X')
        elif self.answer == 2 :
            self.print_same_lcd(self.down[set_logic], 'X')
        elif self.answer == 3 :
            self.print_same_lcd(self.left[set_logic], 'X')

    def init_rotary(self) :
        self.btn = 0
        self.game_state = 0
        self.game_collect = False
        randans = randint(0, 3)
        while self.answer == randans :
            randans = randint(0, 3)
        self.answer = randans
#         self.answer = 0
        self.rotary_to_lcd()       
            
    def check_rotary(self) :
        self.rval_new = self.r.value()
        self.rval_old = self.rval_new
        print('result = {}'.format(self.rval_new))

    def check_ans(self) :
        self.check_rotary()
        sleep(0.1)
        rans = self.rval_new
        ans = self.answer*5
        if rans == 19 :
            rans = -1
        self.clear_lcd()
        if rans == ans or rans == ans-1 or rans == ans+1 :
            self.count_pass += 1
            self.lcd.putstr("  Good...")
            print("True, Good")
        else :
            self.game_state = b'\xFF'
            self.lcd.putstr("  Try agian...")
            print("False, Loser sus sus")
            self.uart.write(self.game_state)
            print(self.game_state)

    def start_game(self) :
        self.lcd.putstr("  Game Start!")
        sleep(2)
        while self.count_pass < 1 and not self.game_stop :
            self.init_rotary()
            _thread.start_new_thread(self.sw_thread, ())
            while self.btn == 0 and not self.game_stop :
                sleep(0.1)
            if self.game_stop :
                break
            self.check_ans()
            sleep(1)
            self.clear_lcd()
            sleep(0.5)
        self.clear_lcd()
        if self.game_stop :
            print("You are Loser")
            self.lcd.putstr("You are Loser!")
        else :
            self.game_state = b'\x01'
            print("You are Winner")
            self.lcd.putstr("You are Winner!")
            self.uart.write(self.game_state)
            print(self.game_state) 
#         print("check-out")
        sleep(3)
        self.clear_lcd()
        _thread.exit()

    def main_esp(self):
        while True:
            commu = self.uart.read()
#             print(commu)
            if commu != None :
                print("You communication with me as... ", commu)
                if ord(commu) == 69 :
                    print("Game Start")
                    sleep(0.3)
                    if not self.game_start :
                        self.game_start = True
                        self.game_stop = False
                        _thread.start_new_thread(self.start_game,())
                if ord(commu) == 47:
                    print("Game Over")
                    self.game_start = False
                    self.game_stop = True
                    sleep(0.3)
                    break
            sleep(0.6)
        sleep(1)
        print("--- E N D G A M E ---")


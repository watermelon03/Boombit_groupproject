import time
from machine import Pin, I2C, UART
import random
from ssd1306 import SSD1306_I2C
import _thread

global btn
global alphabet
global selected
global sequence
global answer
#global i2c
i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)
global oled
global your_ans

global button1
global button2
global button3
global button4

global state
global is_pass
global btnend

btnend = 0
is_pass = 0
global thread
thread = [0,0,0,0]
def wait_pin_change(button):
    cur_value = button.value()
    active = 0
    while active < 20 and is_pass == 0:
        if button.value() != cur_value:
            active += 1
        else:
            active = 0
        time.sleep(0.001)

def button1_thread(button) :
    global btn
    global btnend
    print("start thread 1")
    btnend = 0
    while True :
        wait_pin_change(button)
        btn = 1
        wait_pin_change(button)
        break
    btnend = 1
    print("thread 1 end")
    _thread.exit()
    
def button2_thread(button) :
    global btn
    global btnend
    print("start thread 2")
    btnend = 0
    while True :
        wait_pin_change(button)
        btn = 2
        wait_pin_change(button)
        break
    btnend = 1
    print("thread 2 end")
    _thread.exit()

def button3_thread(button) :
    global btn
    global btnend
    print("start thread 3")
    btnend = 0
    while True :
        wait_pin_change(button)
        btn = 3
        wait_pin_change(button)
        break
    btnend = 1
    print("thread 3 end")
    _thread.exit()

def button4_thread(button) :
    global btn
    global btnend
    print("start thread 4")
    btnend = 0
    while True :
        wait_pin_change(button)
        btn = 4
        wait_pin_change(button)
        break
    btnend = 1
    print("thread 4 end")
    _thread.exit()

def get_random():
    selected.clear()
    sequence.clear()
    answer.clear()
    while True:
        random.seed(time.ticks_ms())
        rand = random.randrange(0, 9)
        rand = alphabet[rand]
        if rand not in selected:
            selected.append(rand)
        if len(selected) == 4:
            break
    for select in selected:
        sequence.append(alphabet.index(select))
        sequence_sorted = sequence.copy()      
        sequence_sorted.sort()

    for ans in sequence_sorted:
        answer.append(sequence.index(ans))
    
    print("sequence =",sequence)
    print('sequence_sorted =',sequence_sorted)
    print('answer =',answer)

def show_oled():
    oled.fill(0)
    oled.text(selected[0],0,0)
    oled.text(selected[1],32,16)
    oled.text(selected[2],64,32)
    oled.text(selected[3],96,48)
    n0_correct = 'Pass = ' + str(len(your_ans))
    if len(your_ans) < 4:
        oled.text(n0_correct,65,0)
    else:
        oled.text('All Pass!!',65,0)
    oled.show()
    
def start(uart):
    print("start")
    global is_pass
    is_pass = 0
    global state
    state = b'\x00'
    str_state = []
    global alphabet
    alphabet = ['klmn','mnop','efgh','cdef','abcd','yzab','uvwx','ghij','qrst','ijkl']
    global selected
    selected = []
    global sequence
    sequence = []
    global answer
    answer = []
    #i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)
    global oled
    oled = SSD1306_I2C(128,64,i2c)
    global your_ans
    your_ans = []

    global button1
    button1 = Pin(13, Pin.IN)
    global button2
    button2 = Pin(12, Pin.IN)
    global button3
    button3 = Pin(14, Pin.IN)
    global button4
    button4 = Pin(27, Pin.IN)

    global btn
    btn = 0
    _thread.start_new_thread(button1_thread, (button1,))
    _thread.start_new_thread(button2_thread, (button2,))
    _thread.start_new_thread(button3_thread, (button3,))
    _thread.start_new_thread(button4_thread, (button4,))

    get_random()
    show_oled()
    global btnend
    while is_pass == 0:
        state = b'\x00'
        print('your_ans =',your_ans)
        while btn == 0 :
            x = 0
        print("momo")
        
        time.sleep(0.15)
        if is_pass == 1 :
            break
        your_ans.append(btn-1)
        if your_ans[-1] != answer[len(your_ans)-1]:
            print("try again")
            your_ans.clear()
            get_random()
            state = b'\xFF'
            uart.write(state)
            print(state)
        elif your_ans == answer:
            print("pass")
            state = b'\x01'
            uart.write(state)
            time.sleep(0.1)
            print(state)
            is_pass = 1
    #         uart.write('pass')
            show_oled()
        show_oled()
        time.sleep(0.15)
        while btnend == 0:
            x = 0
        if btn == 1 and is_pass == 0:
            print(btn)
            _thread.start_new_thread(button1_thread, (button1,))
        elif btn == 2 and is_pass == 0:
            print(btn)
            _thread.start_new_thread(button2_thread, (button2,))
        elif btn == 3 and is_pass == 0:
            print(btn)
            _thread.start_new_thread(button3_thread, (button3,))
        elif btn == 4 and is_pass == 0:
            print(btn)
            _thread.start_new_thread(button4_thread, (button4,))
        btn = 0
    print("out_while")
    _thread.exit()
#         str_state = chr(state)
#         uart.write(str_state)
#         print(str_state, state)
        
def ALP(uart):
    global is_pass
    while True:
        x = uart.read()
        if x != None :
            if ord(x) == 69 :
                print("game start")
                _thread.start_new_thread(start,(uart,))
            if ord(x) == 47:
                is_pass = 1
                break
        time.sleep(0.8)
    time.sleep(2)    
    print("I SUS")

uart = UART(2, 9600)                         # init with given baudr ate
uart.init(9600, bits=8, parity=None, stop=1)
ALP(uart)
# start(uart) 

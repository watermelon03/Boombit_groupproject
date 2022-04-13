from rotary_irq_esp import RotaryIRQ
from machine import I2C, Pin, UART
from i2c_lcd import I2cLcd
from class_rotary import Rotary_game

DEFAULT_I2C_ADDR = 0x27

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

r = RotaryIRQ(pin_num_clk=32, 
              pin_num_dt=33, 
              min_val=0, 
              max_val=19, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)
sw = Pin(34, Pin.IN)


rot = Rotary_game(r, sw, lcd, uart)
# rot.start_game()
rot.main_esp()


Dependency library (need to be downloads)


I2c_lcd:https://techtotinker.blogspot.com/2021/01/008-micropython-technotes-16x2-lcd.html?m=1
Rotary_irq_esp : https://github.com/miketeachman/micropython-rotary
React-countdown-circle-timer : https://www.npmjs.com/package/react-countdown-circle-timer 
React-hook-form : https://react-hook-form.com/
React-pdf : https://www.npmjs.com/package/react-pdf
DebounceIn : https://os.mbed.com/users/pilotak/code/DebounceIn/






คู่มือการเล่นเกม : https://docs.google.com/document/d/1zdboJJapsm2Sdhj-8ohvT7nEEhFJXi56ff9u5qPQ0yY/edit










































Folder structure


ในทุก folder ที่เป็น source code ของ microcontroller จะมี รูป schematic ของวงจร ใน board นั้นๆอยู่ด้วย 


Group_ผมเองก็บำลาก -> esp_32_0_master : folder นี้เก็บไฟล์ที่ต้อง upload ลง esp32 1 ตัวที่เป็น master และต้อง 
             Downloads file : lcd_api.py และ i2c_lcd.py จาก เว็บที่ระบุไว้ที่หัวข้อ      
             Dependency library
* class_tower.py
* Master.py
* send_byte_i2c.py
                      -> esp_32_1 :  folder นี้เก็บไฟล์ที่ต้อง upload ลง esp32 1 ตัวเพื่อ run เกม alphabet
                                      - alphabet.py 
                      -> esp_32_2 :   folder นี้เก็บไฟล์ที่ต้อง upload ลง esp32 1 ตัวเพื่อ run เกม
                                      - class_rotary.py
                                      - game_rotary.py
                                      - lcd_api.py
                                      - i2c_lcd.py
                     -> socketserver : folder นี้เก็บไฟล์ที่ใช้ในการติดต่อระหว่าง mcu (esp_32_0_master) 
      - test_websocket.py
    -> stm32_0 :  folder นี้เก็บไฟล์ที่ต้อง upload ลง stm32 1 ตัวเพื่อ run เกม wire cut , compile ลงด้วย 
                           Mbed studio
                      - main.cpp
    -> stm32_1 :  folder นี้เก็บไฟล์ที่ต้อง upload ลง stm32 1 ตัวเพื่อ run เกม press sequence , compile 
                           ลงด้วย Mbed studio
              - main.cpp
                    -> web_app : folder นี้เก็บไฟล์ใช้ใน src ของเว็บ 
                                      - component folder : ประกอบด้วย component ที่ใช้แสดงเอกสารการกู้ระเบิด
                                      - App.css 
                                      - App.js : เป็นไฟล์หลักที่มีการใส่ข้อมูลและเรียกใช้ api 
                                      - App.test.js
                                      - boom_bit.pdf : pdf ที่ใช้เป็นคู่มือประกอบการเล่น
                                      - index.css
                                      - index.js
                                      - logo.svg
                                      - reportWebVitals.js
                                      -setupTest.js
                    -> webserver : folder นี้เก็บไฟล์ใช้ใน รัน webserver เพื่อเชื่อมต่อ ระหว่าง socketserver และ api ที่ใช้ใน     
                                     Web_app
                                      - config.py
                                      - main.py
                 - readme.txt : this file
 - ผมเองก็บำลาก_pic.png : รูปกลุ่มพร้อมชิ้นงาน 
 - IMG20220329210627.jpg : รูปภายใน model ของ project
 - unknown.png : รูปภายนอก model ของ project
 - license.txt
/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "DebounceIn.h"
#include <cstdio>

DigitalOut led1(PA_8);
DigitalOut led2(PA_11);
DigitalOut led3(PB_5);
DigitalOut led4(PB_4);

DebounceIn sw1(PA_4,PullUp);
DebounceIn sw2(PA_3,PullUp);
DebounceIn sw3(PA_1,PullUp);
DebounceIn sw4(PA_0,PullUp);

Thread thread_game;
Thread thread_i2c;
  
I2CSlave slave(D4,D5); 

#define BLINKING_RATE 1000ms


void blink(int led){
    switch(led){
        case 1:
            led1 = 1;
            ThisThread::sleep_for(BLINKING_RATE);
            led1=0;
            ThisThread::sleep_for(BLINKING_RATE/2);
            break;
        case 2:
            led2 = 1;
            ThisThread::sleep_for(BLINKING_RATE);
            led2=0;
            ThisThread::sleep_for(BLINKING_RATE/2);
            break;
        case 3:
            led3 = 1;
            ThisThread::sleep_for(BLINKING_RATE);
            led3=0;
            ThisThread::sleep_for(BLINKING_RATE/2);
            break;
        case 4:
            led4 = 1;
            ThisThread::sleep_for(BLINKING_RATE);
            led4=0;
            ThisThread::sleep_for(BLINKING_RATE/2);
            break;
    }
} 

int cc=0;
int ans[4]={0,0,0,0};
int gamestart=0,gamestop=0,state=0,ready=0;

void sw1_pressed(void) {
    if(ready==1){
        cc = cc + 1;
        ans[cc-1]=1;       
    }
    else{
        ready=1;    
    }
    // ready=1;
}

void sw2_pressed(void) {
    cc = cc + 1;
    ans[cc-1]=2;
}

void sw3_pressed(void) {
    cc = cc + 1;
    ans[cc-1]=3;
}

void sw4_pressed(void) {
    cc = cc + 1;
    ans[cc-1]=4;
}
void fail_lcd(){
    led1=1;
    led2=1;
    led3=1;
    led4=1;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=0;
    led2=0;
    led3=0;
    led4=0;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=1;
    led2=1;
    led3=1;
    led4=1;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=0;
    led2=0;
    led3=0;
    led4=0;
    ThisThread::sleep_for(BLINKING_RATE);
}
void win_lcd(){
    led1=1;
    led2=0;
    led3=1;
    led4=0;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=0;
    led2=1;
    led3=0;
    led4=1;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=1;
    led2=0;
    led3=1;
    led4=0;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=0;
    led2=1;
    led3=0;
    led4=1;
    ThisThread::sleep_for(BLINKING_RATE);
    led1=0;
    led2=0;
    led3=0;
    led4=0;
    ThisThread::sleep_for(BLINKING_RATE);
}


void i2c_master() {
// void message() {
    char buf[20];
    int check = 0;
    int count = 10;
    char A[5];
    slave.address(0xA0); 
    while (1) {
        int i = slave.receive();
        for(int i = 0; i < sizeof(buf); i++) buf[i] = 0; // Clear buffer
        switch (i) {
            case I2CSlave::ReadAddressed:
                A[0] = (char)state;
                slave.write(A, 1);
                if(state == -1){
                    printf("send fail\n");
                    ThisThread::sleep_for(100ms);
                    state = 0;
                }
                break;

                // 0 not yet
                // 1 pass
                // - fail
            case I2CSlave::WriteAddressed:
                slave.read(buf,sizeof(buf)-1);
                int buf_int = buf[0];
                printf("Blink requested: %d\n", buf_int);

                    if(buf_int == 69){
                        gamestart = 1;
                    }
                    else if (buf_int == 47){
                        gamestop =1;
                        ready=0;
                        gamestart=0;
                        thread_game.terminate();
                            //     led1=1;
                            // led2=1;
                            // led3=1;
                            // led4=1;
                    }
                break;
        }
    }
}


void game(){
    int i,j,n,l,k,p=0,q=0;
    time_t t;
    int seq[4];
    int in[4];
    int min = 999;
    int max = 0;
    int a,b,c,d,difmin,difmax,tempmin1=999,tempmin2=999;


    
    led1 = 1;
    ThisThread::sleep_for(BLINKING_RATE/2);
    led1=0;
    ThisThread::sleep_for(BLINKING_RATE/2);
    printf("start\n");
        while(1){

            if(gamestart == 1 && ready == 1){
                gamestart = 0;
                srand((unsigned) us_ticker_read());

                for( i = 0 ; i < 4 ; i++ ) {
                    seq[i] =( rand() % 1000)+1;
                    if(seq[i]<min){
                        min=seq[i];
                        a=i;
                    }
                    if(seq[i]>max){
                        max=seq[i];
                        d=i;
                    }
                }

                for( i = 0 ; i < 4 ; i++ ) {
                    difmin = seq[i]-min;
                    difmax = max - seq[i];
                    if(seq[i] != max){
                        if(difmax<tempmin1){
                            tempmin1=difmax;
                            c=i;
                        }
                    }
                    if(seq[i]!=min){
                        if(difmin<tempmin2){
                            tempmin2=difmin;
                            b=i;
                        }
                    }
                }
                seq[0]=a+1;
                seq[1]=b+1;
                seq[2]=c+1;
                seq[3]=d+1;
                for( i = 0 ; i < 4 ; i++ ) {
                    printf("seq %d : %d\n",i+1,seq[i]);
                    printf("------------------\n");
                }
                
                // end of gen sequence ----------------------------------------------------------------

                printf("game start\n");
                win_lcd();
                for( i = 1 ; i < 5;  ) { 
                    if(gamestop==1)
                        break;

                    for( l = 0 ; l < i ; l++ ) {
                        if(gamestop==1)
                            break;
                        blink(seq[l]);
                    }    

                    for( j = 1 ; j <= i ; j++ ) {
                        //loop button
                        if(gamestop==1)
                            break;

                        while(cc < j){
                            if(gamestop==1)
                                break;
                            sw1.fall(sw1_pressed);
                            sw2.fall(sw2_pressed);
                            sw3.fall(sw3_pressed);
                            sw4.fall(sw4_pressed);
                            ThisThread::sleep_for(100ms);
                        }

                        if(seq[j-1] == ans[j-1])
                            printf("pass\n");
                        else{
                            state=-1;
                            q=1;
                            fail_lcd();
                            // state=0;
                            break;
                        }
                    }
                    if(q==0)
                        i++;
                    else
                        i=1;
                    q=0;
                    cc=0;
                }
                state=1;
                printf("success\n");
                win_lcd();
            }
            else{
                sw1.fall(sw1_pressed);
                ThisThread::sleep_for(200ms);
                // while(!ready)
                    // sw1.fall(sw1_pressed);
            }
        }
        printf("gg");
        led1=1;
        led2=1;
        led3=1;
        led4=1;

}

int main(){
    thread_i2c.start(i2c_master);
    ThisThread::sleep_for(BLINKING_RATE);   
    thread_game.start(game);

}

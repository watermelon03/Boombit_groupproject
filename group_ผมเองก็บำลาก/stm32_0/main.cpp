#include "mbed.h"
#include <cstdio>
#include <ctime>


//gpio_t input1;
bool start = false; 
Thread thread1;
Thread thread2;
Thread thread3;

I2CSlave slave(D0,D1);
//gpio_init(gpio_t *input1, PinName pin)

DigitalIn input0(D3 , PullUp);
DigitalIn input1(D4 , PullUp);
DigitalIn input2(D5 , PullUp);
DigitalIn input3(D6 , PullUp);
DigitalIn input4(D9 , PullUp);
DigitalOut output0(PA_0);
DigitalOut output1(PA_1);
DigitalOut output2(PA_3);
DigitalOut output3(PA_4);
DigitalOut output4(PB_4);
//gpio_init(gpio_t *obj, PinName pin)


void gen_freq(int mode , int freq[5] ){
    int n0,n1,n2,n3,n4;

    switch (mode){
        case 0:
            n0 = rand()%10;
            while (n0%4 == 0) n0 = rand()%10;

            n1 = rand()%10;
            while (n1 == 5 ) n1 = rand()%10;

            n2 = rand()%10;
            n3 = rand()%10;
            n4 = rand()%10;
            while (n4  == n2 ) n4 = rand()%10;
            break;
        
        case 1: 
            n1 = 5;
            n0 = rand()%10;
            n2 = rand()%10;
            n3 = rand()%10;
            n4 = rand()%10;
            break;

        case 2:
            n0 = rand()%10;
            n1 = rand()%10;
            n2 = rand()%10;
            while (n2 == 5) n2 = rand()%10;
            n3 = rand()%10;
            n4 = n2;
            break;

        case 3:
            n0 = rand()%10;
            while (n0 > 2) n0 = rand()%10;
            n1 = n0;
            n2 = n0;
            n3 = n0;
            n4 = n0;
            break;

        case 4:
            n0 = rand()%10;
            while (n0 %4 != 0) n0 = rand()%10;
            n1 = rand()%10;
            while(n1 == 5) n1 = rand()%10;
            n2 = rand()%10;
            n3 = rand()%10;
            n4 = rand()%10;
            while (n4 == n2) n4 = rand()%10;
            break;
        case 5:
            n0 = rand()%10;
            while (n0 <= 2) n0 = rand()%10;
            n1 = n0;
            n2 = n0;
            n3 = n0;
            n4 = n0;
            break;

    }
    freq[0] = n0;
    freq[1] = n1;
    freq[2] = n2;
    freq[3] = n3;
    freq[4] = n4;
}


int check_wire(int wire){
    int ret ;
    switch (wire){
        case 0 :
            ret = input0;
            break;
        case 1:
            ret = input1;
            break;
        case 2:
            ret = input2;
            break;
        case 3:
            ret = input3;
            break;
        case 4:
            ret = input4;
            break;
    }
    return !ret;
}


int freq[5] = {-1,-1,-1,-1,-1};
int game_state = 0;

void main1(){
    while(!start){
        printf("w1\n");
        ThisThread::sleep_for(100ms);
    } 
    printf("main1 start\n");
    time_t t ;  
    srand((unsigned) us_ticker_read());
    int ans = rand()%5;
    gen_freq(ans , freq);
    //printf("%d %d %d %d %d",freq[0], freq[1], freq[2],freq[3], freq[4]);
    printf("..%d..",ans);
    while(game_state == 0 && start ){
        for(int i = 0 ; i < 5 ; i++){
            if(i == ans){
                if(! check_wire(i) && start){
                    game_state = 1;
                    printf("ans discon");
                }
            }
            else {
                if(! check_wire(i) && start){
                    game_state = -1;
                    printf("no ans discon ");
                }
            }
        }
    
    printf("ans:%d 0:%d 1:%d 2:%d 3:%d 4:%d\n",ans,check_wire(0),check_wire(1),check_wire(2),check_wire(3),check_wire(4));
    ThisThread::sleep_for(100ms);
    }
}

void blink(int n){
    switch (n){
        case 0 :
            output0 = !output0;
            break;
        case 1 :
            output1 = !output1;
            break;
        case 2 :
            output2 = !output2;
            break;
        case 3 :
            output3 = !output3;
            break;
        case 4 :
            output4 = !output4;
            break;
    } 
}

void main2(){
  int counter = 0;
  //printf("[state : %d]\n",game_state);
  while(! start){
      printf("w2\n");
      ThisThread::sleep_for(100ms);
  } 
  printf("main2 start\n");
  while(freq[4] == -1) /*printf("esus4\n")*/;

  int n = 0;
  int blink_rate ;
  while(game_state == 0 && start ){
      counter = 0;
      blink_rate = 1000/freq[n];
      //printf("[state : %d]\n",game_state);
      //if(counter % int(10 / freq[0]) == 0) output0 = !output0;
      //if(counter % int(10 / freq[1]) == 0) output1 = !output1;
      //if(counter % int(10 / freq[2]) == 0) output2 = !output2;
      //if(counter % int(10 / freq[3]) == 0) output3 = !output3;
      //if(counter % int(10 / freq[4]) == 0) output4 = !output4;
      //output4 = 0;
      while(counter < (2*freq[n])){
        blink( n );
        counter += 1;
        ThisThread::sleep_for(blink_rate);
      }
      //counter += 1;
      n = (n+1)%5;
      //ThisThread::sleep_for(100ms);
  }
  //printf("[state : %d]\n",game_state);
  printf("game is end\n");
}


void message() {
    char buf[20];
    int check = 0;
    int count = 10;
    char A[5];
    slave.address(0xA2); 
    while (1) {
        int i = slave.receive();
        for(int i = 0; i < sizeof(buf); i++) buf[i] = 0; // Clear buffer
        switch (i) {
            case I2CSlave::ReadAddressed:
                A[0] = (char)game_state;
                slave.write(A, 1);
                if(game_state == -1){
                    start = false;
                    game_state = 0;
                    printf("game state = %d\n",game_state);
                }
                break;

                // 0 not yet
                // 1 pass
                // - fail
            case I2CSlave::WriteAddressed:
                slave.read(buf,sizeof(buf)-1);
                int buf_int = buf[0];
                //printf("Blink requested: %d\n", buf_int);
                if(buf_int == 69){
                    start = true;
                }
                else if(buf_int == 101)start = false;
                else if (buf_int == 47){
                    start = false;
                    printf("terminate");
                    //NVIC_SystemReset();
                    thread1.terminate();
                    thread2.terminate();
                    thread3.terminate();
                };
                break;
        }
    }
}


//10ms / freq



int main(){
    thread3.start(message);
    //while (! start );
    thread1.start(main1);
    thread2.start(main2);
    //while(start) {} ;
    //thread1.terminate();
    //thread2.terminate();
    //thread3.terminate();
    //printf("fuck you");
}



#include "serial_device.h"
#include "gpio_device.h"
//#include "blck_serial.h"
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sfr_defs.h>

//volatile char incoming[2];
//static int uart_putchar(char c, FILE *stream);
//static FILE mystdout = FDEV_SETUP_STREAM(uart_putchar, NULL,_FDEV_SETUP_WRITE);
//static int uart_putchar(char c, FILE *stream){
  //if (c == '\n')
    //uart_putchar('\r', stream);
  //loop_until_bit_is_set(UCSR0A, UDRE0);
  //UDR0 = c;
  //return 0;
//}
//FILE mystdout &incoming;
char table[2];
void print(char s[]){
  uint8_t i ;
  for(i=0;s[i]!='\0';i++)
    serial_put(s[i]);
  s[i]='\0';
  serial_put(s[i]);
}

int readline(char s[], uint8_t m){
  uint8_t i = 0;
  uint8_t n;
  while(true){
    n= serial_get();
    if((isgraph(n))&&(i!=m)){
      s[i]=n;
      i++;
    }
    else
      break;
  }
  s[i]='\0';
  return i;
}
void apaga(void){
    PORTB &= ~(_BV(5));
   //PORTB &= ~(_BV(5)) ;
}
void encen(void){
    //PINB |= _BV(5) ;
    PORTB |= _BV(5) ;

}
void init_led(void){
   DDRB |= 0b00100000; //DDRB5 AS OUTPUT
   //PORTB &= ~(_BV(5)) ;
   //PORTB |= _BV(5);
   apaga();
}

void setup(void){
    init_led();
    serial_init();
    sei();
}
bool consulta(void){
    return bit_is_set(PINB,5);
}
int main (void){
    uint8_t c;
    //stdout= &mystdout;
    if (serial_can_read ()){
        if (readline(table,2)){
            print("l");
        //c='\0';
            //serial_put(c);
        //while((c=serial_get())!= '\n'){

    //        if ((c !='E') || (c=! 'A')||(c!='C')){
            if (table[0]=='E'){
                encen();
            }
            else if(table[0]='A'){//incoming[0]
                apaga();
            }
            else if (table[0]=='C'){//incoming[0]
                if (consulta()){
                    print("1");
                }
                else {
                    print("0");
                }
            }
        }
        else print("P");
    }
    return 0;
}

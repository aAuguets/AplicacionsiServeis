#include <pbn.h>
#include <stdio.h>
#include <stdlib.h>
#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL

static void setup(void);
static void led_on(void);
static void led_off(void);
static void state_led(void);

static pin_t led;

static void setup(void){
  led = pin_create(&PORTB, 5, Output);
  pin_w(led, false);
  serial_open();
}

static void led_on(void){
  pin_w(led, true);
}

static void led_off(void){
  pin_w(led, false);
}

static void state_led(void){
    if(bit_is_set(PINB,5))
      print("1");
    else
      print("0");
}

int main(void){
  char caracter;
  setup();
  sei();
  while(true){
    if(serial_can_read()){
      caracter = serial_get();
      switch(caracter){
      case 'E':
	     led_on();
	      break;
      case 'A':
	     led_off();
	      break;
      case 'S':
	     state_led();
	      break;
      default:
	     break;
        }
      }
    }
  cli();
  serial_close();
  return 0;
}

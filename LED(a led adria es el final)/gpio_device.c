#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#include "gpio_device.h"


pin_t pin_bind(volatile uint8_t *port,uint8_t pin, pin_direction_t d){

  pin_t p;
  p.port=port;
  p.pin=pin;
  
  if (d == Input)
    *(port-1) &= ~(_BV(pin));//mascara cambia el valor del DDR(lo pone 1)
  else if(d==Output)//pone el DDR del port como salida 
    *(port-1) |= (_BV(pin));
  return p;
}

void pin_w(pin_t p,bool v){
  if ((p.port)!=NULL){ // si esta asociado el PORT.
    if (bit_is_set(*((p.port-1)),p.pin)){ //miramos si es Output el DDR
      if (v==true)
	*(p.port) |= _BV(p.pin);//1
      else
	*(p.port) &= ~_BV(p.pin);//0
    }
  }
}

bool pin_r(pin_t p){
  if ((p.port)!=NULL) // miramos si esta asociado el PORT
    return bit_is_set(*(p.port-2),p.pin);//leemos el PIN 1=True, 0=False
  return false;
}


void pin_toggle(pin_t p){
  if (p.port != NULL){//miramos si esta asociado
    if (bit_is_set(*(p.port-1),p.pin)){// miramos si EL DDR esta en 1(output)
      if (bit_is_set(*(p.port),p.pin)){// si tenemos un 1 en el port(encendido)
	pin_w(p,false);//off
      }
      else{
	pin_w(p,true); //on
      }
    }
  }
}
void pin_unbind(pin_t *const p){
  (*p).port=NULL;
}

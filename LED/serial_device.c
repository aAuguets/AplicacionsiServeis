#include "serial_device.h"
#include <avr/io.h>

#define BAUD_RATE 9600
#define CLK_BY100 F_CPU/100
#define BDR 16*BAUD_RATE/100
#define MYUBRR ((CLK_BY100/BDR)-1)

void serial_init(void){
  /* Set baud rate */
  //UBRR0H = (uint8_t)MYUBRR>>8;
  //UBRR0L = (uint8_t)MYUBRR;
  UBRR0H=0;
  UBRR0L=103;

  /* arreglem el bit U2X0 */
  UCSR0A &= ~_BV(U2X0);

  /* Enable receiver and transmitter */
  UCSR0B |= _BV(TXEN0)|_BV(RXEN0);

  /* Set frame format: 8data, 1stop bit, no parity */
  UCSR0C |=_BV(UCSZ00)|_BV(UCSZ01);
}

uint8_t serial_get(void){
  /* Return the value of Data Register */
  loop_until_bit_is_set(UCSR0A,RXC0)
    ;
  return UDR0;
}

void serial_put(uint8_t c){
  /* Wait for Data Register Empty, 
     before send new data */
  loop_until_bit_is_set(UCSR0A,UDRE0)
    ;
  UDR0=c;
}

bool serial_can_read(void){
  /* return False if USART RX Not Complete */
  return bit_is_set(UCSR0A,RXC0);
}

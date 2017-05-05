#include <stdio.h>
#include <avr/io.h>
#include <util/delay.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>

#ifndef _GPIO_DEVICE_H
#define _GPIO_DEVICE_H 

typedef enum{Input=0, Output=1} pin_direction_t;//especifica la direccion del pin

typedef struct{   //asi se Representa un pin
	volatile uint8_t *port;
	uint8_t pin;
} pin_t;

pin_t pin_bind(volatile uint8_t *port, uint8_t pin, pin_direction_t d);
//retorna un objecte pin_t asociado al pin numero pin, del port Port i de
// inicializacion de mode d.

void pin_w(pin_t p,bool v);
//escribe un valor v en el pin p. p estara asociado y en modo output.

bool pin_r(pin_t p);
// lee el valor del pin p. p estara asociado y en modo Input.

void pin_toggle(pin_t p);
//conmuta el valor del pin p. p estara asociado i en modo Output.

void pin_unbind(pin_t *const p);
//desasocia el pin p d'un pin fisic.
#endif

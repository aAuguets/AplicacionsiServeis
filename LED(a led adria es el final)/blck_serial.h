#ifndef _BLCK_SERIAL_H
#define _BLCK_SERIAL_H
#include "serial_device.h"
#include <stdlib.h>
#include <stdint.h>


//Envia per la UART el bloc de caracters que se li passa com aparametre. Quan troba el caracter ’\0’ acaba.
void print(char  s[]);

//Va llegint caracters i els va guardant a la taula s fins que troba un caracter no grafic o be el nombre de caracters iguala a m. El valor retornat  es el nombre de caracters que ha llegit.
int readline(char  s[], uint8_t m);

#endif

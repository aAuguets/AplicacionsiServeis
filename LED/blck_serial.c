#include "blck_serial.h"
#include <ctype.h>
#include <stdlib.h>
#include <stdint.h>

void print(char s[]){
  uint8_t i ;
  for(i=0;s[i]!='\0';i++)
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

#ifndef SERIAL_DEVICE
#define SERIAL_DEVICE
#include <inttypes.h>
#include <stdbool.h>

void serial_init(void);
uint8_t serial_get(void);
void serial_put(uint8_t);
bool serial_can_read(void);

#endif


.PHONY : loadmain
loadmain: main.hex
	sudo avrdude -c arduino -p atmega328p -P /dev/cu.usbmodem1421 -U main.hex
	rm -f *~ *.hex main
	sudo picocom /dev/cu.usbmodem1421 -c 9600
#115200

main:  serial_device.c    main.c

# opcio 1 standard: 2368 bytes
	avr-gcc -std=c99 -Os -mmcu=atmega328p -fshort-enums -DF_CPU=16000000UL main.c serial_device.c -o main

# opcio 2 minimized 2014 bytes
#	avr-gcc -std=c99 -Wall -Os -mmcu=atmega328p -fshort-enums -Wl,-u,vfprintf -lprintf_min -DF_CPU=16000000UL osc.c serial_device.c  control_TMR0.c -o osc

# opcio 3 with float 3888 bytes
##	avr-gcc -std=c99 -Wall -Os -mmcu=atmega328p -fshort-enums -Wl,-u,vfprintf -lprintf_flt -lm -DF_CPU=16000000UL main.c serial_device.c  control_TMR0.c adc.c tmr0.c -o main

main.hex: main
	avr-objcopy -Oihex main main.hex

#main.hex: main
#avr-objcopy -Oihex main main.hex

#main: serial_device.o  gpio_device.o main.o
#avr-gcc -std=c99 -Os -mmcu=atmega328p -fshort-enums -DF_CPU=16000000UL serial_device.o semaphore.o gpio_device.o controlsem.o main.o -o main

#main.o: main.c serial_device.h
#avr-gcc -std=c99 -Os -mmcu=atmega328p -fshort-enums -DF_CPU=16000000UL main.c -c

#gpio_device.o: gpio_device.c gpio_device.h
#avr-gcc -std=c99 -Os -mmcu=atmega328p -fshort-enums -DF_CPU=16000000UL gpio_device.c -c

#serial_device.o: serial_device.c serial_device.h
#avr-gcc -std=c99 -Os -mmcu=atmega328p -fshort-enums -DF_CPU=16000000UL serial_device.c -c

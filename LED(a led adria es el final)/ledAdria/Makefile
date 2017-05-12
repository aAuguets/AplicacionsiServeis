led:
	avr-gcc -std=c99 -Os -mmcu=atmega328p -fshort-enums -DF_CPU=16000000UL -Ilibpbn main.c -o main libpbn/libpbn.a
	avr-objcopy -Oihex main main.hex
	avrdude -c arduino -p atmega328p -P /dev/cu.usbmodem1421 -U main.hex
	picocom /dev/cu.usbmodem1421

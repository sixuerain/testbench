#!/usr/bin/env python
import smbus, time

# ls /dev/i2c-1  => smbus(1)
bus=smbus.SMBus(1)
AT=0x27
# address check with $>  i2cdetect -y 1
filename="register.txt"
with open(filename, 'r') as f:
  ioss=int(f.next())

ios=ioss if 0<=ioss<=65535 else 0

# GPIO EXPANDER pinout : 
# ON_1 : P00  P10 : OFF_1
# ON_2 : P01  P11 : OFF_2
# ON_3 : P02  P12 : OFF_3
# ON_4 : P03  P13 : OFF_4
# ON_5 : P04  P14 : OFF_5
# ON_6 : P05  P15 : OFF_6
# ON_7 : P06  P16 : OFF_7
# ON_8 : P07  P17 : OFF_8

# Demarrage : Rpi (USB meter) = 500mA
bus.write_byte_data(AT,0x00,0xff)# 670 mA 'clic' des 4 relais
bus.write_byte_data(AT,0xff,0xff)# => 500mA => plus de conso des relai
# commutation sans bruit

bus.write_byte_data(AT,0xff,0x00)# 750mA 'clac' des 4 relais
bus.write_byte_data(AT,0xff,0xff)# 500mA => pause plus de conso normallement
# commutation sans bruit

port0=0xfe
port1=0xff
ios=(port1<<8)|(port0&0xff)

print "P0 {0:02x} : {1:08b}".format(port0,port0)
print "P1 {0:02x} : {1:08b}".format(port1,port1)
print "register {0:04x} : {1:16b} {2:d}".format(ios,ios,ios)

  

FILE = open(filename,"w")
FILE.write("{}".format(ios))
FILE.close()

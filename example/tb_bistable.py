import bistable
import smbus, time; from time import sleep
import numpy as np

import RPi.GPIO as GPIO ; GPIO.setmode(GPIO.BOARD)
[GPIO.setup(i, GPIO.IN) for i in [31,33,35,37]]
bi=bistable.bistable(0x27); bi.AT, bi.reg

bi.setreg(0b1000)
bi.send(1)# UP
bi.release()# no more conso : relay maintained
bi.regs()# read gpio where loopback test power by vdd and re-read by gpio
bi.send(0)# Position Zero for REGISTERS (required power)
bi.release()# no more conso : relay maintained


bi.setreg(0b1000); bi.send(1); sleep(1) ; bi.release(); sleep(0.1);bi.regs()
bi.setreg(0b1111); bi.send(0); sleep(1) ; bi.release(); sleep(0.1);bi.regs()
bi.setreg(0b0001); bi.send(1); sleep(1) ; bi.release(); sleep(0.1);bi.regs()
bi.setreg(0b0010); bi.send(1); sleep(1) ; bi.release(); sleep(0.1);bi.regs()
bi.setreg(0b0011); bi.send(1); sleep(1) ; bi.release(); sleep(0.1);bi.regs()
bi.setreg(0b0100); bi.send(1); sleep(1) ; bi.release(); sleep(0.1);bi.regs()
bi.setreg(0b0100); bi.send(0); sleep(1) ; bi.release(); sleep(0.1);bi.regs()

bi.setreg(0b0111); bi.send(0); sleep(0.1) ; bi.release(); sleep(0.1);bi.regs()
#=> ['0:1', '1:0', '2:0', '3:0']
bi.setreg(0b1010); bi.send(1); sleep(0.1) ; bi.release();sleep(0.1); bi.regs()
#['0:1', '1:0', '2:1', '3:0']
bi.setreg(0b1000); bi.send(0); sleep(0.1) ; bi.release();sleep(0.1); bi.regs()

# bi.regs() need more time: 0.4s

bi.addreg(1)
bi.send(1)

bi.regs()

bus=smbus.SMBus(1);
bus.write_byte_data(0x27, 1<<1, 0x00 )

# # Scurve :
# for delay in np.arange(0,0.1,0.001) :
#     k=0
#     for i in range(100):
#         bi.send(1)
#         sleep(delay)
# #        bi.regs()
#         R=bi.read(1)
#         bi.release()
#         bi.send(0)
#         sleep(0.2)
#         k=k+1 if R else k
#     print "delay ; {} ; {}".format(delay, k)
# # delay ; 0.0 ; 0
# # delay ; 0.001 ; 0
# # delay ; 0.002 ; 0
# # delay ; 0.003 ; 0
# # delay ; 0.004 ; 100
# # delay ; 0.005 ; 100
# # delay ; 0.006 ; 100
# # delay ; 0.007 ; 100
# # delay ; 0.008 ; 100


for i in range(18):
    print("{:08b}".format(i%16))
    bi.setreg(i)
    bi.read(i)


bi.setreg(7)
bi.read8b()

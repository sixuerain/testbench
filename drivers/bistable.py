#!/usr/bin/env python
import smbus; from time import sleep
bus=smbus.SMBus(1); AT=0x27 # ls /dev/i2c-1  => smbus(1)


class bistable:
  filename="register.txt"
  def __init__(self, AT=0x27, gpio=[31,33,35,37],filename=filename):
    self.version= "ebecheto-v2"
    self.AT=AT
    try:
      _reg = open(filename).read()
    except IOError:
      _reg = '0b0000'
    _reg=_reg if _reg!='' else '0b0'
    base=2 if _reg[0:2]=="0b" else 10
    ioss=int(_reg, base)
    ios=ioss if 0<=ioss<2**8 else 0
    self.reg=ios
  
  def __del__(self,filename=filename):
    open(filename, "w").write("0b{:08b}".format(self.reg))

  def addreg(self, nb):
    self.reg |= (1<<nb)
  
  def rmreg(self, nb):
    self.reg &= ~(1<<nb)
  
  def setreg(self, ios):
    self.reg = ios&0xff
  
  def send(self, onoff):
    """
    write(AT, 0x00, 0xff) enable all
    write(AT, 0xff, 0x00) disable all
    """
    ports=[self.reg, 0x00]
    if onoff:
      ports.reverse()
    bus.write_byte_data(self.AT, ports[0], ports[1] )
    
  def release(self):
    bus.write_byte_data(self.AT,0x00,0x00)# 750mA 'clac' des 4 relais
    
  def reset(self):
    self.reg=0
    
  def regs(self):
    return ["{}:{}".format(i, self.read(i)) for i in range(4)]
  
  def tic(self,onoff=1, tps=0.03):
    self.send(onoff)# UP
    sleep(tps)
    self.release()# no more conso : relay maintained

  def tac(self,onoff=0, tps=0.03):
    self.send(onoff)# UP
    sleep(tps)
    self.release()# no more conso : relay maintained

  

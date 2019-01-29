#!/usr/bin/env python
import smbus; from time import sleep
bus=smbus.SMBus(1); AT=0x27 # ls /dev/i2c-1  => smbus(1)
# mtps temps de maintien du relai
# TODO : check if position in maintained during a long period of operation (1 week) withou command. Test1 : withtout load, Test2: with 12V-few amps load.

class bistable:
  filename="register.txt"
  def __init__(self, AT=0x27,inb=False, mtps=0.03 ,filename=filename):
    self.version= "ebecheto-v3"
    self.AT=AT; self.mtps=mtps
    try:
      _reg = open(filename).read()
    except IOError:
      _reg = '0b0000'
    _reg=_reg if _reg!='' else '0b0'
    _reg=_reg if not(inb) else inb
    base=2 if _reg[0:2]=="0b" else 10
    ioss=int(_reg, base)
    ios=ioss if 0<=ioss<2**8 else 0
    self.reg=ios
  
  def __del__(self,filename=filename):
    open(filename, "w").write("0b{:08b}".format(self.reg))

  def __str__(self):
    return "REG=0b{:08b}".format(self.reg)
  
  # def __repr__(self):
  #   return "REG=0b{:08b}".format(self.reg)
  
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
  
  def tic(self,onoff=1):
    self.send(onoff)# UP
    sleep(self.mtps)
    self.release()# no more conso : relay maintained

  def tac(self,onoff=0):
    self.send(onoff)# UP
    sleep(self.mtps)
    self.release()# no more conso : relay maintained

  def set(self):
    """
    switch the relay in register one by one (optimized current)
    """
    for i in range(8):
      mask=1<<i
      bit=(self.reg>>i)&0x1
      ports=[mask, 0x00]
      if bit:
        ports.reverse()
      bus.write_byte_data(self.AT, ports[0], ports[1] )
      sleep(self.mtps)
      self.release()# no more conso : relay maintained
  
  def setOnly(self, i=0, onoff=1):
    """
    bit range 0-7
    onoff=1 ==> UP
    onoff=0 ==> DOWN
    """
    mask=1<<i
    ports=[mask, 0x00]
    if onoff:
      ports.reverse()
    bus.write_byte_data(self.AT, ports[0], ports[1] )
    sleep(self.mtps)
    self.release()# no more conso : relay maintained
    self.reg=self.reg|(onoff<<i) if onoff else ~(1<<i)&self.reg
  
  def inc(self):
    """
    increment
    """
    oldReg=self.reg
    self.reg=0x00
    for i in range(8):
      self.setOnly(i)
      raw_input("{} {}".format(i,self))
    self.reg=oldReg

  def loop(self):
    oldReg=self.reg
    self.reg=0x00
    for i in range(8):
      self.setOnly(i)
      if i>0:
        self.setOnly(i-1,0)
      print("{} {}".format(i,self))
    self.reg=oldReg

  def chenillard(self):
    while(True):
      self.loop()

  def rampe(self):
    oldReg=self.reg
    for i in range(2**5):
      self.setreg(i)
      self.set()
      print(self)
      

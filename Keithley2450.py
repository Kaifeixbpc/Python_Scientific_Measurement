# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:43:09 2018

@author: Kaifei Kang
"""

import visa
rm=visa.ResourceManager()
import numpy as np
import time

class Keithley2450():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
    
    def get_idn(self):
        self.x = self.inst.query('*IDN?')
        return self.x
    
    def query_command(self,value):
        self.x = self.inst.query(value)
        return self.x
    
    def write_command(self, value):
        self.inst.write(value)
    
    
    def set_volt(self,value):
        self.inst.write("SOUR:FUNC VOLT")
        self.inst.write("SOUR:VOLT:LEV "+str(value))

    def set_curr(self,value):
        self.inst.write("SOUR:FUNC CURR")
        self.inst.write("SOUR:CURR:LEV "+str(value))
        
    def get_volt(self):
        self.inst.write("SENS:FUNC 'VOLT'")
        self.x=self.x.strip('\n')
        return float(self.x)
    
    def get_curr(self):
        self.inst.write("SENS:FUNC 'CURR'")
        self.x=self.inst.query(":MEAS:CURR?")
        self.x=self.x.strip('\n')
        return float(self.x)

    def get_set_volt(self):
        self.x = self.inst.query(":SOUR:VOLT:LEV?")
        self.x=self.x.strip('\n').split(',')[0]
        return (float(self.x))
    
    def ramp_gate(self,end, num = 100, waittime = 0.1):
        
        self.curr_gate = self.get_set_volt()
        self.list=np.linspace(self.curr_gate, end, num)
        
        for i in range(len(self.list)):
            self.set_volt(self.list[i])
            time.sleep(waittime)
            
    def scan_volt(self,low,high,num):
        self.x=np.linspace(low,high,num)
        for i in self.x:
            self.set_volt((i))
#            print(self.get_curr())
            time.sleep(0.1)
    
    def scan_curr(self,low,high,num):
        self.x=np.linspace(low,high,num)
        for i in self.x:
            self.set_curr((i))
#            print(self.get_curr())
            time.sleep(0.1)
#    
    def closeall(self):
        self.inst.close()
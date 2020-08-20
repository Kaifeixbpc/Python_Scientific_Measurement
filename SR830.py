# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:18:13 2018

@author: Kaifei Kang

SR830 sometime return unexpected values through GPIB. Turn it off and on could solve the problem.
"""
import visa
import numpy as np
import time
rm=visa.ResourceManager()
funclist=([ 'get_X', 'get_Y', 'get_R', 'get_Theta', 'get_AUX','set_amplitude',  'set_freq'])
class SR830():
    
    def __init__(self,address):
        self.inst=rm.open_resource(address)
        self._auto_ON = False
        self.func_list={'get_X':self.get_X,'get_Y':self.get_Y,'set_amplitude':self.set_AC_Volt,
                       'printX':self.printx}
    
    def write(self, value):
        print(self.inst.query(value))
    def printx(self):
        print('Hi')
    def get_X(self):
        self.x=self.inst.query("OUTP?1")
        self.x = float(self.x.strip("\n"))
#        if self._auto_ON :
#            self._Xval=float(self.x)
#            self.__auto_range()
        return self.x
    
    def get_Y(self):
        self.x=self.inst.query("OUTP?2")
        self.x = float(self.x.strip("\n"))
        if self._auto_ON:
            self._Yval=float(self.x)
        return self.x
    
    def get_R(self):
        self.x=self.inst.query("OUTP?3")
        self.x = float(self.x.strip("\n"))
        if self._auto_ON:
            self._Rval=float(self.x)
            self.__auto_range()
        return self.x
    
    def get_Theta(self):
        self.x=self.inst.query("OUTP?4")
        self.x = float(self.x.strip("\n"))
        return self.x
    
    def set_AC_Volt(self,value):
        self.inst.write("SLVL"+str(value))
        
    def scan_bias(self,low,high,num):
        self.x=np.linspace(float(low),float(high),int(num)+1)
        for i in range(int(num)+1):
            self.set_AC_Volt(self.x[i])
            self.get_X()
            self.get_Y()
                
    def set_freq(self, value):
        self.inst.write('FREQ {}'.format(value))
    
    def get_AUX(self,InputPortNum):
        self.x=self.inst.query("OAUX?"+str(int(InputPortNum)))
        self.x = self.x.strip("\n")
        return self.x
        return False
    def get_SENS(self):
        self.x=self.inst.query('SENS?')
        self.x=self.x.strip("\n")
        return self.x
    
    def set_auto_range(self,value,InputType ='volt'):
        self._auto_ON = False
        if value == 'on':
            self.senslist = np.array([2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9, 1e-6, 2e-6, 
                          5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3, 2e-3, 5e-3,
                          10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3, 1])
            if InputType == 'curr':
                self.senslist = self.senslist*1e-6
            self.sens=int(self.get_SENS())
            self._Xval=0
            self._Yval=0
            self._Rval=0
            self._auto_ON = True
        return False
            
    def __auto_range(self):
        i = self.sens
        value=max(abs(self._Xval),abs(self._Yval),abs(self._Rval))
        if value < 0.1*self.senslist[i]:
            i = i-1
        elif value > 0.85*self.senslist[i]:
            i=i+2
        if i < 12:
            i=12
        if i > 26:
            i=26
        if i != self.sens:
            self.inst.write('SENS ' +str(i))
            self.sens=i
            print('SR830 changed range to '+ str(self.senslist[i]) + ' X='+ str(self._Xval) +' Y=' +str(self._Yval) +'\n')
            time.sleep(0.1)
        return False  
    def call_func(self, arg,*args):
        
        a=self.func_list[arg].__get__(self, type(self))(*args)
        return a
    
    def closeall(self):
        self.inst.close()
        
        
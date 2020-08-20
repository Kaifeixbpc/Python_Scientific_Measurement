# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 00:08:06 2019

@author: paulv
"""

import visa
import numpy as np
rm=visa.ResourceManager()
import matplotlib.pyplot as plt
import time
func_list=(['set_DC_offset', 'set_waveshape', 'set_frequency', 'set_amplitude', 'ramp_offset', 'ramp_to_zero',  'get_oupt','printl'])

class AG33500B():
    
    
    
    
    def __init__(self,address='GPIB0::8::INSTR'):
        self.inst=rm.open_resource(address)
        
        pass
        
#        self.func_dic={'set_DC_offset':self.set_DC_offset,
#                        'set_amplitude':self.set_amplitude,
#                        'set_frequency':self.set_frequency,
#                        'ramp_volt':self.ramp_volt,
#                        'ramp_to_zero':self.ramp_to_zero}
        
    def set_DC_offset(self,offset):
        self.inst.write('SOUR:VOLT:OFFS %fV' % (offset))
        return False
    def set_waveshape(self,shape='SINE'):
        self.inst.write('SOUR:FREQ %f' % (shape))
        return False
    def set_frequency(self,frequency):
        self.inst.write('SOUR:FREQ %f' % (frequency))
        return False
    def set_amplitude(self,amplitude_by_mV):
        amplitude=amplitude_by_mV*0.001
        self.inst.write('SOUR:VOLT %f' % (amplitude))
        return False
    def ramp_volt(self,setp,stepsize=0.01,time_per_step=0.1):
        
        oupt=self.get_oupt()
        if oupt==setp:
            self.set_DC_offset(setp)
        elif setp>oupt:
            ramplist=np.arange(oupt,setp+stepsize,stepsize)
            print('The ramping time is about '+str(int(time_per_step*len(ramplist)))+'seconds')
            for offset in ramplist:
                self.set_DC_offset(offset)
                time.sleep(time_per_step)
        else:
            ramplist=np.arange(setp,oupt+stepsize,stepsize)[::-1]
            print('The ramping time is about '+str(int(time_per_step*len(ramplist)))+'seconds')
            for offset in ramplist:
                self.set_DC_offset(offset)
                time.sleep(time_per_step)
#        print('ramped to setpoint voltage')
        return False
    def ramp_to_zero(self):
        
        self.ramp_offset(0)
#        print('Output voltage from AG33500B is zero now!')
        return False
    def AG_scan_DCbias(self,scanlist,filename,data):
        for offset in scanlist:
            self.set_DC_offset(offset)
            with open(filename,'a') as file:
                file.write(data)
    
    def get_oupt(self):
        return float(self.inst.query('SOUR:VOLT:OFFS?'))
    
    def call_func(self, arg,*args):
        getattr(AG33500B,arg)(*args)
#        a=self.func_dic[arg].__get__(self, type(self))(*args)
#        return a
    def printl(self):
        print('hello world')
        return False
    
    def disconnect(self):
        self.inst.close()
        return False
        
    
#print(AG33500B.__dict__.keys())
    
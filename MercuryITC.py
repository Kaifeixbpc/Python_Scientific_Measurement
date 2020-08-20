# -*- coding: utf-8 -*-
"""
Created on May 24 21:13:51 2018 by Kaifei Kang
Updated on Dec 05 2018 by Egon Sohn



## Need to test iTC 1 & 2. Check all the daughter board assignment and test one by one


"""

import visa
rm=visa.ResourceManager()
import time
import numpy as np
func_list=['get_VTI_temp', 'get_Prob_temp','get_Pressure', 'get_NV', 'set_NV','set_Prob_temp', 'set_VTI_temp', 'ramp_temp']

class Mercury():
    
    def __init__(self,addr='ASRL6::INSTR'):
        
        self.addr = addr      
        self.func_dic={'get_VTI_temp':self.get_VTI_temp,
                       'get_Prob_temp':self.get_Prob_temp,
                       'get_NV':self.get_NV,
                       'set_Prob_temp':self.set_Prob_temp,
                       'set_VTI_temp':self.set_VTI_temp,
                       'ramp_temp':self.ramp_temp
                       }

    def get_VTI_temp(self):
        
        command="READ:DEV:MB1.T1:TEMP:SIG:TEMP"
        while True:
            try:
                VTI_T = self.get_value(command)
                VTI_T = VTI_T.split(":")[6].strip("K\n")
                VTI_T=float(VTI_T)
                break
            except:
                continue
        return VTI_T
    
    def get_Prob_temp(self):
        
        command="READ:DEV:DB8.T1:TEMP:SIG:TEMP"
        while True:
            try:
                Prob_T = self.get_value(command)
                Prob_T = Prob_T.split(":")[6].strip("K\n")
                Prob_T=float(Prob_T)
                break
            except:
                continue
        return Prob_T
    
    def get_Pressure(self):
        
        command="READ:DEV:DB5.P1:PRES:SIG:PRES"
        Pres = self.get_value(command)
        Pres = Pres.split(":")[6].strip("mB\n")
        return Pres
    
    def get_NV(self):
        
        command="READ:DEV:DB4.G1:AUX:SIG:PERC"
        Nvav = self.get_value(command)
        Nvav = Nvav.split(":")[6].strip("%\n")
        return Nvav    

    def set_NV(self,value):
        command="SET:DEV:DB5.P1:PRES:LOOP:FSET:%s" %value
        self.set_value(command)

    def set_Prob_temp(self,value):
        
        command=["SET:DEV:DB8.T1:TEMP:LOOP:RENA:OFF",
                  "SET:DEV:DB8.T1:TEMP:LOOP:TSET:%"%value]
        [self.set_value[a] for a in command]
        time.sleep(0.05)
        
        ProbT_now=self.get_Prob_temp()
        if np.abs(value-ProbT_now)<0.1:
            return False
        else:
            return True
        
    def set_VTI_temp(self,value):
        
        command=["SET:DEV:MB1.T1:TEMP:LOOP:RENA:OFF",
                 "SET:DEV:MB1.T1:TEMP:LOOP:TSET:%s"%value]
        [self.set_value[a] for a in command]
        time.sleep(0.05)
        VTIT_now=self.get_VTI_temp()
        if np.abs(value-VTIT_now)<0.1:
            return False
        else:
            return True    
        
    def ramp_temp(self, setT):
        
        CurrentT = self.get_Prob_temp()
        command=["SET:DEV:DB8.T1:TEMP:LOOP:RSET:%s" %2,
                 "SET:DEV:DB8.T1:TEMP:LOOP:TSET:%s"%CurrentT,
                 "SET:DEV:DB8.T1:TEMP:LOOP:RENA:ON",
                 "SET:DEV:DB8.T1:TEMP:LOOP:TSET:%s"%setT]
        [self.set_value[a] for a in command]
        
        if np.abs(setT-CurrentT)<0.1:
            return False
        else:
            return True         
           
    def get_value(self,command):
        
        self.inst=rm.open_resource(self.addr)
        data=self.inst.query(command)
        self.inst.close()
        return data

    def set_value(self,command):
        
        self.inst=rm.open_resource(self.addr)
        self.inst.query(command)
        self.inst.close()     
        
    def call_func(self, arg,*args):    
        self.__dict__[arg].__get__(self, type(self))(*args)     

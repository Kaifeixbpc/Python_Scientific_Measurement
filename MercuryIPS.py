# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 21:22:01 2019

@author: kaife
"""

import socket
import time
import numpy as np
func_list=['set_field', 'set_rate',  'get_field','get_magtemp']
class ips():
    
    def __init__(self):
        self.HOST = '192.168.1.4'    # The remote host
        self.PORT = 7020              # The same port as used by the server
        self.func_dic={'set_field':self.set_field,
                       'set_rate':self.set_rate,
                       'get_field':self.get_field,
                       'get_magtemp':self.get_magtemp}

####set ips parameters
                
    def set_field(self,field):


        command="SET:DEV:GRPZ:PSU:SIG:FSET:"+str(field)+'\n'
        self.command1=command.encode('utf-8')
        self.set_command(self.command1) 
        self.to_set()
        while True:
            try:
                if np.abs(field-float(self.get_field()))<0.0002:
                    return False
                else:
                    return True
                break
            except:
                continue
        
#    def scan_field(self, stop, measurement,time):
#        
#        self.set_field(stop)
#        while np.abs(stop-float(self.get_field()))<0.0002:
#        
#        
#        
#        
#        
#        pass
        
    def set_rate(self,rate):


        command="SET:DEV:GRPZ:PSU:SIG:RFST:"+str(rate)+'\n'
        self.command1=command.encode('utf-8')
        self.set_command(self.command1) 
        self.to_set()     
        
    def safe_set_field(self,field):
        while True:
            try:
                self.set_field(field)
                break
            except socket.error as msg:
                time.sleep(2)
                continue
###### aquire temperatures    
    def get_info(self):
        
        
        self.command='READ:SYS:CAT?\n'
        self.data=self.query_command(self.command)
        return self.data 
        print(self.data)
        
    def get_magtemp(self):

        self.command='READ:DEV:MB1.T1:TEMP:SIG:TEMP?\n'
        self.data=self.query_command(self.command)
        self.data=self.data.split(':')[6].strip('K')
        return self.data        
        
    
    def get_field(self):
        
        while True:
            try:
                self.command='READ:DEV:GRPZ:PSU:SIG:FLD?\n'
                self.data=self.query_command(self.command)
                self.data=self.data.split(':')[6].strip('T')
                return float(self.data)
                break
            except:
                continue

####################### universal command
    
    def query_command(self,command):
        
        HOST=self.HOST
        PORT=self.PORT
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        s.sendall(str.encode(command))
        data=s.recv(1024)
        data=data.decode('utf-8').strip('\n')
        return(data)
        s.close()
        
    def to_set(self):
        
        while True:
            try:
                self.set_command(b"SET:DEV:GRPZ:PSU:ACTN:HOLD\n")
                self.set_command(b"SET:DEV:GRPZ:PSU:ACTN:RTOS\n")
                break
            except socket.error as msg:
                continue
            
        
    def set_command(self,command):
        
        self.HOST = '192.168.1.4'    # The remote host
        self.PORT = 7020              # The same port as used by the server
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST,self.PORT))
        self.s.sendall(command)
        self.data=self.s.recv(1024)
        self.data=self.data.decode('utf-8').strip('\n')
        self.s.close()
        time.sleep(0.1)


#print(ips.__dict__.keys())
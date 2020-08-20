# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 20:43:16 2019

@author: kaife
"""
func_list=('printl','printn','printm')
import numpy as np
class dummy():
    
    def __init__(self):
    
        self.x=0
        
    def printn(self,x):
        self.x=x
        return False
    
    def printl(self):   
        y1=np.sin(self.x)
        return y1
    
    def printm(self):  
        y2=2*np.cos(self.x)
        return y2 
    
    def call_func(self, arg,*args):
        return getattr(self,arg)(*args)

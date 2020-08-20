# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:53:35 2019

@author: kaife
"""
from scipy import signal

class data_processing():
    
    def __init__(self):
        pass
    
    def smooth_data(self,data,strength=1,order=3):
        data=signal.savgol_filter(data,
                                  strength,
                                  order)
        return data
        
        
    
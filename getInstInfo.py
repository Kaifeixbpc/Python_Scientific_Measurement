# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 00:21:23 2019

@author: kaife
"""
import numpy as np
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QObject,pyqtSignal
import AG33500B,Keithley2400,SR830,dummy,MercuryIPS,MercuryITC


InstName=("Keithley2400", "SR830", "AG33500B","dummy","ips_ethernet")

KeFunc=Keithley2400.func_list
SRFunc=SR830.funclist
AGFunc=AG33500B.func_list
dumFunc=dummy.func_list
IpsFunc=MercuryIPS.func_list
ITCFunc=MercuryITC.func_list

import visa
rm=visa.ResourceManager()


FuncDic={"Keithley2400":KeFunc,
         "SR830":SRFunc,
         "AG33500B":AGFunc,
         "ips_ethernet":IpsFunc,
         "MercuryITC":ITCFunc,
         "dummy":dumFunc}

#NewFuncDic={}

def getInstruments():
    NewInstDic={}
    NewFuncDic={}
    info=[]
    InstrumentList=rm.list_resources()
    
    for i in range(len(InstrumentList)):
        try:
            inst=rm.open_resource(InstrumentList[i])
            infonew=inst.query('*IDN?')+InstrumentList[i]
            info.append(infonew)
            inst.close()
        except:
            pass
    
    for a in info:
       if "Keithley2400" in a:
            instname="Keithley2400"+a.split('\n')[1]
            NewFuncDic[instname]=KeFunc
            NewInstDic[instname]=Keithley2400.Keithley2400(a.split('\n')[1])
            
    for a in info:        
        if "Stanford" in a:
            instname="SR830"+a.split('\n')[1]
            NewFuncDic[instname]=SRFunc
            NewInstDic[instname]=SR830.SR830(a.split('\n')[1])
    for a in info:        
       if "Agilent" in a:
            instname="AG33500B"+a.split('\n')[1]
            NewFuncDic[instname]=AGFunc
            NewInstDic[instname]=AG33500B.AG33500B(a.split('\n')[1])
    for a in info:        
       if "ITC" in a:
            instname="ITC"+a.split('\n')[1]
            NewFuncDic[instname]=ITCFunc
            NewInstDic[instname]=AG33500B.AG33500B(a.split('\n')[1])            
            
            
    NewFuncDic['dummy']=dumFunc        
    NewFuncDic['MercuryIPS']=IpsFunc
    NewFuncDic['MercuryITC']=ITCFunc
    NewInstDic['dummy']=dummy.dummy()
    NewInstDic['MercuryIPS']=MercuryIPS.ips()
    NewInstDic['MercuryITC']=MercuryITC.Mercury()
    return NewInstDic,NewFuncDic

NewInstDic,NewFuncDic=getInstruments()
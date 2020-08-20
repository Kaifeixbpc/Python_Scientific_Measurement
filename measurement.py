# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:12:06 2019

@author: kaife
"""
import numpy as np
import time,os
from PyQt5 import QtCore
from PyQt5.QtCore import QObject,pyqtSignal
import getInstInfo


NewFuncDic=getInstInfo.NewFuncDic
NewInstDic=getInstInfo.NewInstDic

class measurement(QObject):
    
    finished =pyqtSignal()
    FN_out=pyqtSignal(str)
    LoopNum=pyqtSignal(int)
    LoopStatus=pyqtSignal(str)
    SingleMS=pyqtSignal(str)
    error_message=pyqtSignal(str)
    
    
    def __init__(self,seqlist='',loop1='',data_saving_file='',labels=''):
        super (measurement,self).__init__()

        self.sq_name=''
        self.seqlist=seqlist
        self.loop1=loop1
        self.running=True
        self.pause=False
        self.sig=True
        self.loop_sig=True
        self.ds_file=data_saving_file
        self.labels=labels
        
        self.info=[]
    
    
    def load_sequence(self,filename):
        
        self.sq_name=filename
        
        with open(filename,'r') as file:
            filetxt=file.readlines()
        return filetxt
            
    def add_sequence(self,sequence):
        
        with open(self.sq_name,'a') as file:
            file.write(sequence)     
            
#        self.load_sequence(self.sq_name)
        
    def delete_sequence(self,filename,selected):
        
        with open(filename,'r+') as file:
            filetxt=file.readlines()
        self.erase(filename)
        self.load_sequence(filename)
        
        with open(filename,'w') as file:
            for i in range(len(filetxt)):
                if i != selected:
                    file.write(filetxt[i])
#        print('file after deleting line')
        self.load_sequence(self.sq_name)    
                
    def erase(self,filename):
        open(filename, 'w').close()   
    


#    def get_source_parameter
    def exc_meas(self):
        print('Measuring')


    def meas_seq(self,mlines,x):

        data=''
#        print(mlines)
        for mline in mlines:
#            print(mline)
            if 'meas' in mline:
                mline=mline.strip('\n')
                mline=mline.split(' ')
#                print(mline)
                try:
#                    print(NewInstDic[mline[1]])
                    newd=NewInstDic[mline[1]].call_func(mline[2]) 
#                    print(newd)
                    data=data+str(newd) +' '
                except:
                    pass
#        print(data)
            
#        data=data+'\n'
        return data
    
    def sline_range(self,sline3):
#        print(sline3)
        s=sline3.strip('range:').split(',')
#        print(s)
        sRange=np.round(np.linspace(float(s[0]),float(s[1]),int(s[2])),4)
        
        return sRange
        
    def loop_control(self):
        
        if self.loop1!='':
            arb=self.loop1[0]
            self.loop1=self.loop1[1].split(' ')
            sctl=self.loop1[2].split(',')
            if not arb:
                second_range=np.round(np.linspace(float(sctl[0]),float(sctl[1]),int(sctl[2])),3)
            else:
                second_range=[float(x) for x in sctl[3:]]

            for i in range(len(second_range)):
                
                self.LoopNum.emit(i)
                
                if self.running:
                    
                    try:
                        print('Running loop'+str(i+1)+' '+self.loop1[0]+' '+self.loop1[1]+' '+str(second_range[i])+'!')
                        self.loop_sig=NewInstDic[self.loop1[0]].call_func(self.loop1[1],second_range[i])
                        
                        while self.loop_sig:
                            if self.running:
                                self.loop_sig=NewInstDic[self.loop1[0]].call_func(self.loop1[1],second_range[i])
                                self.LoopStatus.emit('Waiting for '+self.loop1[0]+' to reach the target Loop value %s!'%second_range[i])
                                time.sleep(1)
                            else:
                                break
                                self.running=False
                                self.finished.emit()
                                self.LoopStatus.emit('Measurement aborted @ Loop %s!'%i)
                        
                        current_path=os.path.split(self.ds_file)[0]
                        self.ds_file=os.path.join(current_path,self.loop1[3]%str(second_range[i]))    
                        with open(self.ds_file,'a') as file:
                            file.write(self.labels)
                        self.excute_seq()
                        
                    except Exception as error:
                        
                        self.error_message.emit(str(error))
                        self.running=False
                        break
                else:
                    self.LoopStatus.emit('Measurement aborted @ Loop %s!'%i)
                    
            self.finished.emit()
                
        else:
            self.excute_seq()
       
    
            
        

    
    
    def excute_seq(self):
        
        data=''
        self.ind=0
#        self.running=True
#        print(self.seqlist)
        for a in self.seqlist:
            mlines=[]
            
            if 'sour' in a:
                sline=a.split(' ')
                self.ind=self.seqlist.index(a)+1
#                print(self.seqlist[self.ind])
                
                while 'meas' in self.seqlist[self.ind]:
                    mlines.append(self.seqlist[self.ind])
                    self.ind+=1
                    if self.ind>len(self.seqlist)-2:
                        break
                mlines.append(self.seqlist[self.ind])
#                    
#                print(mlines)   

                sRange=self.sline_range(sline[3])
                wt=float(sline[4].strip('Wait'))

                if 'Keithley2400' in sline[1] or 'AG33500B' in sline[1]:
                    NewInstDic[sline[1]].call_func('ramp_volt',sRange[0])
                    
                self.FN_out.emit(self.ds_file)
                
                for i in range(len(sRange)):
#                    print(NewInstDic)
                    if self.running:
                        
                        
                        while self.sig:
                            
                            if self.running:   
                                self.sig=NewInstDic[sline[1]].call_func(sline[2],sRange[i])
                                
                                QtCore.QCoreApplication.processEvents()
                                newdata=self.meas_seq(mlines,sRange[i])
                                time.sleep(wt)
                                data=str(sRange[i])+' '+newdata+'\n'
                                if self.sig:
                                    self.SingleMS.emit('Waiting '+sline[1]+' to reach the set value %s'% sRange[i])
                                try:
                                    with open(self.ds_file,'a') as file:
                                        file.write(data)
                                except Exception as error:
                                    break
                                    self.error_message.emit('File error:'+str(error))
                                    self.finished.emit()
                                    
                                while self.pause:
                                    
                                    self.SingleMS.emit('Measurement paused!')
                                    time.sleep(1)
                            else:
                                break
                                self.pause=False
                                self.finished.emit() 
                                
                        self.sig=True
      
                    else:
                        self.pause=False
                        self.finished.emit()
                        

                     
                     
        self.finished.emit()
        
    def stop(self):
        self.running=False
        
    def start(self):
        self.running=True       
        
    def pause_seq(self):
        self.pause=True
        
    def resume_seq(self):
        self.pause=False

                
            
    
            
























#        
if __name__ == "__main__":
    f=measurement()
#    f.getInstruments()
#    f.getInstruments()
#    print(f.InstDic)
#    print(f.InstDic.keys())
#    for i in range(20):
#    f.InstDic['AG33500BGPIB0::8::INSTR'].call_func('set_DC_offset',0.02)
#        print(f.InstDic['SR830GPIB0::1::INSTR'].call_func('get_X'))
#        print(f.InstDic['SR830GPIB0::1::INSTR'].call_func('get_Y'))
#    print(f.InstDic['dummy'].call_func('printl'))
#    f.excute_seq()
##    mline='meas0: dummy printl'
##    a=f.meas_seq(mline)
##    print(a)
##  filename=r"C:\Users\kaife\Desktop\New Text Document (2).txt"
##    data='hello world'
##    M=measurement()
###    M.load_sequence(filename)
##    M.delete_sequence(filename,6)
###    for i in range(10):
###        M.delete_sequence(filename,6)
###        data1=data+str(i)+'\n'
###        M.add_sequence(data1)
        
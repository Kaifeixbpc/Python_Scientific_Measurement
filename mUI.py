# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 22:55:32 2019

@author: kaife
"""


from __future__ import division
import sys
import time
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets,QtTest, uic
import numpy as np
import sip
sip.setapi('QString', 2)
import worker

#############################################################self made modules
import measurement
import QueEditor as AddQue
import SecondExcite as SE_control
MSMT=measurement.measurement()







path = sys.path[0]
vtiTempControlGUI = path + r'\measurement.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(vtiTempControlGUI)

class main(QtWidgets.QMainWindow, Ui_MainWindow,QtWidgets.QFileDialog,QtWidgets.QMessageBox,QtWidgets.QInputDialog):
    
    def __init__(self):
        super(main, self).__init__()
        
        self.thread=QThread()
        self.obj = worker.Worker() 
        self.obj.moveToThread(self.thread)
        
        
#        MSMT.moveToThread(self.thread)
        self.thread.started.connect(self.run_seq)
#        self.thread.start()
        self.setupUi(self)
        self.statusBar().showMessage('hello!')

#######################################################


        
        self.fig_dict={}
        self.colx_dict={}
        self.coly_dict={}
        self.seq_dict={}

#############Button and labels    
#################################################################        
        

        
        self.LoadSeq.clicked.connect(self.Load_Seq)
        self.NewSeq.clicked.connect(self.SeqGetItem)
        self.ClearSeq.clicked.connect(self.clear_que)
        self.AddSeqItem.clicked.connect(self.se_control)
        self.AbortSeq.clicked.connect(self.Abort_MS)
        self.StartSeq.clicked.connect(self.Start_MS)
        self.PauseSeq.clicked.connect(self.Pause_MS)
        self.StartSeq.clicked.connect(self.run_seq)
        self.QueList.addItem('Secondary_control_disabled!\n')
        self.statusBar().setStyleSheet("QStatusBar{padding-left:8px;background-color:black;color:yellow;font: 75 16pt 'Arial';}")
     
    
    def STBar(self,message):
        
        self.statusBar().setStyleSheet("QStatusBar{padding-left:8px;background-color:black;color:yellow;font: 75 16pt 'Arial';}")
        self.statusBar().clearMessage()
        self.statusBar().showMessage(message)

        
    def clear_que(self):
        self.QueList.clear()
        self.QueList.addItem('Secondary_control_disabled!\n')
        
    def show_message(self,message):
        self.information(None,'Error!',message)
            
        
        
        
    def Load_Seq(self):
        
        filename=self.getOpenFileName()[0]
        if filename !='':
            lines=MSMT.load_sequence(filename)
            [self.QueList.addItem(a) for a in lines]
            
        
    def Abort_MS(self):
        
        self.MS_Status=False
        self.STBar('Measurement aborted!')

    def Pause_MS(self):
        
        self.MS_Status=False
        self.STBar('Measurement paused!')
        
    def Start_MS(self):
    
        self.MS_Status=True
        self.STBar('Measurement started!')
        
    def SeqGetItem(self):
        
        que_file = self.getOpenFileName()[0]
        if que_file != '':
            newWin=AddQue.QueDialog()
            value=newWin.getResults(que_file)    
            lines=MSMT.load_sequence(que_file)
            [self.QueList.addItem(a) for a in lines]
            print(value)
        
    def GetItem(self):
       items = ("Keithley2400", "SR830", "AG33500B", "Oxford Teslatron")
		
       item, ok = self.getItem(self, "Select Instruments", 
          "Source instrument:", items, 0, False)
       if ok and item:
          print(item)
          
    def se_control(self):
        
        w=SE_control.SE_Dialog()
        value=w.getResults()
        print(value)
        
    def run_seq(self):
        
        seqlist=[self.QueList.item(i).text() for i in range(self.QueList.count())]
        
        if seqlist[0]=='Secondary_control_disabled!\n':
            self.statusBar().showMessage('Just a single measurement!')
#            
#            for i in range(len(seqlist)):
#                
            if 'sour' in seqlist[1]:
                self.statusBar().showMessage('Good to start!')
                sline=seqlist[1]
                mlines=seqlist[2:]
                MSMT.excute_seq(sline,mlines)
















if __name__ == "__main__":
    

    
    
    
    app = QtWidgets.QApplication([])
    window = main()    
    window.show()
#    timer = QtCore.QTimer()
#    timer.timeout.connect(window.refresh_input)
#    timer.start(100)    
    
    
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 16:15:50 2019

@author: kaife
"""
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets,QtTest, uic
import getInstInfo
NewFuncDic=getInstInfo.NewFuncDic
NewInstDic=getInstInfo.NewInstDic
path = sys.path[0]

AddQueUI = path + r'\Add_queue.ui'
AddQueDialog, QtBaseClass = uic.loadUiType(AddQueUI)


class QueDialog(QtWidgets.QDialog, AddQueDialog):
    
    def __init__(self):
        
        super(QueDialog, self).__init__()
        self.setupUi(self)
        self.meas=0
        self.fname=''
        self.info=[]
        self.NewInstDic=NewInstDic
        self.NewFuncDic=NewFuncDic
        
        self.SourceName.addItems(self.NewInstDic.keys())
        self.SourceName.currentIndexChanged.connect(self.refresh_S)
        self.MeasInst.addItems(self.NewInstDic.keys())
        self.MeasInst.currentIndexChanged.connect(self.refresh_M)
        self.SourceRange.setText('-100,100,201')
        self.WaitTime.setValue(0.3)
        self.AddMeas.clicked.connect(self.add_measure)
        
        self.refresh_S()
        self.refresh_M()
        
        
    def add_measure(self):
        
        val5 = self.MeasInst.currentText()
        val6 = self.MeasFunc.currentText()
        Val='meas'+str(self.meas)+': '+val5+' '+ val6
        self.QueList.addItem(Val)
        self.meas+=1
    
    def write_queue(self,filename):
        

        l1 = self.SourceName.currentText()+' '
        l2 = self.SourceFunc.currentText()+' '
        l3 = self.SourceRange.text().split(',')
        l4=''
        for i in range(self.QueList.count()):
            l4=l4+self.QueList.item(i).text()+'\n'
        slist_str='range:'+self.SourceRange.text()+' '
            
        
        wait = 'Wait'+str(self.WaitTime.value())
        sour = 'sour '+l1+l2+slist_str+wait+'\n'
#        sourlist=np.linspace(float(l3[0]),float(l3[1]),int(l3[2]))
        meas=l4
        queue=sour+meas
        
#        print(queue)
#        return queue
        with open(filename,'a') as file:
            file.write(queue)
            

        
        
    def getResults(self,filename):
        
        if self.exec_() == self.Accepted:
            self.write_queue(filename)
        else:
            return None

    def comboChanged(self):
        self.updateComboData()
        self.update()

     
    def refresh_S(self):
        b=self.SourceName.currentText()
        print(b)
        self.Sfunc=self.NewFuncDic[b]
        
        self.SourceFunc.clear()
        self.SourceFunc.addItems(self.Sfunc)
        
    def refresh_M(self):
        b=self.MeasInst.currentText()
        self.Mfunc=self.NewFuncDic[b]
        self.MeasFunc.clear()
        self.MeasFunc.addItems(self.Mfunc)



        
if __name__=='__main__':
    
    app = QtWidgets.QApplication([])
    window = QueDialog()    
    window.show()

    sys.exit(app.exec_())
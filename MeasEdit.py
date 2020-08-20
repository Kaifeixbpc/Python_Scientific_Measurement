# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 13:23:57 2019

@author: kaife
"""

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
AddQueUI = path + r'\MeasEdit.ui'
AddQueDialog, QtBaseClass = uic.loadUiType(AddQueUI)


class QueDialog(QtWidgets.QDialog, AddQueDialog):
    
    def __init__(self):
        
        super(QueDialog, self).__init__()
        self.setupUi(self)
        self.meas=0
        self.fname=''
        
        self.NewInstDic=NewInstDic
        self.NewFuncDic=NewFuncDic
        self.MeasInst.addItems(self.NewInstDic.keys())
        self.MeasInst.currentIndexChanged.connect(self.refresh_M)
        self.AddAfter.setChecked(False)
        self.Delete.setChecked(False)
#        self.error=''
        self.refresh_M()
        

    def write_queue(self,meas_num):
        

        l1 = self.MeasInst.currentText()+' '
        l2 = self.MeasFunc.currentText()
        l3=self.AddAfter.isChecked()
        l4=self.Delete.isChecked()
        meas=meas_num+l1+l2
        return meas,l3,l4
            
    def show_meas(self,que):
        que=que.strip('\n')
        que=que.split(' ')
#        print(que)
        index1=self.MeasInst.findText(que[1], QtCore.Qt.MatchFixedString)
        self.MeasInst.setCurrentIndex(index1)
        self.refresh_M()
        
        index2=self.MeasFunc.findText(que[2], QtCore.Qt.MatchFixedString)
        self.MeasFunc.setCurrentIndex(index2)

        
    def getResults(self,meas_num):
        
        if self.exec_() == self.Accepted:
            return(self.write_queue(meas_num))
        else:
            return None

     

    def refresh_M(self):
        try:
            self.Mfunc=self.NewFuncDic[self.MeasInst.currentText()]
            self.MeasFunc.clear()
            self.MeasFunc.addItems(self.Mfunc)
        except:
            return ('Selected equipment is not connected, please check connections or switch equipments!')



        
if __name__=='__main__':

#    print(rm.list_resources())
    app = QtWidgets.QApplication([])
    window = QueDialog()    
    window.show()

    sys.exit(app.exec_())
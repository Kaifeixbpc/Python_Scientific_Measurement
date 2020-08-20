# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:44:19 2019

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

AddQueUI = path + r'\SourEdit.ui'
AddQueDialog, QtBaseClass = uic.loadUiType(AddQueUI)


class QueDialog(QtWidgets.QDialog, AddQueDialog):
    
    def __init__(self):
        
        super(QueDialog, self).__init__()
        self.setupUi(self)
        self.meas=0
        self.fname=''
        self.NewInstDic=NewInstDic
        self.NewFuncDic=NewFuncDic
        
        self.SourceName.addItems(self.NewInstDic.keys())
        self.SourceName.currentIndexChanged.connect(self.refresh_S)
        self.SourceRange.setText('-100,100,201')
        self.WaitTime.setValue(0.3)
        self.refresh_S()


        
    def show_sour(self,que):
        que=que.strip('\n')
        
        que=que.split(' ')
#        print(que)
        index1=self.SourceName.findText(que[1], QtCore.Qt.MatchFixedString)
        self.SourceName.setCurrentIndex(index1)
        self.refresh_S
        index2=self.SourceFunc.findText(que[2], QtCore.Qt.MatchFixedString)
        self.SourceFunc.setCurrentIndex(index2)
        
        self.SourceRange.setText(que[3].strip('range:'))
        self.WaitTime.setValue(float(que[4].strip('Wait')))
        
#    def update_combo(self,text):
        
        
    
    def write_queue(self):
        

        l1 = self.SourceName.currentText()+' '
        l2 = self.SourceFunc.currentText()+' '
#        l3 = self.SourceRange.text().split(',')
#        l4=''
#        for i in range(self.QueList.count()):
#            l4=l4+self.QueList.item(i).text()+'\n'
        slist_str='range:'+self.SourceRange.text()+' '
            
        
        wait = 'Wait'+str(self.WaitTime.value())
        sour = 'sour '+l1+l2+slist_str+wait+'\n'
        return sour

            

        
        
    def getResults(self):
        
        if self.exec_() == self.Accepted:
            return(self.write_queue())
        else:
            return None

    def refresh_S(self):
        try:
            self.Sfunc=self.NewFuncDic[self.SourceName.currentText()]
            self.SourceFunc.clear()
            self.SourceFunc.addItems(self.Sfunc)
        except:
            return ('Selected equipment is not connected, please check connections!')
        
#    def refresh_M(self):
#        self.Mfunc=FuncDic[self.MeasInst.currentText()]
#        self.MeasFunc.clear()
#        self.MeasFunc.addItems(self.Mfunc)


        
if __name__=='__main__':
    
    app = QtWidgets.QApplication([])
    window = QueDialog()    
    window.show()

    sys.exit(app.exec_())
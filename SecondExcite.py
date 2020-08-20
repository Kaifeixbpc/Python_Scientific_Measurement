# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 19:53:11 2019

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
path = sys.path[0]
import QueEditor
SecondExiteUI = path + r'\SecondExite2.ui'
SecondExiteDialog, QtBaseClass = uic.loadUiType(SecondExiteUI)



class SE_Dialog(QtWidgets.QDialog, SecondExiteDialog):
    
    def __init__(self):
        
        super(SE_Dialog, self).__init__()
        self.setupUi(self)
        
        self.ExcInst1.addItems(QueEditor.NewInstDic)
        self.ExcInst1.currentIndexChanged.connect(self.refresh)
#        self.ExcInst2.addItems(InstName)
#        self.ExcInst3.addItems(InstName)
        self.current_setting=[]
        self.ExcFunc1.addItems(QueEditor.NewFuncDic)
        self.ListContr1.setChecked(False)
        self.Arbitrary.setChecked(False)
        self.refresh()
        
    def getResults(self):
        
        if self.exec_() == self.Accepted:
            print('hello')
            # get all values
            val1 = self.ExcInst1.currentText()
            val2 = self.ExcFunc1.currentText()
            val5 = self.AList.text()
            Val4=self.ListExc1.text()
            Val6=self.BaseName.text()
            
            try:
                Val4_list=np.linspace(float(Val4[0]),float(Val4[1]),int(Val4[2]))
                print(Val4_list)
            except:
                pass              
            val3=False
            val=False
#            print(val1, val2, Val4)
            
            if self.ListContr1.isChecked():
                print('List Control enabled!')
                val3=True
            else:
                val3=False
            if self.Arbitrary.isChecked():
                print('Arbitrary list!')
                val=True
            else:
                val=False
                    
                
            self.current_setting=(val3,val,val1+' '+val2+' '+Val4+','+val5+' '+Val6)
            return self.current_setting
        else:
            return None
        
    def show_Exc(self,current_setting):
        
        sour_set=current_setting[2].split(' ')
        self.ListContr1.setChecked(current_setting[0])
        self.Arbitrary.setChecked(current_setting[1])
        
        index1=self.ExcInst1.findText(sour_set[0], QtCore.Qt.MatchFixedString)
        self.ExcInst1.setCurrentIndex(index1)
#        self.refresh_S
        index2=self.ExcFunc1.findText(sour_set[1], QtCore.Qt.MatchFixedString)
        self.ExcFunc1.setCurrentIndex(index2)
        sourlist=sour_set[2].split(',')
        nplist=','.join(sourlist[:3])
        ablist=','.join(sourlist[3:])
        
        self.ListExc1.setText(nplist)
        self.AList.setText(ablist)
        self.BaseName.setText(sour_set[3])
        
#        self.WaitTime.setValue(float(que[4].strip('Wait')))  
        
        
        
        
    def refresh(self):
        
        
        self.Sfunc=QueEditor.NewFuncDic[self.ExcInst1.currentText()]
        self.ExcFunc1.clear()
        self.ExcFunc1.addItems(self.Sfunc)
        
#        self.Mfunc=QueEditor.FuncDic[self.MeasInst.currentText()]
#        self.MeasFunc.clear()
#        self.MeasFunc.addItems(self.Mfunc)
#        
#        
#if __name__=='__main__':
#    
#    app = QtWidgets.QApplication([])
#    window = SE_Dialog()    
#    window.show()
#    sys.exit(app.exec_())
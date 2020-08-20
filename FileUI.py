# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 00:24:07 2019

@author: kaife
"""

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,QtTest, uic

path = sys.path[0]

FileUI = path + r'\file_saving.ui'
Filedialog, QtBaseClass = uic.loadUiType(FileUI)

class FileSaving(QtWidgets.QDialog,Filedialog):
    
    def __init__(self,directory,name,title):
        
        super(FileSaving, self).__init__()
        self.setupUi(self)
        self.dir=directory
        self.nam=name
        self.title=title
        
        self.Directory.setText(self.dir)
        self.Filename.setText(self.nam)
        self.Title.setText(self.title)
        
        self.FileDir.clicked.connect(self.get_dir)
        
    def get_dir(self):
        
        
        try:
            self.dir=QtWidgets.QFileDialog.getExistingDirectory()
            self.Directory.setText(self.dir)
            self.Title.setText(self.title)
            print(self.dir)
        except:
            print('Dir not found!')
        
    def FgetResults(self):
        
        if self.exec_() == self.Accepted:
            
            self.dir=self.Directory.text()
            self.nam=self.Filename.text()
            self.title=self.Title.text()
            
            if self.dir!='' and self.nam!='':
                save_dir=self.dir+'/'+self.nam
                os.path.normpath(save_dir)
                if not os.path.exists(save_dir):
                    with open(save_dir,'a') as file:
                        file.write(self.title+'\n')
                    return self.dir,save_dir,self.nam,self.title
        else:
            return None
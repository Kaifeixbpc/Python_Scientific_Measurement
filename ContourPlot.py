# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:41:48 2019

@author: kaife
"""

from __future__ import division
import sys
import time,os
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtGui, QtWidgets,QtTest, uic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import pyqtgraph as pg
import sip
import datetime
import pandas as pd
sip.setapi('QString', 2)

mpl.rcParams['font.size']=22
mpl.rcParams['legend.fontsize']=10
mpl.rcParams['lines.linewidth']=1.5
mpl.rcParams['figure.figsize']=(8,6)
mpl.rcParams['xtick.major.size']=5
mpl.rcParams['ytick.major.size']=5
mpl.rcParams['font.family']='Arial'
mpl.rcParams['mathtext.fontset'] = "stixsans"
path = sys.path[0]
vtiTempControlGUI = path + r'\ContourPlot.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(vtiTempControlGUI)

class ContourPlot(QtWidgets.QMainWindow, Ui_MainWindow,QtWidgets.QFileDialog,QtWidgets.QMessageBox,QtWidgets.QInputDialog):
    
    def __init__(self):
        super(ContourPlot, self).__init__()
#        super().__init__()
        self.setupUi(self)

#        self.thread=QThread()
        
        self.loop1=''
        self.saving_dir=r''
        self.newdirect=''
        self.newname=''
        self.newtitle='x y1 y2 y3 y4'
        self.file_list=[]
        self.directory=''
        self.File=[]
        self.basename=''
        self.dlist=[]
        self.header=[]
        self.dlength=0
        self.dwidth=0
        self.xdata=[];self.ydata=[];self.zdata=[]
        self.get_matrix_data()
        
#        self.Clr.clicked.connect(self.get_matrix_data)
        self.startPlot.clicked.connect(self.update)
        self.OpenFile.clicked.connect(self.open_file)
        
        self.cm=plt.colormaps()
        self.Cmap.addItems(self.cm)
#        self.baseName.textChanged.connect(self.get_matrix_data)
#        self.Xlist.textChanged.connect(self.get_matrix_data)
        
        self.yGain.returnPressed.connect(self.update_graph)
        self.zGain.returnPressed.connect(self.update_graph)
        self.Ycol.valueChanged.connect(self.update_graph)
        self.Zcol.valueChanged.connect(self.update_graph)
        
        self.skipRow.returnPressed.connect(self.update)
        self.skipFoot.returnPressed.connect(self.update)
        self.Xlabel.returnPressed.connect(self.update_graph)
        self.Ylabel.returnPressed.connect(self.update_graph)
        self.Zlabel.returnPressed.connect(self.update_graph)
        self.Cmap.currentTextChanged.connect(self.update_graph)
        
        self.fig = plt.figure()
        self.ax =self.fig.add_subplot(111)
        self.fig.tight_layout()
        self.canvas=FigureCanvas(self.fig)
        self.canvas.draw()
        
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.plot_window, coordinates=True)        
        self.mpl.addWidget(self.toolbar)  
        self.mpl.addWidget(self.canvas)   
        
        self.tabWidget.currentChanged.connect(self.change_tab)
################################################################################
        self.OpenFile_2.clicked.connect(self.load_files)
        self.file_dic={}
        self.Clr2.clicked.connect(self.FileList.clear)
        self.startPlot_2.clicked.connect(self.lineplot)
        self.FileList.itemDoubleClicked.connect(self.remove_item)
        
        self.Xlist_2.returnPressed.connect(self.lineplot)
        self.yGain_2.returnPressed.connect(self.lineplot)
        self.zGain_2.returnPressed.connect(self.lineplot)
        self.Ycol_2.valueChanged.connect(self.lineplot)
        self.Zcol_2.valueChanged.connect(self.lineplot)
        
        self.skipRow_2.returnPressed.connect(self.lineplot)
        self.skipFoot_2.returnPressed.connect(self.lineplot)
        self.Xlabel_2.returnPressed.connect(self.lineplot)
        self.Ylabel_2.returnPressed.connect(self.lineplot)
#        self.
######################################for contour
        
    def open_file(self):
        
        f = self.getOpenFileName()[0]
        if os.path.exists(f):
            self.baseName.setText(f)
            df=pd.read_csv(f,sep=' ',header=0,index_col=False)
            self.shape=df.shape
#            print(df.shape)
            self.dlength=df.shape[0]
            self.dwidth=df.shape[1]
            self.Ycol.setMaximum(int((self.shape[1])-1))
            self.Zcol.setMaximum(int((self.shape[1])-1))
     
        
        
    def get_dllist(self):

        code='global dlist;dlist={}'.format(self.Xlist.text())
        print(code)
        exec(code)
        global dlist
        print(dlist)
        return dlist
        
    def get_file(self,basename,dlist):
        
        basename=str(basename)
        self.File=[]
        for i in dlist:
            f=basename.format(i)
            if f!=basename and os.path.exists(f) :
                self.File.append(f)
        return self.File        
        
        
        
    def rmmpl(self):
        self.mpl.removeWidget(self.canvas)
        self.mpl.removeWidget(self.toolbar)
        self.canvas.close()
        
    def admpl(self,fig):
        
        self.canvas = FigureCanvas(fig)
        self.mpl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, 
                self, coordinates=True)
#        self.extend_toolbar()
        self.mpl.addWidget(self.toolbar)
        self.mpl.addWidget(self.canvas)
    
    def newfig(self):
        fignew = plt.figure()
        return fignew
    
    


    
    def get_header(self):
        df = pd.read_csv(self.File[0],sep=' ',header=0,index_col=False,skiprows=int(self.skipRow.text()))
        return list(df.columns)
                
    def get_matrix_data(self):
        
#        fulld=[]
        self.dlength_new=self.dlength-int(self.skipRow.text())
        
        self.ydata=[]
        self.zdata=[]
        basename=self.baseName.toPlainText()
#        dlist_para=self.Xlist.text().split(',')
        dlist=self.get_dllist()
        File=self.get_file(basename,dlist)
        
        
#        if len(File)!=oldFile:
            
        for j in range(int(self.dwidth)):
            
            
            try:
                self.x=np.zeros((len(File),int(self.dlength_new)))
                self.y=np.zeros((len(File),int(self.dlength_new)))
                self.z=np.zeros((len(File),int(self.dlength_new)))        
                for i in range(len(File)): 
                    df = pd.read_csv(File[i],sep=' ',header=0,index_col=False,skiprows=int(self.skipRow.text()))
                    I=df.values[:,j]
                    V=df.values[:,j]             
        
                    self.x[i]=(np.repeat(dlist[i],len(I)))
                    self.y[i]=I
                    self.z[i]=V     
                
            except Exception as error:
                print(error)
                self.x=np.zeros((1,1))
                self.y=np.zeros((1,1))
                self.z=np.zeros((1,1))
                
            self.ydata.append(self.y)
            self.zdata.append(self.z)

         

    
    
    
    
    def pcolormesh(self):
        
        try:
            self.fig=plt.figure()
            self.ax =self.fig.add_subplot(111)
            self.ax.clear()
            self.rmmpl()
            self.admpl(self.fig)
            
            try:
#                skiprow=int(self.skipRow.text())
#                skipfoot=int(self.skipFoot.text())  
                ygain=float(self.yGain.text())
                zgain=float(self.zGain.text())
                
                cols=(int(self.Ycol.value()),int(self.Zcol.value()))
                
                self.x1=self.x
                self.y1=self.ydata[cols[0]]*ygain
                self.z1=self.zdata[cols[1]]*zgain
                
            except Exception as error:
                print(error)
                self.x1=self.x
                self.y1=self.y
                self.z1=self.z

#            cm=cont.get_cmap()
            cont=self.ax.pcolormesh(self.x1,self.y1,self.z1,cmap=self.Cmap.currentText()) 
#            plt.colorbar(cont,label='').remove()
            plt.colorbar(cont,fraction=0.05,label=self.Zlabel.text())
            
            self.ax.set_xlabel(self.Xlabel.text())
            self.ax.set_ylabel(self.Ylabel.text())
            self.canvas.draw()
            self.fig.tight_layout()
            
        except Exception as error:
            print(error)
            
    def update(self):
        
        self.get_matrix_data()
        self.pcolormesh()
        
    def continuous_update(self):
        
        if self.Cont.isChecked():
            try:
                self.get_matrix_data()
                self.pcolormesh()
            except:
                pass
    def update_graph(self):
        self.pcolormesh()


################################################for lineplots
            
    def load_files(self):
        f = self.getOpenFileNames()[0]
        print(f)
        for i in range(len(f)):
            print(f[i])
            indx=os.path.split(f[i])[1]
            self.FileList.addItem(str(indx))
            self.file_dic[indx]=f[i]
     
    def get_color(self):
        num=int(self.FileList.count())
        print(num)
        if num%2==0:
            return num
        else:
            return num+1
            
    def lineplot(self):
        
        
        colord=self.get_color()
        
        colorlist=plt.cm.RdBu_r(np.linspace(0,1,colord))
        leg=self.leglist()
        self.fig=plt.figure()
        self.ax =self.fig.add_subplot(111)
        self.ax.clear()
        self.rmmpl()
        self.admpl(self.fig)

        try:
            skiprow=int(self.skipRow_2.text())
            skipfoot=int(self.skipFoot_2.text())  
            ygain=float(self.yGain_2.text())
            zgain=float(self.zGain_2.text())
            cols=(int(self.Ycol_2.value()),int(self.Zcol_2.value()))
            
            for i in range(self.FileList.count()): 
                
                df = pd.read_csv(self.file_dic[self.FileList.item(i).text()],sep=' ',header=0,index_col=False,skiprows=skiprow,skipfooter=skipfoot )
                I=df.values[:,cols[0]]*ygain
                V=df.values[:,cols[1]]*zgain
                
                self.ax.plot(I,V,color=colorlist[i],label=leg[i])
                
            self.ax.set_xlabel(self.Xlabel_2.text())
            self.ax.set_ylabel(self.Ylabel_2.text())
            self.ax.tick_params(direction='in', length=6, width=1, colors='k',
               grid_color='r', grid_alpha=0.5)
            self.ax.legend(fontsize=15, ncol=1).set_draggable(True)
            
            self.canvas.draw()
            self.fig.tight_layout()
        
        
        except  Exception as error   :
            print(error)

#    def get_labels(self):
#        l=self.Xlist_2.text()
#        l='global labels;labels={}'.format(self.Xlist_2.text())
            

    def remove_item(self):
        self.FileList.takeItem(self.FileList.currentRow())
        self.lineplot()


    def change_tab(self):
        indx=self.tabWidget.currentIndex()
        if indx==0:
            self.pcolormesh()
        elif indx==1:
            self.lineplot()
            
    def leglist(self):
        
        code='global dlist;dlist={}'.format(self.Xlist_2.text())
        print(code)
        exec(code)
        global dlist
        print(dlist)
        return dlist






            
if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    window = ContourPlot()    
#    main.self.setupUi(self)
    window.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(window.continuous_update)
    timer.start(1000)    
    
    
    sys.exit(app.exec_())

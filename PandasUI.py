# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:24:54 2019

@author: kaife
"""
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,QtTest, uic
#from QtWidgets import QTableWidgets
import pandas as pd
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import pyqtgraph as pg
import matplotlib.pyplot as plt
import matplotlib as mpl
import data_processing

DTP=data_processing.data_processing()
mpl.rcParams['font.size']=22
mpl.rcParams['legend.fontsize']=10
mpl.rcParams['lines.linewidth']=1.5
mpl.rcParams['figure.figsize']=(8,6)
mpl.rcParams['xtick.major.size']=5
mpl.rcParams['ytick.major.size']=5
mpl.rcParams['font.family']='Arial'
mpl.rcParams['mathtext.fontset'] = "stixsans"


path = sys.path[0]
dataGUI = path + r'\data_Analyzer.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(dataGUI)
class main(QtWidgets.QMainWindow, Ui_MainWindow,QtWidgets.QFileDialog,QtWidgets.QMessageBox):
    
    def __init__(self):
        super(main, self).__init__()
        self.setupUi(self)

        self.LoadF.clicked.connect(self.load_data)
        self.editCol.clicked.connect(self.set_column_value)
        self.Cmd.returnPressed.connect(self.set_column_value)
        self.df=pd.DataFrame()
        self.dx=[]
        self.dy=[]
        
    def load_data(self):
        
        file=self.getOpenFileName()[0]
        
        if os.path.exists(file):
            self.df=pd.read_csv(file,sep=' ',index_col=False)
            self.dx=(self.df.columns)
            self.dy=(self.df.index)
            
            self.DataTable.setRowCount(len(self.dy))
            self.DataTable.setColumnCount(len(self.dx))
            self.DataTable.setHorizontalHeaderLabels(self.dx)
            self.update_data()
            
    def update_data(self):
            for i in range(len(self.dy)):
                for j in range(len(self.dx)):
                    self.DataTable.setItem(i,j,QtWidgets.QTableWidgetItem(str(self.df.iloc[i,j])))        
    
    
  
    def show_message(self,message):
        self.information(None,'Error!',message)
        
    def set_column_value(self):
        df=self.df
        command=self.Cmd.text()
        try:
            exec(command)
            self.df=df
            self.update_data()
        except Exception as error:
#            self.show_message(error)
            print(error)

        
        
        
#        for items in self.DataTable.selectedItems():
#            txt=items.text()
#            try:
#                txt=str(5*float(txt))
#                items.setText(txt)
#            except:
#                pass















    def add_fig(self,name,fig,xcol,ycol):
        
        self.fig_dict[name] = fig
        self.colx_dict[name] = xcol
        self.coly_dict[name] = ycol
        self.PlotList.addItem(name)
        
    def change_fig(self,item):
        
        text1 = item.text()
        print(text1)
        self.rmmpl()
        self.admpl(self.fig_dict[text1])
        self.xaxis = self.colx_dict[text1]
        self.yaxis = self.coly_dict[text1]
        
        self.ax=self.fig_dict[text1].add_subplot(111)
        
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





    def plot_data(self):
#        print(self.f)
        try:
            figs=self.newfig()
            self.ax=figs.add_subplot(111)
            filename=self.f
            self.xaxis=self.Xaxis.value()
            self.yaxis=self.Yaxis.value()
            self.skip=self.SkipRows.value()
            self.foot=self.SkipFoot.value()
            self.xg = float(self.Xgain.text())
            self.yg = float(self.Ygain.text())
            self.xl = self.Xlabel.text()
            self.yl = self.Ylabel.text()
            self.smooth_factor=self.SmoothFac.value()*2+1
            data=pd.read_csv(filename,sep=' ',header=None,skiprows=self.skip,skipfooter=self.foot)
            
            x=data.values[:,self.xaxis]
            y=data.values[:,self.yaxis]
            
            if self.XTime.isChecked():
                x=self.get_timed(data.values[:,0],data.values[:,1])
                self.xl='Date and Time'
            if self.Smooth.isChecked():
                y=DTP.smooth_data(y,self.smooth_factor)
            try:                                                                                                                                                                                                                   
                x=x*self.xg
            except:
                pass
            if self.LogScale.isChecked():
                self.ax.clear()
                self.ax.plot(x,y*self.yg,'k',label=self.CurveLabel.text())
            else:
                self.ax.clear()
                self.ax.plot(x,y*self.yg,'k',label=self.CurveLabel.text())
                
            self.ax.set_xlabel(self.xl)
            self.ax.set_ylabel(self.yl)
            figs.tight_layout()
            self.rmmpl()
            self.admpl(figs)
            self.canvas.draw()
            
            
            self.add_fig('Plot'+str(self.num),figs,self.xaxis,self.yaxis)        
            self.num += 1      
            self.STBar('Plots exceuted!')
        except Exception as e:
            self.show_message(str(e)+', please check the data file and correct properties!')
        











if __name__ == "__main__":

    
    app = QtWidgets.QApplication([])
    window = main()    
    window.show()   
    
    
    sys.exit(app.exec_())
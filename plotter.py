# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:17:53 2019

@author: kaife
"""


import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import pyqtgraph as pg
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


mpl.rcParams['font.size']=22
mpl.rcParams['legend.fontsize']=10
mpl.rcParams['lines.linewidth']=1.5
mpl.rcParams['figure.figsize']=(8,6)
mpl.rcParams['xtick.major.size']=5
mpl.rcParams['ytick.major.size']=5
mpl.rcParams['font.family']='Arial'
mpl.rcParams['mathtext.fontset'] = "stixsans"
from lineplot import main


class plotter():
    
    def __init__(self):
                
        self.f=''
        self.header=[]
        self.xaxis=0
        self.yaxis=1
        self.skip=2
        self.SkipRows.setValue(0)
        self.SkipRows.setMaximum(1000)
        self.SkipFoot.setValue(0)
        self.SkipFoot.setMaximum(1000)
        self.Xaxis.setValue(0)
        self.Yaxis.setValue(3)
        self.Xaxis.valueChanged.connect(self.update_labels)
        self.Yaxis.valueChanged.connect(self.update_labels)
        self.SmoothFac.setValue(2) 

    
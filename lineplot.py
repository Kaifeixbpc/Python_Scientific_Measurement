from __future__ import division
import sys,os,datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets, uic
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sip;sip.setapi('QString', 2)
import pyqtgraph as pg

from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,NavigationToolbar2QT as NavigationToolbar)
mpl.rcParams['font.size']=22;mpl.rcParams['legend.fontsize']=10;mpl.rcParams['lines.linewidth']=2
mpl.rcParams['xtick.major.size']=5;mpl.rcParams['ytick.major.size']=5;mpl.rcParams['font.family']='Arial';mpl.rcParams['mathtext.fontset'] = "stixsans"
#############################################################self made modules
import measurement
import data_processing
import QueEditor as AddQue
import SecondExcite as SE_control
import FileUI
import SourEdit
import MeasEdit
DTP=data_processing.data_processing()
#####################################################################
path = sys.path[0]
vtiTempControlGUI = path + r'\lineplot.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(vtiTempControlGUI)

class main(QtWidgets.QMainWindow, Ui_MainWindow,QtWidgets.QFileDialog,QtWidgets.QMessageBox,QtWidgets.QInputDialog):
    
    def __init__(self):
        super(main, self).__init__()
        self.setupUi(self)
        self.MSMT=measurement.measurement()
        self.thread=QThread()
###################################################       
        self.loop1=''
        self.saving_dir=r''
        self.newdirect=r"C:\Users\kaife\Desktop"
        self.newname='new file name.txt'
        self.newtitle='x y1 y2 y3 y4'
        self.file_list=[]
        self.directory=''
        self.f=''
        self.se_setting=[]
###############################################################
        self.fig_dict={} 
        self.header=[]
        self.num=0
        self.fig,self.ax,self.canvas,self.toolbar=self.initialize_fig()
        
############################################################################fig editor   
        self.file_name.textChanged.connect(self.loadData)
        self.bbutton.clicked.connect(self.get_file)
        self.plot_Btn.clicked.connect(self.newPlot)
        self.addPlot.clicked.connect(self.add_plot)
        self.FileIndex.valueChanged.connect(self.scroll_file)
        self.PlotList.itemClicked.connect(self.change_fig)
        self.Xaxis.valueChanged.connect(self.update_label)
        self.Yaxis.valueChanged.connect(self.update_label)
######################################################################seq editor  
        template=path+"\\template.txt"
        self.initialize_seq(template)
        self.DataSave.clicked.connect(self.get_saving_profile)
        self.LoadSeq.clicked.connect(self.Load_Seq)
        self.NewSeq.clicked.connect(self.SeqGetItem)
        self.ClearSeq.clicked.connect(self.clear_que)
        self.AbortSeq.clicked.connect(self.Abort_MS)
        self.StartSeq.clicked.connect(self.Start_MS)
        self.SaveSeq.clicked.connect(self.save_seq)
        self.StartSeq.clicked.connect(self.exceute) 
        self.PauseButton.clicked.connect(self.Pause_MS)
        self.ResumeButton.clicked.connect(self.Resume_MS)
        self.QueList.itemDoubleClicked.connect(self.edit_seq)
#########################################################################initialize fig and measurement
    def initialize_seq(self,template):       
        self.statusBar().setStyleSheet("QStatusBar{padding-left:8px;background-color:black;color:yellow;font: 75 16pt 'Arial';}")
        self.MS_Status=False
        self.QueList.addItem('Secondary_control_disabled!\n Double Click to edit!\n')
        lines=self.MSMT.load_sequence(template)
        [self.QueList.addItem(a) for a in lines]         
            
    def initialize_fig(self):       
        fig = plt.figure()
        ax=fig.add_subplot(111)
        canvas=FigureCanvas(fig)
        canvas.draw()
        toolbar = NavigationToolbar(canvas,self.plot_window, coordinates=True)
        self.mpl.addWidget(toolbar)  
        self.mpl.addWidget(canvas)
        self.add_fig('Plot'+str(self.num),fig)
        self.num += 1
        return fig,ax,canvas,toolbar
    
#######################################################################
        
    def get_file(self):       
        self.f = self.getOpenFileName()[0]
        if os.path.exists(self.f):
            self.file_name.setText(self.f)
            self.list_all_files(self.f)
            self.FileIndex.setValue(self.file_list.index(os.path.split(self.f)[1]))
        return (self.f)
            
    def list_all_files(self,filepath):
        if os.path.exists(filepath):
            self.directory=os.path.dirname(filepath)
            self.file_list=[f1 for f1 in os.listdir(self.directory) 
            if f1.endswith('.txt') or f1.endswith('.dat')]
            self.FileIndex.setMaximum(len(self.file_list)-1)
            
    def scroll_file(self):
        self.f=os.path.abspath(os.path.join(self.directory, self.file_list[int(self.FileIndex.value())]))
        self.file_name.setText(self.f)
    
    def get_current_data(self,filename):        
        try:
            self.file_name.setText(filename)
            self.list_all_files(filename)
            indx=self.file_list.index(os.path.split(filename)[1])
            self.FileIndex.setValue(indx)            
        except Exception as error:
            self.show_message('File:'+str(error))            
############################################################fig control          
    def add_fig(self,name,fig):
        self.fig_dict[name] = fig
        self.PlotList.addItem(name)
        
    def change_fig(self,item):
        text1 = item.text()
        self.rmmpl()
        self.admpl(self.fig_dict[text1])
        self.ax=self.fig_dict[text1].add_subplot(111)
        
    def rmmpl(self):
        self.mpl.removeWidget(self.canvas)
        self.mpl.removeWidget(self.toolbar)
        self.canvas.close()
        
    def admpl(self,fig):
        self.canvas = FigureCanvas(fig)
        self.mpl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,self,coordinates=True)
        self.mpl.addWidget(self.toolbar)
        self.mpl.addWidget(self.canvas)

    def loadData(self):
        skip=self.headerSkip.value()
        try:
            filename=self.f
            data=pd.read_csv(filename,sep=None,header=0,index_col=False,skiprows=skip)
            self.header=list(data.columns)
            self.Xaxis.setMaximum(len(self.header)-1)
            self.Yaxis.setMaximum(len(self.header)-1)
            return data
            self.STBar('Data successfully loaded!') 
        except Exception as error:
                self.STBar(error) 

    def getPlotData(self):
            try:        
                data=self.loadData()
                x=data.values[:,int(self.Xaxis.value())][int(self.SkipRows.value()):data.shape[0]-int(self.SkipFoot.value())]*float(self.Xgain.text())
                y=data.values[:,int(self.Yaxis.value())][int(self.SkipRows.value()):data.shape[0]-int(self.SkipFoot.value())]*float(self.Ygain.text())
                if self.XTime.isChecked():
                    x=[datetime.datetime.fromisoformat('{} {}'.format(data.values[:,0],data.values[:,1])) 
                    for i in range(int(data.shape[0]))]
                    self.Xlabel.setText("Date and time")
                if self.Smooth.isChecked():
                    self.smooth_factor=self.SmoothFac.value()*2+1
                    y=DTP.smooth_data(y,self.smooth_factor)         
                return x,y
            except Exception as error:
                self.STBar(error)     
     
    def update_label(self):
        if len(self.header)>1:
            self.Xlabel.setText(self.header[int(self.Xaxis.value())])
            self.Ylabel.setText(self.header[int(self.Yaxis.value())])

    def setFig_layout(self):    
            self.ax.autoscale()
            self.ax.set_xlabel(self.Xlabel.text())
            self.ax.set_ylabel(self.Ylabel.text())
            self.ax.tick_params('both',which='major',direction='in',length=12,width=1.5)
            self.ax.tick_params('both',which='minor',direction='in',length=6,width=1)
            [self.ax.spines[a].set_linewidth(1.5) for a in ['left','right','bottom','top']]
            le=self.ax.legend(fontsize=15, ncol=1)
            if self.Continuous.isChecked():
                le.remove()
            else:
                le.set_draggable(True)
            self.fig.tight_layout() 

    def add_plot(self,**kwargs):
        
        try:
            if self.LogScale.isChecked():
                self.ax.set_yscale('log')
            else:
                self.ax.set_yscale('linear')
                
            x,y=self.getPlotData()
            self.ax.plot(x,y,color=kwargs.get('color'), linewidth=1.5,label=self.CurveLabel.text())         
            self.setFig_layout()
            self.canvas.draw()
            
        except Exception as error:
            self.STBar(error)

    def continuous_plot(self):
        self.ax.clear()
        self.add_plot(color='k')
            
    def newPlot(self):
        figs=plt.figure();self.ax=figs.add_subplot(111)
        self.add_plot()
        self.rmmpl();self.admpl(figs) 
        self.add_fig('Plot'+str(self.num),figs)        
        self.num += 1      
###########################sequence
    def Load_Seq(self):
        filename=self.getOpenFileName()[0]
        if os.path.exists(filename):
            lines=self.MSMT.load_sequence(filename)
            self.QueList.clear()
            self.QueList.addItem('Secondary_control_disabled!\n Double Click to edit!\n')
            [self.QueList.addItem(a) for a in lines]
        else:
            pass
            
    def clear_que(self):
        self.QueList.clear()
        self.QueList.addItem('Secondary_control_disabled!\n Double Click to edit!\n')         

    def SeqGetItem(self):
        
        que_file = self.getSaveFileName()[0]
        if os.path.exists(que_file):
            newWin=AddQue.QueDialog()
            newWin.getResults(que_file)    
            lines=self.MSMT.load_sequence(que_file)
            [self.QueList.addItem(a) for a in lines]
        
    def edit_seq(self):
        
        SeqName=self.QueList.currentItem().text()
        
        if 'Secondary' in SeqName:
            self.se_control()
        
        elif 'sour' in SeqName:
            w=SourEdit.QueDialog()
            w.show_sour(SeqName)
            text=w.getResults()
            
            if text!=None and len(text.split(' '))==5:
                self.QueList.currentItem().setText(text)
          
        elif 'meas' in SeqName:
            w=MeasEdit.QueDialog()
            w.show_meas(SeqName)
            text_return=w.getResults(SeqName.split(' ')[0]+' ')
            if text_return!=None:
                text,add_after,delete=text_return[:3]
                if text!=None and len(text.split(' '))==3:
                    self.QueList.currentItem().setText(text+'\n')
                if add_after:
                    text=text.replace(text[4],str(int(text[4])+1))
                    self.QueList.addItem(text+'\n')
                if delete:
                    self.QueList.takeItem(self.QueList.currentRow())

    def save_seq(self):
        filename=self.getSaveFileName()[0]
        if os.path.exists(filename):
            seqlist=[self.QueList.item(i).text() for i in range(self.QueList.count())]
            for a in seqlist[1:]:
                with open (filename,'a') as file:
                    file.write(a)
                    
    def run_seq(self,loop1):
        self.Abort_MS()
        self.Continuous.setChecked(True)
        self.statusBar().showMessage('Measurement started!') 
        
        fname=self.saving_dir
        self.file_name.setText(fname)
        seqlist=[self.QueList.item(i).text() for i in range(self.QueList.count())]
        self.MSMT=measurement.measurement(seqlist,loop1,fname,self.newtitle)
        self.MSMT.SingleMS.connect(self.statusBar().showMessage)
        self.MSMT.FN_out.connect(self.get_current_data)
        self.MSMT.error_message.connect(self.show_message)
        self.MSMT.moveToThread(self.thread)
        self.MSMT.finished.connect(self.thread.quit)
        self.thread.started.connect(self.MSMT.loop_control)
        self.thread.start() 
          
    def se_control(self):
        w=SE_control.SE_Dialog()
        if len(self.se_setting)==3:
            w.show_Exc(self.se_setting)
        value=w.getResults()
        if value!=None:
            if value[0]:
                self.QueList.item(0).setText('Secondary_control_enabled!\n Double Click to edit!\n')
                self.loop1=value[1:]
            else:
                self.QueList.item(0).setText('Secondary_control_disabled!\n Double Click to edit!\n')
            self.se_setting=value

    def exceute(self):
        if self.QueList.item(0).text()=='Secondary_control_disabled!\n Double Click to edit!\n':
            self.statusBar().showMessage('Just a single measurement!')   
            loop1=''
            self.run_seq(loop1)
        elif self.QueList.item(0).text()=='Secondary_control_enabled!\n Double Click to edit!\n':
            loop1=self.loop1
            self.statusBar().showMessage('Loop measurement starts!') 
            self.run_seq(loop1)
            self.MSMT.LoopNum.connect(self.showLoop)
            self.MSMT.LoopStatus.connect(self.statusBar().showMessage)

    def showLoop(self,loop):
        self.statusBar().showMessage('Executing Loop item '+str(loop)+' !')            

###############################################################################
    def get_saving_profile(self):
        w1=FileUI.FileSaving(self.newdirect,self.newname,self.newtitle)
        self.filedata=w1.FgetResults()
        try:
            self.newdirect=self.filedata[0]
            self.saving_dir=self.filedata[1]
            self.newname=self.filedata[2]
            self.newtitle=self.filedata[3]
        except:
            self.show_message('File not correct, please input the directory or filename again!')

    def Start_MS(self):
        self.MS_Status=True
        self.STBar('Measurement started!')
        
    def Abort_MS(self):
        self.MSMT.resume_seq()
        self.MSMT.stop()
        self.MS_Status=False
        self.STBar('Measurement aborted!')

    def Pause_MS(self):
        self.MS_Status=False
        self.MSMT.pause_seq()
        self.STBar('Measurement paused!')
        
    def Resume_MS(self):
        self.MSMT.resume_seq()
        self.STBar('Measurement resumed!')

################################################################################
    def show_message(self,message):
        self.information(None,'Error!',message)
    
    def STBar(self,message):
        self.statusBar().setStyleSheet("QStatusBar{padding-left:8px;background-color:black;color:red;font: 75 16pt 'Arial';}")
        self.statusBar().clearMessage()
        self.statusBar().showMessage(str(message))
        
    def refresh_input(self):
        if self.Continuous.isChecked():
            self.continuous_plot()
#################################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = main()    
    window.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(window.refresh_input)
    timer.start(50)    
    sys.exit(app.exec_())
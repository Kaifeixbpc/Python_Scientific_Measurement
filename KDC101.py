# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 02:42:31 2020

@author: Kaifei Kang
"""

import sys
import clr
import ctypes
import numpy as np
import System


sys.path.append("C:\Program Files\Thorlabs\Kinesis")

clr.AddReference("Thorlabs.MotionControl.KCube.DCServoCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.DCServoUI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *
from Thorlabs.MotionControl.KCube.DCServoUI import *


def list_devices():
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()
d_list=list_devices()


class Motor():
    
    def __init__(self,ser):

        self.ser=str(ser)
        self.motor=KCubeDCServo.CreateKCubeDCServo(self.ser)
        self.polling_time=250
        self.connect()
 
    def connect(self):
        
        self.motor.Connect(self.ser)
        self.motor.StartPolling(self.polling_time)
        self.motor.WaitForSettingsInitialized(50000);
        self.motor.GetMotorConfiguration(self.ser,DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        self.motor.EnableDevice()
        self.set_jog_params()
        
    def jog_up(self):
        
        stepsize=float(str(self.motor.GetJogStepSize()))
        timewait=int(stepsize*10000)
        if timewait<self.polling_time:
            timewait=self.polling_time
        self.motor.MoveJog(1,timewait)
        return self.pos()
    
    def jog_down(self):
        
        stepsize=float(str(self.motor.GetJogStepSize()))
        timewait=int(stepsize*10000)
        if timewait<self.polling_time:
            timewait=self.polling_time
            
        self.motor.MoveJog(2,timewait)
        return self.pos()       
    
    def move_to(self,target):
        
        current_pos=self.pos()
        moving_range=np.abs(target-current_pos)
        timewait=int(moving_range*10000)
        
        if timewait<self.polling_time:
            timewait=self.polling_time
        self.motor.MoveTo(System.Decimal(target),timewait)
        
        return self.pos()

    def set_jog_params(self,vel=0.01,accl=0.01,stp_mode=1):
        
        vel=System.Decimal(vel)
        accl=System.Decimal(accl)
        new_pa=self.motor.GetJogParams()
        new_pa.StopMode=1
        self.motor.SetJogParams(new_pa)
        self.motor.SetJogVelocityParams(vel,accl)

    
    
    def set_jog_step(self,step):
        self.motor.SetJogStepSize(System.Decimal(step))
        

    def set_backlash(self,lash):
        self.motor.SetBacklash(System.Decimal(lash))

    def pos(self):
        return float(str(self.motor.Position))
        
    def motor_state(self):
        state=self.motor.State
        return state

    def get_jog_params(self):
        
        vel=self.motor.GetJogVelocityParams()[0]
        accl=self.motor.GetJogVelocityParams()[1]
        stop_mode=self.motor.GetJogParams().StopMode
        return(vel,accl,stop_mode)
    
    def get_vel_params(self):
        return self.motor.GetVelocityParams()

    def disconnect(self):
        self.motor.ShutDown()

if len(d_list)>0:
    m=Motor(d_list[0])

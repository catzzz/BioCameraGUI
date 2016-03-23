#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the grid
manager to create a more complicated
layout.

Author: Jan Bodnar
Last modified: December 2015
Website: www.zetcode.com
"""
import math
import threading
from Tkinter import *
from ttk import Frame, Button, Label, Style
import os.path
import cv2
import numpy as np
import xlwt
import xlrd
import RPi.GPIO as GPIO
import time
from picamera.array import PiRGBArray
import picamera
import picamera.array

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()


    def initUI(self):

        self.parent.title("Windows")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        #check button variable
        self.testMode_check_button = IntVar()
        self.collectionMode_check_button = IntVar()
        self.isOldCoordinateFile= IntVar()

        #entry string variable
        self.entry_1_string = StringVar()
        self.entry_2_string = StringVar()
        self.entry_3_string = StringVar()
        self.entry_4_string = StringVar()
        self.entry_5_string = StringVar()
        self.entry_6_string = StringVar()
        self.entry_7_string = StringVar()


        self.entry_1_string.set("database12.xls")
        self.entry_2_string.set("coeffnmean12.xls")
        self.entry_3_string.set(".xls")
        self.entry_4_string.set(".xls")

        self.saveFileName= StringVar()
        self.saveCoordinateFileName = StringVar()

        # database array
        self.radiusArray =[]
        self.xavgArray=[]
        self.yavgArray=[]
        self.coeffIndexArray=[]

        # coefficient array
        self.coeffArray=[]
        self.meanRGBArray=[]
        self.VarCoeffArray=[]
        self.adjustmentRGBArray=np.zeros(shape=(1,3))
        self.referenceRGBArray=np.zeros(shape=(1,3))



        # num Of Area
        self.numberOfArea=IntVar()

        # num of Sec
        self.numberOfSec= IntVar()

        # flag of the camera action

        self.stopCameraPreview=BooleanVar()
        self.stopCameraClipAndCrop= BooleanVar()
        self.stopCameraExperiment = BooleanVar()

        #init the flag
        self.stopCameraPreview.set(FALSE)
        self.stopCameraClipAndCrop.set(FALSE)
        self.stopCameraExperiment.set(FALSE)

        # image variable

        self.cropImage =[]
        #clip and clop
        self.refPt=[]
        self.cropping=[]
        self.cropNumber=IntVar()
        self.selectAreaArray=[]




        #Step 1
        lbl1 = Label(self, text="Step 1: Input file name ")
        lbl1.grid(sticky=W, pady=4, padx=5)

        #check button
        self.checkbutton0  = Checkbutton(self,text="Test mode (no database, coefficient, coordinate, save file)"
                                         ,variable=self.testMode_check_button,command=self.testMode)
        self.checkbutton0.grid(row=1,columnspan = 3, sticky=W,pady=3,padx=5)

        self.checkbutton1  = Checkbutton(self,text="Collection data mode (no database, coefficient)"
                                         ,variable=self.collectionMode_check_button,command=self.collecitonMode)
        self.checkbutton1.grid(row=2,columnspan = 3,sticky=W,pady=3,padx=5)

        #input database xls file name
        self.label_1 = Label(self, text = "Type the database file name(xls)")
        self.label_1.grid(row=3,column=0, sticky= W,padx=5,pady=3)
        self.entry_1 = Entry(self,textvariable=self.entry_1_string)
        self.entry_1.grid(row=3,column = 1)
        #input coefficient

        self.label_2 = Label(self, text = "Type the coefficient file name(xls)")
        self.label_2.grid(row=4,column=0, sticky= W,padx=5,pady=3)
        self.entry_2 = Entry(self,textvariable=self.entry_2_string)
        self.entry_2.grid(row=4,column = 1)

        #input the coordinate file

        self.label_3 = Label(self, text = "Type new or load coordinate file(xls)")
        self.label_3.grid(row=5,column=0, sticky= W,padx=5,pady=3)
        self.entry_3 = Entry(self,textvariable=self.entry_3_string)

        self.entry_3.grid(row=5,column = 1)
        self.checkbutton3  = Checkbutton(self,text="load old file? "
                                         ,variable=self.isOldCoordinateFile,command=self.isOldCoordinateFileMethod)
        self.checkbutton3.grid(row=5,column=2,columnspan = 3,sticky=W,padx=5,pady=3)
        #input the result file

        self.label_4 = Label(self, text = "Type the save file name(xls)")
        self.label_4.grid(row=6,column=0, sticky= W,padx=5,pady=3)
        self.entry_4 = Entry(self,textvariable=self.entry_4_string)
        self.entry_4.grid(row=6,column = 1)
        self.step1_next_btn = Button(self, text="Go to Step 2",command= self.pressStep1NextBtn)
        self.step1_next_btn.grid(row=7, column =2, padx=5,pady=3)

        #Step 2
        lbl1 = Label(self, text="Step 2: Input Variable")
        lbl1.grid(sticky=W, pady=4, padx=5)

        self.label_5 = Label(self, text = "How many sencod")
        self.label_5.grid(row=9,column=0, sticky= W,padx=5,pady=3)
        self.entry_5 = Entry(self,textvariable=self.entry_5_string,state='disabled')
        self.entry_5.grid(row=9,column = 1)

        self.label_6 = Label(self, text = "How many areas")
        self.label_6.grid(row=10,column=0, sticky= W,padx=5,pady=3)
        self.entry_6 = Entry(self,textvariable=self.entry_6_string,state='disabled')
        self.entry_6.grid(row=10,column = 1)

        self.label_7 = Label(self, text = "How many variable from database")
        self.label_7.grid(row=11,column=0, sticky= W,padx=5,pady=3)
        self.entry_7 = Entry(self,textvariable=self.entry_7_string,state='disabled')
        self.entry_7.grid(row=11,column = 1)

        self.step2_next_btn = Button(self, text="Go to Step 3",command= self.pressStep2NextBtn,state='disabled')
        self.step2_next_btn.grid(row=14, column =2, padx=5,pady=3)

        #step 3
        lbl2 = Label(self, text="Step 3: Experiment")
        lbl2.grid(sticky=W, pady=4, padx=5)
        # preview button

        self.start_preview_button = Button(self, text="Start Preview Video", command=self.startPreview,state='disabled')
        self.start_preview_button.grid(row=16,column=0,sticky=W)
        self.stop_preview_button = Button(self, text="Stop Preview Video", command=self.stopPreview,state='disabled')
        self.stop_preview_button.grid(row=16,column=1,sticky=W)
        #click and crop image button
        self.start_click_and_crop_button = Button(self, text="Start Crop Image", command=self.startClipAndCrop,state='disabled')
        self.start_click_and_crop_button.grid(row=17,column=0,sticky=W)
        self.stop_click_and_crop_button = Button(self, text="Close Crop Image", command=self.stopClipAndCrop,state='disabled')
        self.stop_click_and_crop_button.grid(row=17,column=1,sticky=W)

        # strart experiment
        self.start_experiment_button = Button(self, text="Start Experiment", command=self.startExperimentButtonPress,state='disabled')
        self.start_experiment_button.grid(row=18,column=0,sticky=W)
        self.stop_experiment_button = Button(self, text="Stop Experiment", command=self.stopExperimentButtonPress,state='disabled')
        self.stop_experiment_button.grid(row=18,column=1,sticky=W)



    def pressStep2NextBtn(self):
        if(len(self.entry_5_string.get())>0 and len(self.entry_6_string.get())>0):

            if self.isOldCoordinateFile.get():
                if not self.checkFileExit(self.saveCoordinateFileName.get()):
                    print 'old coordinate file is not exit, please input correct file name'
                    return
               # else:


            # area is define by the entry
            else:
                self.numberOfArea.set(str(self.entry_6_string.get()))

            # add 1 area for the color calibration

            self.enableStep3Area()
            if len(self.selectAreaArray)==0:

                self.selectAreaArray= np.zeros(shape=(self.numberOfArea.get()*2,2))
            self.numberOfSec.set(str(self.entry_5_string.get()))
            self.saveFileName.set(self.entry_4_string.get())
            self.saveCoordinateFileName.set(self.entry_3_string.get())

            print "go to step 3 "
            print 'number of area '+str(self.numberOfArea.get())
            print 'number of sec '+str(self.numberOfSec.get())
            print 'save file name: '+self.saveFileName.get()
            print 'save coordinate name '+self.saveCoordinateFileName.get()
            # if old file is select, check file exit


        else:
            print "please enter correct number"

    def pressStep1NextBtn(self):
        # test mode
        if(self.testMode_check_button.get()):
            print "test  mode"
            self.enableStep2Area()
        # collection mode
        elif (self.collectionMode_check_button.get()):
            print "collection mode"
            if (len(self.entry_3_string.get()) <4
                or len(self.entry_4_string.get()) <4):
                print "Please input correct file name"
            else:
                self.enableStep2Area()

        # normal mode
        else:
            if (len(self.entry_1_string.get()) <4
                or len(self.entry_2_string.get()) <4
                or len(self.entry_3_string.get()) <4
                or len(self.entry_4_string.get()) <4):
                print "Please input correct file name"
            else:
                print "normal next step"
                if (self.checkFileExit(self.entry_1_string.get()) and (self.checkFileExit(self.entry_2_string.get()))):
                    self.enableStep2Area()
                    self.openCoefficientFileAndDataBase(self.entry_1_string.get(),self.entry_2_string.get())


    def openOldCoordinateFile(self,coordFileName):
        data1 = xlrd.open_workbook(coordFileName)
        table= data1.sheets()[0]
        DareaNum=table.nrows
        areaNum=int(DareaNum/2)
        # set up area number base on the
        selectAreaArray=np.zeros(shape=(DareaNum,2))
        for si in range(DareaNum):
            selectAreaArray[si][0],selectAreaArray[si][1]=table.row_values(si)
        return selectAreaArray

    def enableStep3Area(self):
        self.start_preview_button.configure(state='normal')
        self.stop_preview_button.configure(state='normal')
        self.start_experiment_button.configure(state='normal')
        self.stop_experiment_button.configure(state='normal')
        #if not old file
        if not self.isOldCoordinateFile.get():
            self.start_click_and_crop_button.configure(state='normal')
            self.stop_click_and_crop_button.configure(state='normal')

    def enableStep2Area(self):
        self.step2_next_btn.configure(state='normal')
        self.entry_5.configure(state='normal')
        self.entry_6.configure(state='normal')
        if (not self.testMode_check_button.get()):
            self.entry_7.configure(state='normal')

    def isOldCoordinateFileMethod(self):
        print "old file"
        self.saveCoordinateFileName.set(self.entry_3_string.get())
        #check if the old file is exit
        if self.isOldCoordinateFile.get():
            if not self.checkFileExit(self.entry_3_string.get()):
                print 'file is not exit,please check again'
            else:
                self.selectAreaArray=self.openOldCoordinateFile(self.saveCoordinateFileName.get())
                #print self.selectAreaArray
                numrow = len(self.selectAreaArray)/2 # 2 columns in your example
                #not in test and collection mode
                #check again database has same area as old coordinate file
                if (not self.testMode_check_button.get()) and (not self.collectionMode_check_button.get()):
                    if not numrow == self.numberOfArea.get():
                        print 'error------coordinate file has different number of area from cooefficient file--------'
                else:
                    self.numberOfArea.set(numrow)
                    self.entry_6_string.set(numrow)

                self.entry_3.configure(state='disabled')
        else:
            self.entry_3.configure(state='normal')

    def checkFileExit(self,fileName):
        if os.path.exists(fileName):
            return TRUE
        else:
            print fileName+' not exit'
            return FALSE

    def testMode(self):
        if(self.testMode_check_button.get()):
            self.checkbutton1.configure(state='disabled')
            self.entry_1_string.set("disable")
            self.entry_2_string.set("disable")
            self.entry_3_string.set("disable")
            self.entry_4_string.set("disable")
            self.entry_1.configure(state='disabled')
            self.entry_2.configure(state='disabled')
            self.entry_3.configure(state='disabled')
            self.entry_4.configure(state='disabled')
            self.entry_7.configure(state='disabled')

        else:
            self.checkbutton1.configure(state='normal')
            self.entry_1_string.set("database12.xls")
            self.entry_2_string.set("coeffnmean12.xls")
            self.entry_3_string.set(".xls")
            self.entry_4_string.set(".xls")
            self.entry_1.configure(state='normal')
            self.entry_2.configure(state='normal')
            self.entry_3.configure(state='normal')
            self.entry_4.configure(state='normal')
            self.entry_7.configure(state='normal')




    def collecitonMode(self):
        if(self.collectionMode_check_button.get()):
            self.checkbutton0.configure(state='disabled')
            self.entry_1_string.set("disable")
            self.entry_2_string.set("disable")
            self.entry_1.configure(state='disabled')
            self.entry_2.configure(state='disabled')
            self.entry_7.configure(state='disabled')
        else:
            self.checkbutton0.configure(state='normal')
            self.entry_1_string.set("database12.xls")
            self.entry_2_string.set("coeffnmean12.xls")
            self.entry_1.configure(state='normal')
            self.entry_2.configure(state='normal')
            self.entry_7.configure(state='normal')



    def previewCamera(self):
        print 'start preview'
        print self.selectAreaArray
        for area in range(self.numberOfArea.get()):
            startPoint = (int(self.selectAreaArray[area*2][0]),int(self.selectAreaArray[area*2][1]))
            endPoint = (int(self.selectAreaArray[area*2+1][0]),int(self.selectAreaArray[area*2+1][1]))
            print startPoint
            print endPoint
        with picamera.PiCamera() as camera:
                #camera = picamera.PiCamera()
                camera.resolution= (640,480)
                camera.frameate=32
                camera.shutter_speed=camera.exposure_speed
                camera.exposure_mode='off'
                camera.awb_mode='off'
                camera.awb_gains=(1.6, 1.4) # white balance parameter
                camera.brightness=60        # brightness
                camera.contrast=20
                camera.saturation=20
                camera.sharpness=1
                rawCapture = PiRGBArray(camera,size=(640,480))
                time.sleep(0.1)
                cv2.namedWindow("realtimeImage")
                cv2.startWindowThread()
                for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
                        image01=frame.array
                        # if load old coordinage file , draw the rectangle area
                        if self.isOldCoordinateFile.get():
                            for area in range(self.numberOfArea.get()):
                                color = (0,255,0)
                                if area ==0:
                                    color = (0,255,255)
                                else:
                                    color = (0,255,0)
                                startPoint = (int(self.selectAreaArray[area*2][0]),int(self.selectAreaArray[area*2][1]))
                                endPoint = (int(self.selectAreaArray[area*2+1][0]),int(self.selectAreaArray[area*2+1][1]))
                                cv2.rectangle(image01,startPoint,endPoint,color,2)
                        #show image
                        cv2.imshow("realtimeImage",image01)
                        key=cv2.waitKey(10) &0xFF
                        rawCapture.truncate(0)
                        if key==ord("q") or self.stopCameraPreview.get():
                                cv2.destroyAllWindows() # close window
                                self.stopCameraExperiment.set(FALSE)
                                self.stopCameraClipAndCrop.set(FALSE)
                                self.stopCameraPreview.set(FALSE)
                                break
    def cropCameraImage(self):
        print 'start preview in crop image for 3 sec'
        startTime = time.time()
        with picamera.PiCamera() as camera:
                #camera = picamera.PiCamera()
                camera.resolution= (640,480)
                camera.frameate=32
                camera.shutter_speed=camera.exposure_speed
                camera.exposure_mode='off'
                camera.awb_mode='off'
                camera.awb_gains=(1.6, 1.4)
                camera.brightness=60
                camera.contrast=20
                camera.saturation=20
                camera.sharpness=1
                rawCapture = PiRGBArray(camera,size=(640,480))
                time.sleep(0.1)
                cv2.namedWindow("realtimeImage")
                cv2.startWindowThread()
                for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
                        self.cropImage=frame.array
                        #show image
                        cv2.imshow("realtimeImage",self.cropImage)
                        key=cv2.waitKey(1 ) &0xFF
                        rawCapture.truncate(0)
                        if time.time()-startTime>3 or self.stopCameraClipAndCrop.get():
                            cv2.destroyAllWindows() # close window
                            self.stopCameraExperiment.set(FALSE)
                            self.stopCameraClipAndCrop.set(FALSE)
                            self.stopCameraPreview.set(FALSE)
                            break
                # end of realtime preview
                cv2.namedWindow("currentImage")
                cv2.startWindowThread()
                cv2.setMouseCallback("currentImage",self.click_and_crop)
                cv2.imshow("currentImage",self.cropImage)



    def click_and_crop(self,event,x,y,flags,param):
        #grab references to the global variables
        #global refPt, cropping,cropNumber,selectAreaArray

        #if the left mouse button was clicked record the starting
        #(x,y) coordinates and indicate that cropping in being
        #performed
        if self.cropNumber.get() == self.numberOfArea.get():
            print "reach area number"
            return

        if event ==cv2.EVENT_LBUTTONDOWN:
                self.refPt=[(x,y)]

                self.selectAreaArray[self.cropNumber.get()*2]=(x,y)
                #testNumber=0
        #check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
                #record the ending (x,y) coordinates and inidate that
                #that cropping operation is finished
                self.refPt.append((x,y))
                self.selectAreaArray[self.cropNumber.get()*2+1]=(x,y)
                #draw a rectangle around the region of interest
                print self.refPt[0]
                print self.refPt[1]
                color = (0,255,0)
                if self.cropNumber.get() ==0:
                    color = (0,255,255)
                else:
                    color = (0,255,0)
                cv2.rectangle(self.cropImage,self.refPt[0],self.refPt[1],color,2)
                self.cropNumber.set(self.cropNumber.get()+1) # add one area num
                print self.cropNumber
                print self.selectAreaArray
                #cv2.destroyAllWindows()
                #cv2.namedWindow("currentImage")
                #cv2.startWindowThread()
                cv2.imshow("currentImage",self.cropImage)
                # end of area and not in test mode . save the coordinate file
                if (self.cropNumber.get() == self.numberOfArea.get()) and (not self.testMode_check_button.get()) :
                    ourthread  = threading.Thread(target=self.saveCoordinateXLS2(self.saveCoordinateFileName.get(),self.selectAreaArray))
                    ourthread.start()




    def saveCoordinateXLS2(self,coorFileName,temparray):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Coordinates')
        for row, array in enumerate(temparray):
                for col, value in enumerate(array):
                        worksheet.write(row,col,value)
        workbook.save(coorFileName)
        print "end wirte coordinate file"

    #start experiment
    def starExperiment(self):
        print 'start experiment'

        with picamera.PiCamera() as camera:
                sensor_roi = dict()  # create a dict for storing sensor data
                tempSaveFileArray=[]
                #camera = picamera.PiCamera()
                camera.resolution= (640,480)
                camera.frameate=10
                camera.shutter_speed=camera.exposure_speed
                camera.exposure_mode='off'
                camera.awb_mode='off'
                camera.awb_gains=(1.6, 1.4)
                camera.brightness=60
                camera.contrast=20
                camera.saturation=20
                camera.sharpness=1
                rawCapture = PiRGBArray(camera,size=(640,480))
                time.sleep(0.1)
                cv2.namedWindow("experimentImage")
                cv2.startWindowThread()
                tstart=time.time()
                currentFrame=0
                for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
                        image=frame.array

                        # calculate the frame
                        frametime = time.time()-tstart

                        print('frame: '+str(currentFrame)+' time: '+str(frametime))


                        # get mean RGB from frame 1
                        if currentFrame==0:
                            senor_roi_01=dict()  # create a dict for storing sensor data
                            senor_roi_01[0] = image[int(self.selectAreaArray[(0)*2][1]):int(self.selectAreaArray[(0)*2+1][1])
                                        ,int(self.selectAreaArray[(0)*2][0]):int(self.selectAreaArray[(0)*2+1][0])]
                                # get mean of each area
                            b,g,r,w=cv2.mean(senor_roi_01[0])
                            #clear senor_roi_01 dict
                            senor_roi_01.clear()
                            self.referenceRGBArray[0][0]=r
                            self.referenceRGBArray[0][1]=g
                            self.referenceRGBArray[0][2]=b
                        # create a temp array to save the mean of each area
                        SampleRGB=np.zeros(shape=(1,3*self.numberOfArea.get()))
                         #grab each area
                        for area in range(self.numberOfArea.get()):
                                sensor_roi[0] = image[int(self.selectAreaArray[(area)*2][1]):int(self.selectAreaArray[(area)*2+1][1])
                                                                ,int(self.selectAreaArray[(area)*2][0]):int(self.selectAreaArray[(area)*2+1][0])]
                                # get  Mean RGB
                                b,g,r,w=cv2.mean(sensor_roi[0])
                                #clear sensor_roi dict
                                sensor_roi.clear()
                                if area==0: # get adjust mean rgb at area 0
                                    tempMeam=np.zeros(shape=(1,3))
                                    tempMeam[0][0]=r
                                    tempMeam[0][1]=g
                                    tempMeam[0][2]=b
                                    self.adjustmentRGBArray = np.zeros(shape=(1,3))
                                    self.adjustmentRGBArray = tempMeam-self.referenceRGBArray
                                    print 'adjust RGB'
                                    print self.adjustmentRGBArray
                                else: # get sampeRGB for the rest of area
                                    SampleRGB[0][area*3]=r+self.adjustmentRGBArray[0][0]
                                    SampleRGB[0][area*3+1]=g +self.adjustmentRGBArray[0][1]
                                    SampleRGB[0][area*3+2]=b +self.adjustmentRGBArray[0][2]
                                    tempObjectRGB = [currentFrame,area,r,g,b]
                                    tempSaveFileArray.append(tempObjectRGB)
                                    # end of the area
                                    # if not in test mode and not in collection mode
                                    if (not self.testMode_check_button.get()) and ( not self.collectionMode_check_button.get()):
                                        if area == self.numberOfArea.get()-1:
                                            self.processPCACompareAlgorithm(SampleRGB,self.meanRGBArray,self.VarCoeffArray)
                        # draw the line
                        for area in range(self.numberOfArea.get()):
                            color = (0,255,0)
                            if area ==0:
                                color= (0,255,255)
                            else:
                                color = (0,255,0)
                            startPoint = (int(self.selectAreaArray[area*2][0]),int(self.selectAreaArray[area*2][1]))
                            endPoint = (int(self.selectAreaArray[area*2+1][0]),int(self.selectAreaArray[area*2+1][1]))
                            cv2.rectangle(image,startPoint,endPoint,color,1)
                        #show image
                        cv2.imshow("experimentImage",image)
                        key=cv2.waitKey(1 ) &0xFF
                        rawCapture.truncate(0)
                        currentFrame=currentFrame+1

                        #chcek if the time period if end or press c save file
                        if time.time()-tstart >  self.numberOfSec.get() :
                                #close the light
                                GPIO.output(11,False)
                                GPIO.output(15,False)
                                cv2.destroyAllWindows() # close window
                                # not in test mode save file
                                if(not self.testMode_check_button.get()):
                                    ourthread = threading.Thread(target=self.saveRGBdataIntoXLS(self.saveFileName.get(),tempSaveFileArray))
                                    ourthread.start()
                                break
                        #quit funcion
                        if key==ord("q") or self.stopCameraExperiment.get():
                                GPIO.output(11,False)
                                GPIO.output(15,False)
                                cv2.destroyAllWindows() # close window
                                self.stopCameraExperiment.set(FALSE)
                                self.stopCameraClipAndCrop.set(FALSE)
                                self.stopCameraPreview.set(FALSE)
                                break
                                                #draw the rectangle



    def is_in_circle(x,y,raduis,center_x,center_y):
        d =math.sqrt(math.pow(center_x-x,2)+math.pow(center_y-y,2))
        print d
        return d<=raduis

    def processPCACompareAlgorithm(self,sampleRGBArray, meanRGBArray, varCoeffArray):
        testPCA = sampleRGBArray-meanRGBArray[1]
        Var1=sum(sum(testPCA*varCoeffArray[0]))
        Var2=sum(sum(testPCA*varCoeffArray[1]))
        # chek if the var1 is inside a circle
        if self.is_in_circle(Var1,Var2,self.radiusArray[0],self.xavg[0],self.yavg[0]):
            print 'Detected: x:'+str(Var1)+' y: '+str(Var2)
        else:
            print 'Not Detectedx:'+str(Var1)+' y: '+str(Var2)


    ''' old // 1 d not use anymore
    def processPCACompareAlgorithm(self,sampleRGBArray, meanRGBArray, varCoeffArray):

        testPCA = sampleRGBArray-meanRGBArray[1]
        Var1=sum(sum(testPCA*varCoeffArray[0]))
        Var1IntBigger= float(self.entry_8_string.get())
        print Var1IntBigger
        Var1IntLess= float(self.entry_9_string.get())
        print Var1IntLess
        if Var1>Var1IntBigger:
                #Result=0
                print 'NORMAL'
        elif Var1<Var1IntLess:
                #Result=1
                print 'DETECT!!'
        else :
                print 'NOT FOUND'
    '''
    def saveRGBdataIntoXLS(self,filename, temparray):
        data = xlwt.Workbook()
        dataws = data.add_sheet('Data')
        for row, array in enumerate(temparray):
                for col, value in enumerate(array):
                        dataws.write(row,col,value)
        data.save(filename)
        print "end wirte rgb save file, end program after 2 sec"
        time.sleep(2)
        sys.exit(0)

    def startPreview(self):
        # put camera into thread
        t1 = threading.Thread(target=self.previewCamera)
        t1.start()


    def stopPreview(self):
        self.stopCameraExperiment.set(TRUE)
        self.stopCameraClipAndCrop.set(TRUE)
        self.stopCameraPreview.set(TRUE)
        print 'stop preview'

    def startClipAndCrop(self):
        t2= threading.Thread(target=self.cropCameraImage)
        t2.start()

    def stopClipAndCrop(self):
        #self.stopCameraExperiment.set(TRUE)
        self.stopCameraClipAndCrop.set(TRUE)
        #self.stopCameraPreview.set(TRUE)
        cv2.destroyAllWindows()
        print 'close crop image'

    def startExperimentButtonPress(self):
        t3=threading.Thread(target=self.starExperiment)
        t3.start()

    def stopExperimentButtonPress(self):
        self.stopCameraExperiment.set(TRUE)
        self.stopCameraClipAndCrop.set(TRUE)
        self.stopCameraPreview.set(TRUE)
        print 'close experiment image'

    #opne coefficient file and database file to get data
    def openCoefficientFileAndDataBase(self,databaseFile,coefficientFile):
        #open database
        ref2=xlrd.open_workbook(databaseFile)
        table2=ref2.sheets()[0]
        database=np.zeros(shape=(table2.nrows,table2.ncols))
        dRows=table2.nrows
        dCols=table2.ncols
        for i in range(0,dRows):
            for j in range(0,dCols):
                #print float(table2.cell(i,j).value)
                database[i][j]=float(table2.cell(i,j).value)
        # average of x
        self.xavg=database[1]
        print str(self.xavg)
        # average of y
        self.yavg=database[2]
        # radius of thie coefficience
        self.radiusArray=database[3]
        # index in coefficience array
        self.coeffIndexArray=database[4]


        #open coefficient mean
        ref1=xlrd.open_workbook(coefficientFile)
        table1=ref1.sheets()[0]
        self.coeffArray=np.zeros(shape=(table1.nrows-2,table1.ncols))
        self.meanRGBArray=np.zeros(shape=(2,table1.ncols))

        self.VarCoeffArray = np.zeros(shape=(len(self.coeffIndexArray),table1.ncols))


        cRows=table1.nrows
        cCols=table1.ncols
        # get coefficient data from file
        for i in range(0,cRows-2):
            for j in range(0,cCols):
                self.coeffArray[i][j]=table1.cell(i,j).value

        #get varcoeffarray

        for i in range(0,len(self.coeffIndexArray)):
            #print self.VarCoeffArray[i]
            #print self.coeffIndexArray[i]
            #print[row[self.coeffIndexArray[i]-1] for row in self.coeffArray]
            self.VarCoeffArray[i]=[row[self.coeffIndexArray[i]-1] for row in self.coeffArray]
        #print 'self.VarCoeffArray'
        #print self.VarCoeffArray[0]
        for i in range(cRows-2,cRows):
            for j in range(0,cCols):
                self.meanRGBArray[i-cRows+2][j]=table1.cell(i,j).value

        # get number of Area base on the coefficinet file

        self.numberOfArea.set(int(table1.ncols/3))
        self.entry_6_string.set(str(self.numberOfArea.get()))
        #self.entry_6.configure(state='disabled')

        # get number of variable from database file
        self.entry_7_string.set(str(len(self.coeffIndexArray)))

        #print 'VarCoeffArry: '+str(self.VarCoeffArray)
        #print 'VarCoeffArry[0]: '+str(self.VarCoeffArray[0])
        #print 'VarCoeffArry[1]: '+str(self.VarCoeffArray[1])

def main():

    GPIO.setmode(GPIO.BOARD)
    # reset GPIO
    GPIO.cleanup()
    GPIO.setwarnings(FALSE)
    # set GPIO output
    GPIO.setup(11,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
    # open LED
    GPIO.output(11,True)
    GPIO.output(15,True)
    time.sleep(2)
    root = Tk()

    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()

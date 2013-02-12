#!/usr/bin/python

# import system modules
import cv2.cv as cv
import urllib
import numpy as np
from numpy import linalg as LA

import socket
import time
import os

global imghsv

# purpose: using HSV thresholds, detects blue, yellow and purple objects in a video stream in three new windows
# 	   1) a black/white stream showing objects matching threshold values (window "threshold")
#	   2) a black/color stream tracking the locations of the objects in their respective colors (window "final")
#	   3) a full-color stream showing the original video and the bounding boxes of detected objects (window "real")

# things that would make this script more useful for future tests: 
# 	   1) GUI HSV threshold and minimum pixel size sliders like Kevin has added to the Canny Edge Detection program
#	   2) Limit the number of blue/yellow/purple objects that can be detected at one time to one

# source from:
# http://stackoverflow.com/questions/8152504/tracking-two-different-colors-using-opencv-2-3-and-python

# definitely works with Mac OSX, Python 2.7, and OpenCV library

# to modify color thresholds, change the cv.Scalar values in the InRange method in the gettresholdedimg function below

def connect(ip,port):
        #make a client socket
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        #keep trying to connect to the server until success
        print("connecting to control server...")
        print("")
        connected = False
        #while not connected:
        try:
                s.connect((ip, port))
                connected = True
        except Exception as err:
                pass
        #print("connected")
        return s

#---------------------------------------------------------
#The following function takes coordinates from the images and convertes them to 3D spatial positions
#The calibration constants are in R1, T1, R2, and T2 for cameras 1 (west) and 2 (east)
#These constants are produced by matlab code that is available here:
#http://www.vision.caltech.edu/bouguetj/calib_doc/
def triang_3D(col_1, row_1, col_2, row_2) :
        
        #Corrected camera matrix for west side
        P1 = np.array([[408.4918, -1607.7562, 3814.1879, 490234.8756], [-1793.2995, -707.4668, -45.8775, 646489.5760], [0.1810, -0.9505, -0.2524, 1285.5524]])

        #Corrected camera matrix for east side
        P2 = np.array([[-49.3179, -518.1547, -4126.6037, 847220.0489], [-1776.8193, 738.4249, -127.1965, 963513.3797], [0.2075, 0.9387, -0.2753, 1589.9759]])

        #blimp position from camera 1
        #col_1 = 396
        #row_1 = 424
        #m1 = np.array([
        #blimp position from camera 2
        #col_2 = 518
        #row_2 = 538


        #translated from matlab:

        #Camera 1
        invR1 = LA.inv(P1[0:3,0:3])
        m1T1 = -1*P1[:,3]
        C1 = np.dot(invR1, m1T1)
        x0 = C1[0]
        y0 = C1[1]
        z0 = C1[2]
        m1 = np.array([[col_1], [row_1], [1]]);
        M1 = np.dot(LA.pinv(P1), m1)
        x = M1[0]/M1[3]
        y = M1[1]/M1[3]
        z = M1[2]/M1[3]
        v1L = np.array([x0, y0, z0])
        v2L = np.array([x, y, z])
        a = x-x0
        b = y-y0
        c = z-z0

        #Camera 2
        invR2 = LA.inv(P2[0:3,0:3])
        m1T2 = -1*P2[:,3]
        C2 = np.dot(invR2, m1T2)
        x1 = C2[0]
        y1 = C2[1]
        z1 = C2[2]
        m2 = np.array([[col_2], [row_2], [1]]);
        M2 = np.dot(LA.pinv(P2), m2)
        x = M2[0]/M2[3]
        y = M2[1]/M2[3]
        z = M2[2]/M2[3]
        v1R = np.array([x1, y1, z1])
        v2R = np.array([x, y, z])
        d = x-x1
        e = y-y1
        f = z-z1

        A11 = (a*a + b*b + c*c)
        A12 = -1*(a*d + e*b + f*c)
        A21 = -1*(a*d + e*b + f*c)
        A22 = d*d + e*e + f*f
        A = np.array([[A11, A12], [A21, A22]])
        A = np.squeeze(A) #get rid of 3rd dimension
        v = np.array([[(x1-x0)*a + (y1-y0)*b + (z1-z0)*c], [(x0-x1)*d + (y0-y1)*e + (z0-z1)*f]])
        v = np.squeeze(v) #get rid of 3rd dimension
        invA = LA.inv(A)
        r = np.dot(invA,v)
        x_coord = x0+a*r[0]
        y_coord = y0+b*r[0]
        z_coord = z0+c*r[0]
        M = np.array([x_coord, y_coord, z_coord])

        #compute distance to each ray from the estimated 3D location
        v1L = v1L.transpose()
        v2L = v2L.transpose()
        v1R = v1R.transpose()
        v2R = v2R.transpose()

        d1 = LA.norm(np.cross(np.subtract(v1L, v2L),np.subtract(M.transpose(),v2L)))/LA.norm(np.subtract(v1L,v2L))
        d2 = LA.norm(np.cross(np.subtract(v1R, v2R),np.subtract(M.transpose(),v2R)))/LA.norm(np.subtract(v1R,v2R))
        err1 = d1 + d2;

        #project the estimated 3D position onto image, then find distance from original position
        m1rn = np.dot(P1,np.vstack((M,[1])))
        m2rn = np.dot(P2,np.vstack((M,[1])))
        m1r = m1rn/m1rn[2]
        m2r = m2rn/m2rn[2]
        err2 = np.sqrt(np.sum(np.square(m1r[0:2]-m1[0:2]))) + np.sqrt(np.sum(np.square(m2r[0:2]-m2[0:2])))

        
        return (x_coord[0], y_coord[0], z_coord[0], err1, err2)

#---------------------------------------------------------
def getthresholdedimg(im):

	# this function take RGB image.Then convert it into HSV for easy colour detection 
	# and threshold it with yellow and blue part as white and all other regions as black.Then return that image
	
	global imghsv
	imghsv = cv.CreateImage(cv.GetSize(im),8,3)
	
	# Convert image from RGB to HSV
	cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)
					
	# creates images for blue 
	imgblue   = cv.CreateImage(cv.GetSize(im),8,1)
	
	# creates blank image to which color images are added
	imgthreshold = cv.CreateImage(cv.GetSize(im),8,1)
	
	# determine HSV color thresholds for yellow, blue, and green
	# cv.InRange(src, lowerbound, upperbound, dst)
	# for imgblue, lowerbound is 95, and upperbound is 115
	cv.InRangeS(imghsv, cv.Scalar(55,110,110), cv.Scalar(155,255,255), imgblue  )
	
	# add color thresholds to blank 'threshold' image
	cv.Add(imgthreshold, imgblue,   imgthreshold)

	#return imgthreshold
	return imgblue
#---------------------------------------------------------
#img is an image (passed in by reference)
#sideName is for output printing purposes
#this returns an x and y coordinate of the blimp (x = col, y = row)
def procImg(img,sideName,dispFlag):

        #creates empty images of the same size
        imdraw = cv.CreateImage(cv.GetSize(img), 8, 3)
        #put the smoothed image here
        imgSmooth = cv.CreateImage(cv.GetSize(img), 8, 3)
        #put thresholded image here
        imgMask = cv.CreateImage(cv.GetSize(img), 8, 1)

        cv.SetZero(imdraw)
        cv.Smooth(img, imgSmooth, cv.CV_GAUSSIAN, 3, 0) #Gaussian filter the image
        imgbluethresh = getthresholdedimg(img) #Get a color thresholed binary image
        imgMask = imgbluethresh
        cv.Erode(imgbluethresh, imgbluethresh, None,  3)
        cv.Dilate(imgbluethresh, imgbluethresh, None, 10)
        #img2 = cv.CloneImage(imgbluethresh)
        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(imgbluethresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)

        centroidx = 0
        centroidy = 0
        prevArea = 0
        pt1 = (0, 0)
        pt2 = (0, 0)

        while contour:
                #find the area of each collection of contiguous points (contour)
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()

                #get the largest contour
                area = bound_rect[2]*bound_rect[3];

                #if dispFlag:
                #        print("Area= " + str(area))
                        
                if (area > prevArea and area > 3000):
                        pt1 = (bound_rect[0], bound_rect[1])
                        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])                        

        # Draw bounding rectangle
        cv.Rectangle(img, pt1, pt2, cv.CV_RGB(255,0,0), 3)

        # calculating centroid
        centroidx = cv.Round((pt1[0]+pt2[0])/2)
        centroidy = cv.Round((pt1[1]+pt2[1])/2)

        if (centroidx == 0 or centroidy == 0):
                print ("no blimp detected from " + sideName)
        else:
                print(sideName + " centroid x:" + str(centroidx))
                print(sideName + " centroid y:" + str(centroidy))
                
        print("")

        if dispFlag:
                small_thresh = cv.CreateImage((int(dispScale1*cv.GetSize(imgbluethresh)[0]), int(dispScale1*cv.GetSize(imgbluethresh)[1])), 8, 1)
                cv.Resize(imgMask, small_thresh)
                cv.Threshold(small_thresh, small_thresh, 0, 255, cv.CV_THRESH_BINARY)
                cv.ShowImage(sideName + "_threshold", small_thresh)
                cv.WaitKey(100)

                small_hsv = cv.CreateImage((int(0.25*cv.GetSize(imghsv)[0]), int(0.25*cv.GetSize(imghsv)[1])), 8, 3)
                cv.Resize(imghsv, small_hsv)

                small_hsv_h = cv.CreateImage((int(0.25*cv.GetSize(imghsv)[0]), int(0.25*cv.GetSize(imghsv)[1])), 8, 1)
                small_hsv_s = cv.CreateImage((int(0.25*cv.GetSize(imghsv)[0]), int(0.25*cv.GetSize(imghsv)[1])), 8, 1)
                small_hsv_v = cv.CreateImage((int(0.25*cv.GetSize(imghsv)[0]), int(0.25*cv.GetSize(imghsv)[1])), 8, 1)
                small_hsv_x = cv.CreateImage((int(0.25*cv.GetSize(imghsv)[0]), int(0.25*cv.GetSize(imghsv)[1])), 8, 1)
                
                cv.Split(small_hsv, small_hsv_h, small_hsv_s, small_hsv_v, None)
                cv.ShowImage(sideName + "_hsv", small_hsv)
                cv.WaitKey(100)

        return (centroidx, centroidy)


        
#---------------------------------------------------------
#!!Need to be on the local WID network to be able to grab images from the cameras
#grab a frame from the east camera, store it to disk
fname_east = './/east.jpg'
url_east = 'http://10.129.20.11/snapshot/view0.jpg'

#grab a frame from the west camera, store it to disk
fname_west = './/west.jpg'
url_west = 'http://10.129.20.12/snapshot/view0.jpg'

# three windows that will open upon execution
cv.NamedWindow("west",cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("east",cv.CV_WINDOW_AUTOSIZE)

# extra images to show intermediate tracking results
dispMore = 1
if dispMore:
        cv.NamedWindow("west_threshold",cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow("east_threshold",cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow("west_hsv",cv.CV_WINDOW_AUTOSIZE)
        cv.NamedWindow("east_hsv",cv.CV_WINDOW_AUTOSIZE)

#Live images from the IP cameras
#(if not live, then this file needs to be in folder with a bunch of images)
#(if live, then need to be local at WID)
liveIP = 0
if liveIP == 0:
        #need to be in directory with a bunch of images
        dirList = os.listdir(os.getcwd())
        num_base = 0
        both_offset = 10
        num_imgs = 145 - both_offset
        east_offset = 0 + both_offset
        west_offset = 147 + both_offset
        

#address of the control server
ip = "md-red5.discovery.wisc.edu"
port = 7779
size = 1024

#first get a connection to the server
#s = connect(ip,port)

dispScale1 = 0.35
dispScale2 = 0.25


while(1):
        if liveIP:
                #capture images from cameras, store images to file
                urllib.urlretrieve(url_west,fname_west)
                urllib.urlretrieve(url_east,fname_east)
        else:
                num_base = (num_base + 1)%(num_imgs)
                west_num = west_offset + num_base
                east_num = east_offset + num_base
                fname_west = dirList[west_num]
                fname_east = dirList[east_num]
                cv.WaitKey(2000) #wait for 2 seconds so I can see the output

        #open the images from file
        frame_west = cv.LoadImage(fname_west,cv.CV_LOAD_IMAGE_COLOR);
        frame_east = cv.LoadImage(fname_east,cv.CV_LOAD_IMAGE_COLOR);

        #find the blimp with one camera, frame is passed in by reference
        centroids = procImg(frame_west,"west",dispMore)  
        centx_west = centroids[0]
        centy_west = centroids[1]

        #find the blimp with one camera, frame is passed in by reference
        centroids = procImg(frame_east,"east",dispMore)        
        centx_east = centroids[0]
        centy_east = centroids[1]

        #decimate the resulting images
        small_west = cv.CreateImage((int(dispScale1*cv.GetSize(frame_west)[0]), int(dispScale1*cv.GetSize(frame_west)[1])), 8, 3)
        small_east = cv.CreateImage((int(dispScale1*cv.GetSize(frame_east)[0]), int(dispScale1*cv.GetSize(frame_east)[1])), 8, 3)
        cv.Resize(frame_west, small_west)
        cv.Resize(frame_east, small_east)


        #display the images with the blimp outlined
        cv.ShowImage("west", small_west)
        cv.WaitKey(100)
        cv.ShowImage("east", small_east)
        cv.WaitKey(100)

        if (centx_west != 0 and centy_west != 0 and centx_east != 0 and centy_east != 0):
                #get the 3D location of the blimp
                coord3D = triang_3D(centx_west, centy_west, centx_east, centy_east)

                print("x_3d: " + str(coord3D[0]))
                print("y_3d: " + str(coord3D[1]))
                print("z_3d: " + str(coord3D[2]))
                print("err1: " + str(coord3D[3]))
                print("err2: " + str(coord3D[4]))
        

##                #send the 3D location to the control server
##                try:
##                        #x,y,z = getPosition()
##                        msg = "" + str(coord3D[0]) + "," + str(coord3D[1]) + "," + str(coord3D[2]) + "\n"
##                        s.send(msg)
##                        #time.sleep(1)
##                except Exception as err:
##                        print("disconnected")
##                        #we got disconnected somehow, reconnect
##                        s = connect(ip,port)
        print("-----------------------------------")
            

######################################################

#!/usr/bin/python

# import system modules
import cv2.cv as cv
import urllib
import msvcrt
import numpy as np
from numpy import linalg as LA

global imghsv
global x_3d, y_3d, z_3d

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


#The following function takes coordinates from the images and convertes them to 3D spatial positions
#The calibration constants are in R1, T1, R2, and T2 for cameras 1 (west) and 2 (east)
#These constants are produced by matlab code that is available here:
#http://www.vision.caltech.edu/bouguetj/calib_doc/
def triang_3D(col_1, row_1, col_2, row_2) :
        global x_3d, y_3d, z_3d
        #R matrix for camera 1 (west side)
        R1 = np.array([[-74.2709, 637.41, -255.7461], [865.2027, 273.6518, -92.0415], [0.1602, 0.3172, -0.9347]])
        #T matrix for camera 1
        T1 = np.array([[1.3248e5], [4.1268e4], [505.0954]])
        P1 = np.hstack((R1, T1))

        #R matrix for camera 2 (east side)
        R2 = np.array([[-20.0487, 179.5963, -666.7510], [751.5431, -397.57, -330.23], [-0.2329, -0.5675, -0.7898]])
        #T matrix for camera 2
        T2 = np.array([[3.7547e5], [3.3423e5], [907.6034]])
        P2 = np.hstack((R2, T2))

        #blimp position from camera 1
        #col_1 = 411
        #row_1 = 382
        #m1 = np.array([
        #blimp position from camera 2
        #col_2 = 531
        #row_2 = 178


        #translated from matlab:

        #Camera 1
        invR1 = LA.inv(R1)
        m1T1 = -1*T1
        C1 = np.dot(invR1, m1T1)
        x0 = C1[0]
        y0 = C1[1]
        z0 = C1[2]
        m1 = np.array([[col_1], [row_1], [1]]);
        M1 = np.dot(LA.pinv(P1), m1)
        x = M1[0]/M1[3]
        y = M1[1]/M1[3]
        z = M1[2]/M1[3]
        a = x-x0
        b = y-y0
        c = z-z0

        #Camera 2
        invR2 = LA.inv(R2)
        m1T2 = -1*T2
        C2 = np.dot(invR2, m1T2)
        x1 = C2[0]
        y1 = C2[1]
        z1 = C2[2]
        m2 = np.array([[col_2], [row_2], [1]]);
        M2 = np.dot(LA.pinv(P2), m2)
        x = M2[0]/M2[3]
        y = M2[1]/M2[3]
        z = M2[2]/M2[3]
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

        x_3d = x_coord
        y_3d = y_coord
        z_3d = z_coord


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
	cv.InRangeS(imghsv, cv.Scalar(55,100,100), cv.Scalar(155,255,255), imgblue  )
	
	# add color thresholds to blank 'threshold' image
	cv.Add(imgthreshold, imgblue,   imgthreshold)

	return imgthreshold


#!!Need to be on the local WID network to be able to grab images from the cameras
#grab a frame from the east camera, store it to disk
fname_east = 'C://Users//Jeremy//Documents//blimp//east.jpg'
url_east = 'http://10.129.20.11/snapshot/view0.jpg'
urllib.urlretrieve(url_east,fname_east)

#grab a frame from the west camera, store it to disk
fname_west = 'C://Users//Jeremy//Documents//blimp//west.jpg'
url_west = 'http://10.129.20.12/snapshot/view0.jpg'
urllib.urlretrieve(url_west,fname_west)

frame_west = cv.LoadImageM(fname_west,cv.CV_LOAD_IMAGE_COLOR);
frame_size = cv.GetSize(frame_west)

# blank images to which images are added later
test = cv.CreateImage(cv.GetSize(frame_west),8,3)
img2 = cv.CreateImage(cv.GetSize(frame_west),8,3)

# three windows that will open upon execution
cv.NamedWindow("west",cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("east",cv.CV_WINDOW_AUTOSIZE)

# blank lists to store coordinates of blue blob
blue   = []

while(1):
        urllib.urlretrieve(url_west,fname_west)
        urllib.urlretrieve(url_east,fname_east)

        frame_west = cv.LoadImageM(fname_west,cv.CV_LOAD_IMAGE_COLOR);
        frame_east = cv.LoadImageM(fname_east,cv.CV_LOAD_IMAGE_COLOR);

        imdraw_west = cv.CreateImage(cv.GetSize(frame_west), 8, 3)
        imdraw_east = cv.CreateImage(cv.GetSize(frame_east), 8, 3)

        #process west image
        cv.SetZero(imdraw_west)
        cv.Smooth(frame_west, frame_west, cv.CV_GAUSSIAN, 3, 0)
        imgbluethresh = getthresholdedimg(frame_west)
        cv.Erode(imgbluethresh, imgbluethresh, None,  3)
        cv.Dilate(imgbluethresh, imgbluethresh, None, 10)
        img2 = cv.CloneImage(imgbluethresh)
        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(imgbluethresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        # blank list into which points for bounding rectangles around blobs are appended
        points = []
        while contour:

                # Draw bounding rectangles
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()
                #print contour  # not sure why print contour

                # for more details about cv.BoundingRect,see documentation
                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                cv.Rectangle(frame_west, pt1, pt2, cv.CV_RGB(255,0,0), 1)

                # calculating centroids
                centroidx = cv.Round((pt1[0]+pt2[0])/2)
                centroidy = cv.Round((pt1[1]+pt2[1])/2)

                # identifying if blue blobs exist and adding centroids to corresponding lists.
                # note that the lower and upper bounds correspond to the the lower and upper bounds
                # in the getthresholdedimg(im): function earlier in the script.
                # e.g., yellow has a lowerbound of 95 and upper bound of 115 in both sections of code
                if (55 < cv.Get2D(imghsv,centroidy,centroidx)[0] < 155): 
                        blue.append((centroidx,centroidy))

        # draw colors in windows; exception handling is used to avoid IndexError.   
        # after drawing is over, centroid from previous part is removed from list by pop. 
        # so in next frame, centroids in this frame become initial points of line to draw   

        # draw blue box around blue blimp blob
        try:
                cv.Circle(imdraw_west, blue[1], 5, (255,0,0))
                cv.Line(imdraw_west, blue[0], blue[1], (255,0,0), 3, 8, 0) 
                blue.pop(0)
                print("west centroid x:" + str(centroidx))
                print("west centroid y:" + str(centroidy))
                print("")       
        except IndexError:
                print "no blimp detected"   


        # adds 
        cv.Add(test,imdraw_west,test)

        centx_west = centroidx
        centy_west = centroidy


        #process east image
        cv.SetZero(imdraw_east)
        cv.Smooth(frame_east, frame_east, cv.CV_GAUSSIAN, 3, 0)
        imgbluethresh = getthresholdedimg(frame_east)
        cv.Erode(imgbluethresh, imgbluethresh, None,  3)
        cv.Dilate(imgbluethresh, imgbluethresh, None, 10)
        img2 = cv.CloneImage(imgbluethresh)
        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(imgbluethresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        # blank list into which points for bounding rectangles around blobs are appended
        points = []
        while contour:

                # Draw bounding rectangles
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()
                #print contour  # not sure why print contour

                # for more details about cv.BoundingRect,see documentation
                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                cv.Rectangle(frame_east, pt1, pt2, cv.CV_RGB(255,0,0), 1)

                # calculating centroids
                centroidx = cv.Round((pt1[0]+pt2[0])/2)
                centroidy = cv.Round((pt1[1]+pt2[1])/2)

                # identifying if blue blobs exist and adding centroids to corresponding lists.
                # note that the lower and upper bounds correspond to the the lower and upper bounds
                # in the getthresholdedimg(im): function earlier in the script.
                # e.g., yellow has a lowerbound of 95 and upper bound of 115 in both sections of code
                if (55 < cv.Get2D(imghsv,centroidy,centroidx)[0] < 155): 
                        blue.append((centroidx,centroidy))

        # draw colors in windows; exception handling is used to avoid IndexError.   
        # after drawing is over, centroid from previous part is removed from list by pop. 
        # so in next frame, centroids in this frame become initial points of line to draw   

        # draw blue box around blue blimp blob
        try:
                cv.Circle(imdraw_east, blue[1], 5, (255,0,0))
                cv.Line(imdraw_east, blue[0], blue[1], (255,0,0), 3, 8, 0) 
                blue.pop(0)
                print("east centroid x:" + str(centroidx))
                print("east centroid y:" + str(centroidy))
                print("")       
        except IndexError:
                print "no blimp detected"   


        # adds 
        cv.Add(test,imdraw_east,test)        

        centx_east = centroidx
        centy_east = centroidy

        cv.ShowImage("west", frame_west)
        cv.WaitKey(100)


        cv.ShowImage("east", frame_east)
        cv.WaitKey(100)

        triang_3D(centx_west, centy_west, centx_east, centy_east)

        print("x_3d: " + str(x_3d))
        print("y_3d: " + str(y_3d))
        print("z_3d: " + str(z_3d))

######################################################

#!/usr/bin/python

# import system modules
import cv2.cv as cv
#import cv
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

# capture from m4v
#capture = cv.CaptureFromFile('/Users/glenaronson/Desktop/blimp_large.m4v')
capture = cv.CaptureFromFile('C:/Users/Jeremy/Documents/GitHub/blimp_blobs/blimp.m4v')
#capture = cv.CaptureFromFile("C:\Users\Jeremy\Documents\GitHub\blimp_blobs\blimp.m4v")
#capture = cv.CaptureFromFile('http://10.129.20.11/snapshot/view0.jpg')
#capture = cv.CaptureFromFile('rtsp://10.129.20.11/video.sav')
#http://10.129.20.11/goform/stream?cmd=get&channel=0
#capture = cv.CaptureFromCAM(0)
#capture = cv.CaptureFromFile("C:/Users/Jeremy/Documents/GitHub/blimp_blobs/Untitled 13.avi")
#capture = cv.CaptureFromFile("Untitled 13.avi")
frame = cv.QueryFrame(capture)
frame_size = cv.GetSize(frame)

#frame = cv.LoadImageM("C:/Users/Jeremy/Documents/GitHub/blimp_blobs/test_images/SmallBlimp/(10.129.20.12)_1_2012_08_21_04_12_07.jpg")
#frame_size = cv.GetSize(frame)

# blank images to which images are added later
test = cv.CreateImage(cv.GetSize(frame),8,3)
img2 = cv.CreateImage(cv.GetSize(frame),8,3)

# three windows that will open upon execution
cv.NamedWindow("Real",0)

# blank lists to store coordinates of blue blob
blue   = []


while(1):
	# captures feed from video in color
	color_image = cv.QueryFrame(capture)
	#color_image = frame
	
	# ??
	imdraw = cv.CreateImage(cv.GetSize(frame), 8, 3)
	
	# ??
	cv.SetZero(imdraw)
	cv.Flip(color_image,color_image, 1)
	cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
	# ??
	imgbluethresh = getthresholdedimg(color_image)
	cv.Erode(imgbluethresh, imgbluethresh, None,  3)
	cv.Dilate(imgbluethresh, imgbluethresh, None, 10)
	# ??
	img2 = cv.CloneImage(imgbluethresh)
	# ??
	storage = cv.CreateMemStorage(0)
	contour = cv.FindContours(imgbluethresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
	
	# blank list into which points for bounding rectangles around blobs are appended
	points = []	

	# this is the new part here. ie use of cv.BoundingRect()
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
		cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

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
		cv.Circle(imdraw, blue[1], 5, (255,0,0))
		cv.Line(imdraw, blue[0], blue[1], (255,0,0), 3, 8, 60) 
		blue.pop(0)
		print("centroid x:" + str(centroidx))
		print("centroid y:" + str(centroidy))
		print("")		
	except IndexError:
		print "no blimp detected"	


	# adds 
	cv.Add(test,imdraw,test)
	
	# display windows previously created
	cv.ShowImage("Real", color_image) 
	
	if cv.WaitKey(33) == 1048603:
		cv.DestroyWindow("Real")
		break
######################################################

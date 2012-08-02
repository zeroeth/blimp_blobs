#!/usr/bin/python
import cv
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

	'''this function take RGB image.Then convert it into HSV for easy colour detection and threshold it with yellow and blue part as white and all other regions as black.Then return that image'''
	global imghsv
	imghsv=cv.CreateImage(cv.GetSize(im),8,3)
	cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)				# Convert image from RGB to HSV

	# A little change here. Creates images for blue and yellow (or whatever color you like).
	imgyellow=cv.CreateImage(cv.GetSize(im),8,1)
	imgblue=cv.CreateImage(cv.GetSize(im),8,1)
	imggreen=cv.CreateImage(cv.GetSize(im),8,1) # glen added this

	imgthreshold=cv.CreateImage(cv.GetSize(im),8,1)

	cv.InRangeS(imghsv,cv.Scalar(20,100,100),cv.Scalar(30,255,255),imgyellow)	# Select a range of yellow color in HSV, where 20 is low H and 30 is high H
	cv.InRangeS(imghsv,cv.Scalar(100,100,100),cv.Scalar(120,255,255),imgblue)	# Select a range of blue color 
	cv.InRangeS(imghsv,cv.Scalar(150,100,100),cv.Scalar(170,255,255),imggreen) 	# glen added this; select a range of green color
	cv.Add(imgthreshold,imgyellow,imgthreshold)
	cv.Add(imgthreshold,imgblue,imgthreshold)
	cv.Add(imgthreshold,imggreen,imgthreshold)
	
	return imgthreshold

capture=cv.CaptureFromCAM(0)
frame = cv.QueryFrame(capture)
frame_size = cv.GetSize(frame)
test=cv.CreateImage(cv.GetSize(frame),8,3)
img2=cv.CreateImage(cv.GetSize(frame),8,3)
cv.NamedWindow("Real",0)
cv.NamedWindow("Threshold",0)
cv.NamedWindow("final",0)

#	Create two lists to store co-ordinates of blobs
blue=[]
yellow=[]
purple=[] # glen added this

while(1):
	color_image = cv.QueryFrame(capture)
	imdraw=cv.CreateImage(cv.GetSize(frame),8,3)
	cv.SetZero(imdraw)
	cv.Flip(color_image,color_image,1)
	cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
	imgyellowthresh=getthresholdedimg(color_image)
	cv.Erode(imgyellowthresh,imgyellowthresh,None,3)
	cv.Dilate(imgyellowthresh,imgyellowthresh,None,10)
	img2=cv.CloneImage(imgyellowthresh)
	storage = cv.CreateMemStorage(0)
	contour = cv.FindContours(imgyellowthresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
	points = []	

#	This is the new part here. ie Use of cv.BoundingRect()
	while contour:
		# Draw bounding rectangles
		bound_rect = cv.BoundingRect(list(contour))
		contour = contour.h_next()
		print contour
		# for more details about cv.BoundingRect,see documentation
		pt1 = (bound_rect[0], bound_rect[1])
		pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
		points.append(pt1)
		points.append(pt2)
		cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

	#	Calculating centroids

		centroidx=cv.Round((pt1[0]+pt2[0])/2)
		centroidy=cv.Round((pt1[1]+pt2[1])/2)

	#	Identifying if blue or yellow blobs and adding centroids to corresponding lists	
		if (20<cv.Get2D(imghsv,centroidy,centroidx)[0]<30):
			yellow.append((centroidx,centroidy))
		elif (100<cv.Get2D(imghsv,centroidy,centroidx)[0]<120): # 100 120
			blue.append((centroidx,centroidy))
		elif (150<cv.Get2D(imghsv,centroidy,centroidx)[0]<170):
			purple.append((centroidx,centroidy))

# 		Now drawing part. Exceptional handling is used to avoid IndexError.	After drawing is over, centroid from previous part is #		removed from list by pop. So in next frame,centroids in this frame become initial points of line to draw.		
	try:
		cv.Circle(imdraw,yellow[1],5,(0,255,255))
		cv.Line(imdraw,yellow[0],yellow[1],(0,255,255),3,8,0)
		yellow.pop(0)
	except IndexError:
		print "Just wait for yellow"

	try:
		cv.Circle(imdraw,blue[1],5,(255,0,0))
		cv.Line(imdraw,blue[0],blue[1],(255,0,0),3,8,0)
		blue.pop(0)			
	except IndexError:
		print "just wait for blue"	
	
# glen added this block
	try:
		cv.Circle(imdraw,purple[1],5,(255,0,255))
		cv.Line(imdraw,purple[0],purple[1],(255,0,255),3,8,0)
		purple.pop(0)			
	except IndexError:
		print "just wait for purple"	
	
	cv.Add(test,imdraw,test)

	cv.ShowImage("Real",color_image) 
	cv.ShowImage("Threshold",img2)	
	cv.ShowImage("final",test)
	if cv.WaitKey(33)==1048603:
		cv.DestroyWindow("Real")
		cv.DestroyWindow("Threshold")
		cv.DestroyWindow("final")
		break
######################################################
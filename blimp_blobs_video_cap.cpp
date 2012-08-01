#include "cv.h"
#include "highgui.h"

using namespace cv;

int main(int, char**)
{
    int threshold1 = 0;
    int threshold2 = 30;

    int aperture_sizes[] = {3, 5, 7};
    int aperture_index = 0;
    int aperture   = aperture_sizes[aperture_index];

    VideoCapture cap(0); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;

    Mat edges;
    namedWindow("edges",1);
    namedWindow("original",1);

    createTrackbar("threshold1", "edges", &threshold1,   100);
    createTrackbar("threshold2", "edges", &threshold2,   100);
    createTrackbar("aperture",   "edges", &aperture_index, 2);

    for(;;)
    {
        aperture = aperture_sizes[aperture_index];

        Mat frame;
        cap >> frame; // get a new frame from camera
        cvtColor(frame, edges, CV_BGR2GRAY);
        GaussianBlur(edges, edges, Size(7,7), 1.5, 1.5);
        Canny(edges, edges, threshold1, threshold2, aperture);
        imshow("edges", edges);
        imshow("original", frame);
        if(waitKey(1) >= 0) break;
    }
    // the camera will be deinitialized automatically in VideoCapture destructor
    return 0;
}

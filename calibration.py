
import cv2
from cv2 import rectangle
import numpy as np
from yaspin import yaspin
import os
from datetime import datetime
import multiprocessing



sp = yaspin()
sp.start()

sp.color="green"

sp.start()
print(datetime.now())

if not os.path.exists("./logs"):
    os.mkdir("./logs")
# for dirpath,dirnames, filenames in os.walk("./logs"):
#     if filenames :
        



cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# video recording settings for opencv

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('outpy.avi',fourcc, 10, (frame_width,frame_height))

# settings for finding aruco 


dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)
parameters = cv2.aruco.DetectorParameters_create() # Initialize the detector parameters using default values



# global variables 

n=0
l=[]
trajectory=[]
trajectory_and_time=[]
two_frame=[]
delta_x=0
delta_y=0
state=0

sp.stop()

class readImage():

    def __init__(self,VideoCapture=0,Width=1280,Height=720):

        self.cap=cv2.VideoCapture(VideoCapture)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, Width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Height)

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        self.out = cv2.VideoWriter('outpy.avi',fourcc, 10, (frame_width,frame_height))

    def getCapture(self):
        ret, Image = self.cap.read()
        if ret == False: # end of video (perhaps)c
            print("camera is busy or is not connected ........")
            return False
        else: 
            return Image,ret

    def DisplayPLusSpecification(self,frame,**kwargs):

        if kwargs["delta_x"] & kwargs["delta_y"]:
                cv2.putText(frame, f"you moved delta_x={int(args[0])}cm and delta_y={int(args[1])} cm", (20,20), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)

        cv2.imshow('win1',Image)

    def __del__(self):

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()


        



     
class processingImage():

    def __init__(self,Image,DictUse=cv2.aruco.DICT_5X5_50) -> None:
        self.dictionary = cv2.aruco.Dictionary_get(dictionary)
        self.parameters = cv2.aruco.DetectorParameters_create() # Initialize the detector parameters using default values        
        self.Image=Image

    def FindAruco(self,frame):
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary=self.dictionary, parameters=self.parameters)
        # need to fix it 
        if np.any(markerCorners):
            arr = np.concatenate(markerCorners, axis=0)
            # get the center of the marker and put red point on it       
            x_axis=(arr[0,0,0]+arr[0,1,0])/2
            y_axis=(arr[0,3,1]+arr[0,1,1])/2
            cv2.circle(frame, (int(x_axis), int(y_axis)), 5, (0, 0, 255), -1)
            # draw rectangle aroud the marker 
            int_corners = np.int0(markerCorners)
            cv2.polylines(frame, int_corners, True, (0, 255, 0), 5)
            # find the relation betwween the merkare size and resolution 


            aruco_perimeter = cv2.arcLength(markerCorners[0], True)
            # Pixel to cm ratio
            pixel_cm_ratio = aruco_perimeter / 40 #it depends on the perimeter of the aruco

        return markerCorners, markerIds, rejectedCandidates,pixel_cm_ratio



while True:



    # Capture frame-by-frame
    ret, Image = cap.read()

    if ret == False: # end of video (perhaps)c
        print("camera is busy or is not connected ........")
        break
    


    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(Image, dictionary, parameters=parameters)

    if np.any(markerCorners):
        arr = np.concatenate(markerCorners, axis=0)
        x_axis=(arr[0,0,0]+arr[0,1,0])/2
        y_axis=(arr[0,3,1]+arr[0,1,1])/2
        cv2.circle(Image, (int(x_axis), int(y_axis)), 5, (0, 0, 255), -1)
        int_corners = np.int0(markerCorners)
        cv2.polylines(Image, int_corners, True, (0, 255, 0), 5)
        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(markerCorners[0], True)
        print(aruco_perimeter)
        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 40
        # print(x_axis,y_axis)







    if cv2.waitKey(30) & 0xFF == ord('s'):
        n=n+1

        if n==1:
            two_frame=[]
            trajectory=[]
            two_frame.append((int(x_axis), int(y_axis)))
            out.write(Image)
            


        l.append([x_axis,y_axis])
        # print(l[0][0])


        if n==2:

            two_frame.append((int(x_axis), int(y_axis)))
            delta_x=abs(l[0][0]-l[1][0])/pixel_cm_ratio
            delta_y=abs(l[0][1]-l[1][1])/pixel_cm_ratio
            out.release()
            with open(f"./logs/trajectory-{datetime.now()}.txt","w") as f :

                sp.ok("✅ file generated and saved  ")
                # print(len(trajectory))
                for item in trajectory_and_time :
                    f.write(str(item)+"\n")
                trajectory_and_time.clear()

            l=[]
            n=0

    if n==1:
        # print(trajectory)
        trajectory.append([x_axis,y_axis])
        trajectory_and_time.append([(x_axis,y_axis),str(datetime.now())])
        for dot in trajectory:
                cv2.circle(Image, (int(dot[0]), int(dot[1])), 1, (0, 0, 255), -1)
                






    cv2.putText(Image, f"you moved delta_x={int(delta_x)}cm and delta_y={int(delta_y)} cm", (20,20), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    for frame in two_frame:
        cv2.circle(Image, frame, 5, (0, 255, 0), -1)
    if len(two_frame)==2:

        Image = cv2.arrowedLine(Image,(two_frame[1][0],two_frame[0][1]),two_frame[0],(0, 0, 255), 2)
        Image = cv2.arrowedLine(Image,two_frame[1],(two_frame[1][0],two_frame[0][1]),(0, 0, 255), 2)



        # cv2.putText(Image, f"you moved delta_x={int(delta_x)}cm and delta_y={int(delta_y)} cm", (10,10), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        # cv2.putText(Image, f"delta_y={int(delta_y)} cm", (int((two_frame[1][0]+two_frame[0][0])/2),two_frame[0][0]), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    cv2.imshow('win1',Image)
    out.write(Image)



    # to quit the program you should press "q"

    if cv2.waitKey(30) & 0xFF == ord('q'): 
        break
    

cap.release()
out.release()
cv2.destroyAllWindows()
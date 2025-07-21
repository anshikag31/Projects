import cv2  #helps in working with image and video processing functions

#face detection
#face features
#cascadeclassifier captures all the face features(eyes,nose,mouth)

face_Cap=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#ENABLING CAMERA

#make the camera on
#runtime camera enabling we take 0 in bracket
video_cap=cv2.VideoCapture(0)

#disable the camera only for a particular key

while True:
    #read the images
    ret,video_data=video_cap.read()

    #TO SHOW THE BOX

    # first we need to convert images into black and white(first it's converted into gray(b&w) color to know about the body parts(eyebrows,eyes,nose) and then again rearrange and convert to color)
    col=cv2.cvtColor(video_data,cv2.COLOR_BGRA2GRAY)

    #cover up face structures
    faces=face_Cap.detectMultiScale(
          col,
          scaleFactor=1.1,
          minNeighbors=5,
          minSize=(30,30),
          flags=cv2.CASCADE_SCALE_IMAGE
    )

    #now create the box
    #rectangle provides a square bracket
    #color(0,255,0) and width(2)
    #h,w=height and width of box
    #x,y=height and width of the person's face
    for(x,y,w,h) in faces:
          cv2.rectangle(video_data,(x,y),(x+w,y+h),(0,255,0),2)


    #show the images in frame (develop a frame)
    cv2.imshow("live_video",video_data)
    #close the video (here by pressing a we can close the camera)
    #waitkey used to stop the video for a particular time period
    if cv2.waitKey(10)==ord("a"):
           break
video_cap.release()




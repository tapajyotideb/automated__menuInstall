import cv2

#cv2.video capture is the command to open the camera and cv2 is module
capture=cv2.VideoCapture(0)
#ret will click the photo and photo will save the pic
ret , photo=capture.read(0)
# to save the photo
cv2.imwrite ('/root/Desktop/Sagar.png', photo)
capture.release()

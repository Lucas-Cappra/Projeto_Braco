#====================#

#Author: Lucas Cappra

#====================#

import cv2 as cv
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import os
#====================#
# Stating to capture videos/webcam.
print("[INFO] starting video stream...")
capture = cv.VideoCapture(0) # Load the video capture, '0' for webcam or 'root/path.mp4' to specify video.
time.sleep(2.0)

#=========Variables.===========#

inform = 0
img_counter = 0

#=========Function set the width/height.===========#
def changeRes(width, height): # live Video
    capture.set(3,width)
    capture.set(4,height)

#========Camera capture filtring.============#
while True:
    isTrue, frame = capture.read()
    # converting to greyscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #blur
    blur  = cv.GaussianBlur(frame, (7,7), cv.BORDER_DEFAULT)
    # edge cascate
    cascate = cv.Canny(blur, 12, 175)
    # cv.imshow('Video', cascate)
    
    barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "{}".format(barcodeData)
        # if inform is different from the information, it will print
        if inform  != text: 
            print(text)
            inform = text
            continue
        cv.putText(frame, text, (x, y - 10),
        cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
             # show the output frame
    cv.imshow("Barcode Scanner", cascate)

    
    #======="P" for print;  "D" to stop capturing.=============#
    if cv.waitKey(1) & 0xFF==ord('p'):
        img_counter = img_counter+1
        print('Saving Image')
        cv.imwrite('Imagem{}.png'.format(img_counter), cascate)
        print(img_counter)
        
        continue

    if cv.waitKey(1) & 0xFF==ord('d'):
        capture.release()
        img_counter = 0
        break

#==========Start to analys the photo taken.============#
# for i in range (1, img_counter, 1):
image = cv.imread(f"C:\\Users\\USUARIO\\Documents\\vstudiocode\\Imagem1.png")
gray  = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
canny = cv.Canny(gray, 10, 150)
canny = cv.dilate(canny, None, iterations=1)
canny = cv.erode(canny, None, iterations=1)
ctns,_= cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#cv.drawContours(image, ctns, -1, (255,255,255), 2)

#==========Start to analys by borders.============#    
for c in ctns:
    epsilon = 0.015 *cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, epsilon, True)
    x,y,w,h = cv.boundingRect(approx)

    if len(approx) == 3:
        cv.putText(image, "Triangulo", (x-5, y-15),1,1,(255,255,255),1)
    if len(approx) == 4:
        aspect_ratio = float(w)/h
        if aspect_ratio == 1:
            cv.putText(image, "Quadrado", (x,y-20), 1,1,(255,255,255), 1)
        else:
            cv.putText(image, "Retangulo", (x,y-20), 1, 1, (255,255,255),1)
    if len(approx) == 5:
        cv.putText(image, "Pentagono", (x,y-20),1,1,(255,255,255),1)
    if len(approx) == 6:
        cv.putText(image, "Hexagono", (x, y-20), 1, 1, (255,255,255),1)
    if len(approx) == 10:
        cv.putText(image, "Decagono", (x, y-20),1, 1,(255,255,255),1)
    if len(approx) == 12:
        cv.putText(image, "Duodecagono", (x, y-20), 1, 1,(255,255,255),1)
    if len(approx) > 12:
        cv.putText(image, "circulo", (x, y-20), 1, 1, (255,255,255),1)

    cv.drawContours(image, [approx], -1, (255,255,255), 4)
    cv.imshow(f"image", image)
    cv.waitKey(1)
    continue

i = 0
cv.waitKey(0)
cv.destroyAllWindows()
import cv2 as cv

# reading videos
capture = cv.VideoCapture(0) # Load the video capture, '0' for webcam or 'root/path.mp4' to specify video.
img_counter = 0
# img = cv.imread('Projeto Braco\photo\caminhao.jpg')

def changeRes(width, height): # live Video
    capture.set(3,width)
    capture.set(4,height)

while True:
    isTrue, frame = capture.read()

    # converting to greyscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    #blur
    blur  = cv.GaussianBlur(frame, (7,7), cv.BORDER_DEFAULT)

    # edge cascate
    cascate = cv.Canny(blur, 12, 175)

    cv.imshow('Video', cascate)        

    if cv.waitKey(1) & 0xFF==ord('p'):  # pressing 'p', it prints the camera frame to a png image.
        img_counter = img_counter+1
        print('Saving Image')
        cv.imwrite('Imagem{}.png'.format(img_counter), cascate)
        print(img_counter)
        continue


    if cv.waitKey(1) & 0xFF==ord('d'): # pressing 'd' screen or when 'd' key is pressed. 
        break

capture.release()       #stop capturing

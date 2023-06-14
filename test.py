import cv2


cap = cv2.VideoCapture(0)

 

if not cap.isOpened():
    raise IOError("Cannot open webcam")

 

while True:
    ret, frame = cap.read()

    if ret:
        if frame.shape[0] > 0 and frame.shape[1] > 0:
            cv2.imshow('webcam', frame)
        else:
            print("Invalid frame dimensions")
    else:
        print("Failed to capture frame")

    cv2.imshow('webcam', frame)

    c = cv2.waitKey(1)

    if c == 27:

        break

 

cap.release()

cv2.destroyAllWindows()


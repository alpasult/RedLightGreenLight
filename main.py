import os
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args["video"])
firstFrame = None

start = time.time()
x_pos = 0
y_pos = 0
while True:
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame is None:
        firstFrame = gray
        continue
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cntsSorted = sorted(cnts, key=cv2.contourArea)
    print(len(cnts))
    if len(cntsSorted) > 0:
        c = cntsSorted[-1]
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if start <= time.time():
            file = "squidgame.mp3"
            os.system("afplay " + file)
            start = time.time() + 11

        if (x_pos + 50 > x > x_pos - 50 or y_pos + 50 > y > y_pos - 50) and start <= time.time() + 9:
            file = "gunshot.mp3"
            os.system("afplay " + file)
            exit()
        elif not start <= time.time() + 9:
            x_pos = x
            y_pos = y
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()

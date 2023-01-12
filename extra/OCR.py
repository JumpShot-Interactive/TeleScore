from doctest import OutputChecker
import cv2, pytesseract, imutils
from imutils.video import VideoStream
import os

output = None

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cv2.namedWindow("OCR")

vs = VideoStream(src=0, framerate=5).start()


while True:
    orgFrame = vs.read()

    #orgFrame = cv2.resize(orgFrame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(orgFrame, cv2.COLOR_BGR2GRAY)

    result = pytesseract.image_to_string(gray, lang="letsgodigital")
    os.system('CLS')
    print(result)

    cv2.imshow("OCR", gray)
    c = cv2.waitKey(1)
    if (c == 27):
        break


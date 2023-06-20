import cv2
import imutils
import numpy as np

def detection_plate(imgVehicle):
    imgPlate = None
    gray = cv2.cvtColor(imgVehicle, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    # equal_histogram = cv2.equalizeHist(gray)
    ret, thresh_gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    canny_image = cv2.Canny(thresh_gray, 250, 255)
    kernel = np.ones((3, 3), np.uint8)
    edged = cv2.dilate(canny_image, kernel, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    screenCnt = 0
    # vong lop tim contours
    for c in cnts:
        # tim contours giong bien so xe
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.083 * peri, True)
        (x, y, w, h) = cv2.boundingRect(c)
        # neu contours co 4 diem thi co the contours day la bien so xe
        if len(approx) == 4 and 7000 > cv2.contourArea(c) > 2000 and w > h and 280 > x > 70:
            imgPlate = gray[y:y + h+1, x:x + w+1]
            cv2.rectangle(imgVehicle, (x, y), (x + w, y + h), (0, 255, 0), 2)
            screenCnt = 1
            break

    if screenCnt == 0:
        detected = 0
        #print("No plate detected")
    else:
        detected = 1

    return detected ,cv2.cvtColor(imgPlate,cv2.COLOR_BGR2RGB), imgVehicle  #cv2.cvtColor(imgPlate,cv2.COLOR_BGR2RGB)


# img_name = "PlateCrop/platecrop.jpg"
# img = cv2.imread(img_name)
# cv2.imshow("img", cv2.cvtColor(img, cv2.COLOR_RGB2HSV))
# # imgplate = detection_plate(img)
# # cv2.imshow("plate",imgplate)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

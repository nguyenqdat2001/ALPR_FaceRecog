import cv2
import imutils
import numpy as np

def sort_contours_y(list_cnts):
    list_tren = []
    list_duoi = []
    lenth = len(list_cnts)
    for i in range(0, lenth):
        if  list_cnts[i][1] < 180:
            list_tren.append(list_cnts[i])
        else:
            list_duoi.append(list_cnts[i])
    return list_tren + list_duoi

def sort_contours_x(cnts):
    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))
    return cnts

def read_plate(imgPlate):

    img = cv2.resize(imgPlate, (570, 420))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph_image = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel, iterations=255)
    thres = cv2.adaptiveThreshold(morph_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 111, 20)

    contours = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sort_contours_x(contours)

    list_cnts = []
    list_char = []
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        # approximate the contour
        if (20<w<90) and (100<h<200) and (h/w>1.5):
            list_cnts.append(cv2.boundingRect(c))
    contours = sort_contours_y(list_cnts)
    for c in contours:
        (x, y, w, h) = c
        crop = thres[y:y + h, x:x + w]
        crop = cv2.resize(crop, dsize=(30, 60))
        crop = np.array(crop, dtype=np.float32)
        crop = crop.reshape(-1, 1800)
        list_char.append(crop)
    return list_char

# img = cv2.imread("Pictures/biensocrop0.jpg")
# print(model.readchar(read_plate(img)))

# plate = detection_plate(img)
# cv2.imshow("lol",plate)
# print(read_plate(plate))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

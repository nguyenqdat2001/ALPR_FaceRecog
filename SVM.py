import cv2
class SVM:
    def __init__(self):
        self.model_svm = cv2.ml.SVM_load('svm.xml')

    def readchar(self, list_c):
        plate_info = ""
        for c in list_c:
            result = self.model_svm.predict(c)[1]
            result = int(result[0, 0])
            if result <= 9:  # Neu la so thi hien thi luon
                result = str(result)
            else:  # Neu la chu thi chuyen bang ASCII
                result = chr(result)
            plate_info += result
        return plate_info

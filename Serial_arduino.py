from serial import Serial
import time

class Serial_Arduino():
    def __init__(self):
        self.status = 1
        try:
            self.arduino = Serial(port='COM3', baudrate=9600, timeout=1)
        except:
            print('NO COM PORT !!')
            self.status = 0

    def write_arduino(self, data):
        time.sleep(0.5)
        self.arduino.write(bytes(data, 'utf-8'))

    def close_arduino(self):
        self.arduino.close();

# On = "73 24 F8 03"
# Off = "AC F3 85 6D"
# arduino = Serial_Arduino()
# open = 2
# while 1:
#
#     if arduino.status == 1:
#         try:
#             arduino.write_arduino('1')
#         except:
#             print("Processing")
#     else: break





import sqlite3
import datetime

class Database():
    def __init__(self):
        self.connect = sqlite3.connect("database_rfid.db")

    def Insert_Or_Update_DB(self, plate="", stt="", date="", name=""):
        self.query = "INSERT INTO RFID(Plate, Status, Datetime, Name) VALUES('"+str(plate)+"','"+str(stt)+"','"+str(date)+"','"+str(name)+"')"
        self.connect.execute(self.query)
        self.connect.commit()

    def Get_Data_DB(self, name=""):
        # SELECT * from RFID WHERE ID = '180407' ORDER BY DATETIME DESC
        self.query = "SELECT * from RFID WHERE Name = '{}' ORDER BY DATETIME DESC".format(str(name))
        self.cusror = self.connect.execute(self.query)
        list_row = []
        for row in self.cusror:
            list_row.append(list(row))
        return list_row[0]

    def Get_Data_TB(self):
        self.query = "SELECT * FROM RFID ORDER BY DATETIME DESC"
        self.cusror = self.connect.execute(self.query)
        list_row = []
        for row in self.cusror:
            list_row.append(list(row))
        return list_row

    def Search_Plate(self, plate = ""):
        self.query = "SELECT * from RFID WHERE Plate = '{}' ORDER BY DATETIME DESC".format(plate)
        self.cusror = self.connect.execute(self.query)
        list_row = []
        for row in self.cusror:
            list_row.append(list(row))
        return list_row

    def Search_TT(self, msv=''):
        self.query = "SELECT * FROM SinhVien WHERE MSV = '{}'".format(str(msv))
        self.cusror = self.connect.execute(self.query)
        list_row = []
        for row in self.cusror:
            list_row.append(list(row))
        return list_row

    def Get_BSGD(self, msv=''):
        self.query = "SELECT * FROM RFID WHERE Name = '{}' AND Status = '0' ORDER BY DATETIME DESC".format(str(msv))
        self.cusror = self.connect.execute(self.query)
        list_row = []
        for row in self.cusror:
            list_row.append(list(row))
        return list_row[0][0]

    def Close_DB(self):
        self.connect.close()

# db = Database()

# print(db.Get_BSGD('10119609'))

# print(db.Search_TT('10119609'))
# [['Nguyễn Quốc Đạt', '10119609', 'Công nghệ thông tin', '101193']]

# rfid = "73 24 F8 03"
# bsx = "89F145240"
# db.Insert_Or_Update_DB("180407", '89F145240', "1", str(datetime.datetime.now()))
# # # ID, Plate, Status,Datetime = db.Get_Data_DB(180403
# id, bsx, status, thoigian = db.Get_Data_DB('73 24 F8 03')
# # dt_str1 = "2022-11-17 18:42:36.846585"
# # dt1 = datetime.datetime.strptime(dt_str1, '%Y-%m-%d %H:%M:%S.%f')
# time_convert = datetime.datetime.now()
# path_save = "History/"+rfid.replace(" ", "")+"_"+bsx+"_"+ str(time_convert.year) + str(time_convert.month) + str(time_convert.day) + str(time_convert.hour) + str(time_convert.minute) + ".jpg"
# # if dt1 > dt2:
# #     print('dung')
# # else:
# #     print('sai')
# # print(id)
# # print(bsx)
# # print(status)
# print(path_save)
# data = db.Get_Data_TB()
# print(data)
# db.Close_DB()


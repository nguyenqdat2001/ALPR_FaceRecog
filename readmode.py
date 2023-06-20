import pickle


with open(r'G:\Study\NCKH2021_2022_NhanDienBSX_Face_Recg\DA3_2021_NhanDienBSX\Models\facemodel.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)
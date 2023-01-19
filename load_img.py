import glob
import numpy as np
import cv2
import pandas as pd

def load_face(path):
    img =  cv2.imread(path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_name_form_path(path):
    arr = path.split('\\')[-1]
    arr = arr.split('_')[-1]
    name = arr.split('.')[0]
    return name

class load_img:
    def __init__(self):
        pass
    W, H = 160, 160
    
    def load_im(self, path):
        X = []  # Lưu ma trận ảnh
        Y = []  # Lưu nhãn tên
        df = pd.DataFrame(columns=['Name', 'Quantity']) # Lưu tên và số lượng 
        # File chứa thư mục ảnh
        #path = 'D:\\Study\\AI\\Project\\Detection_Ai\\image_training\\'
        # list_link chứa link các thư mục ảnh
        list_link = glob.glob(path + "*")
        name =''
        for link in list_link:
            for filename in glob.glob( link + '\\' + '*.jpg'): 
                img = load_face(filename)
                img = cv2.resize(img,(self.W, self.H))
                #img = preprocessing_image(img)
                X.append(img.reshape(self.W * self.H))
                name = get_name_form_path(link)
                Y.append(name)
                if not(name in np.array(df['Name'])):
                    df.loc[df.shape[0]] = [name, 1]
                else:
                    i = 0
                    while df['Name'][i] != name:
                        i+=1
                    a = df.iloc[i][1]
                    a += 1
                    df.loc[i] = [name, a]
        return np.array(X), np.array(Y), df

#ld = load_img()
#X, Y, df = ld.load_im('D:\\Study\\AI\\Project\\Detection_Ai\\image_training\\')
#print(df)
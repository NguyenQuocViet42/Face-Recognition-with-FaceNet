import glob
import cv2
import os
import cv2
from facenet_pytorch import MTCNN
import torch

def count_face():
    list_link = glob.glob(os.path.join('D:\\Study\\AI\\Project\\PJ1\\face', "*"))
    for link in list_link:
        filename = glob.glob(link + '\\' + '*.jpg')
        if len(filename) != 10:
            print(link)

def get_face_mtcnn():
    device =  torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print("Starting: ", device)
    mtcnn = MTCNN(margin = 20, keep_all=False, select_largest = True, post_process=False, device = device)
    count = 0
    list_link = glob.glob(os.path.join('D:\\Study\\AI\\Project\\PJ1\\pre_train', "*"))
    for link in list_link:
        name = link.split('\\')[-1]
        path = 'D:\\Study\\AI\\Project\\PJ1\\new_face\\' + str(name)
        print(name)
        try:
            os.mkdir(path)
        except:
            pass
        for filename in glob.glob(link + '\\' + '*.jpg'): 
            try:
                frame = cv2.imread(filename)
                os.chdir(path)
                name = filename.split('\\')[-1]
                face_img = mtcnn(frame, save_path = name)
                #img = cv2.resize(src=img, dsize=(160, 160)) 
                # Lưu ảnh
            except Exception as e:
                print(e)
        count += 1
        if count > 200:
            break
            
get_face_mtcnn()
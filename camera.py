import cv2
import pandas as pd
import numpy as np
import os
import glob
from facenet_pytorch import MTCNN
import torch
import time
RUN = True
def save(file_name, img, path):
        # Set vị trí lưu ảnh
        os.chdir(path)
        # Lưu ảnh
        cv2.imwrite(file_name, img)

def get_loc(event,x,y,flags,param): 
    if(event == cv2.EVENT_LBUTTONDOWN):  
        print(param)

class camera:
    def __init__(self):
        pass
    # Công cụ lưu ảnh
    path_im_training = 'D:\Study\AI\Project\Detection_Ai\Modul\image_training'
    
    def add_face(self, name, ld):
        # Thiết lập Camera
        cascPath = "D:\\Study\\AI\\Project\\Detection_Ai\\Modul\\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        video_capture = cv2.VideoCapture(1)
        
        # X lưu ảnh, Y lưu nhãn(Tên)
        X = []
        Y = []
        
        # Tạo mới thư mục
        new_path = 'D:\\Study\\AI\\Project\\Detection_Ai\\image_training\\' + name
        try:
            os.mkdir(new_path)
        except:
            pass
        A= glob.glob( new_path + '\\' + '*.png')
        # Biến đếm số ảnh
        im_connt = len(A)
        
        # Set kích thước ảnh
        W, H = 200,200
        RUN = True
        while RUN:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            new_face = []
            new_frame = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Vẽ một hình chữ nhật quanh khuôn mặt
            for (x, y, w, h) in faces:
                font = cv2.FONT_HERSHEY_SIMPLEX
                # Put Text
                #cv2.putText(frame,'Nguyen Quoc Viet',(x,y-10), font, 1,(239, 50, 239),2,cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                new_face = gray[y:y+h, x:x+w]
                new_face = cv2.resize(src=new_face, dsize=(W, H))
            # Hiển thị Video
            try:
                if cv2.getWindowProperty('frame',1) == -1 :
                    break
            except:
                pass
            # Sự kiện tắt cửa sổ
            cv2.imshow('frame', frame)
            # Lưu lại ảnh
            if cv2.waitKey(1) & 0xFF == ord('s'):
                try:
                    file_name = str(im_connt) + '_' + name + '.png'
                    save(file_name, new_face, new_path)
                    im_connt +=1
                    print("saved")
                    #X.append(new_face.reshape(W*H))
                    #Y.append(name)
                except:
                    print("Error")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        # Sau khi thực hiện thành công thì giải phóng ảnh
        video_capture.release()
        cv2.destroyAllWindows()
        X, Y, Z = ld.load_im('D:\\Study\\AI\\Project\\Detection_Ai\\image_training\\')
        return X, Y, Z

    def detect_face(self, predicter):
        cascPath = "D:\\Study\\AI\\Project\\Detection_Ai\\Modul\\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        # Đặt nguồn video thành webcam mặc định mà OpenCV có thể dễ dàng chụp.
        video_capture = cv2.VideoCapture(0)
        # Ở đây, chúng ta quay video. Hàm read() đọc một khung hình từ nguồn video, trong ví dụ này là webcam. Điều này sẽ trả về:
        # 1.Đọc khung video thực tế (một khung trên mỗi lần lặp)
        # 2.Một mã trả lại
        RUN = True
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            # Set kích thước ảnh
            W, H = 200, 200
            
            # Vẽ một hình chữ nhật quanh khuôn mặt
            for (x, y, w, h) in faces:
                try:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    # Put Text
                    new_face = gray[y:y+h, x:x+w]
                    new_face = cv2.resize(src=new_face, dsize=(200, 200))
                    id = predicter(new_face)
                    cv2.putText(frame,str(id),(x,y-10), font, 1,(239, 50, 239),2,cv2.LINE_AA)
                    #cv2.putText(frame,str(accuracy),(x,y-30), font, 1,(239, 50, 239),2,cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                except Exception as e:
                    print(e)
                #cv2.imshow('face', frame[y:y+h, x:x+w])

            # Hiển thị khung kết quả
            cv2.imshow('Predict', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        # Sau khi thực hiện thành công thì giải phóng ảnh
        video_capture.release()
        cv2.destroyAllWindows()
        
    def detect_face_mtcnn(self, predicter):
        device =  torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print(device)
        prev_frame_time = 0
        new_frame_time = 0
        mtcnn = MTCNN(margin = 20, keep_all=False, select_largest = True, post_process=False, device = device)

        cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        while cap.isOpened():
            isSuccess, frame = cap.read()
            if isSuccess:
                boxes, _, points_list = mtcnn.detect(frame, landmarks=True)
                if boxes is not None:
                    for box in boxes:
                        bbox = list(map(int,box.tolist()))
                        try:
                            face = mtcnn(frame, "tmp.jpg")
                            face = cv2.imread("tmp.jpg", 0)
                            face = cv2.resize(src=face, dsize=(160, 160))
                            id, dis= predicter(face)
                            cv2.putText(frame,str(id),(bbox[0]+20,bbox[1]-10), cv2.FONT_HERSHEY_DUPLEX, 1,(239, 50, 239),2,cv2.LINE_AA)
                            if dis != None:
                                dis = round(dis,2)
                                cv2.putText(frame,str(dis),(bbox[0]+20,bbox[1]-40), cv2.FONT_HERSHEY_DUPLEX, 1,(239, 50, 239),2,cv2.LINE_AA)
                        except Exception as e:
                            print(e)
                        frame = cv2.rectangle(frame,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,0,255),6)              
                        # Bo comment phan duoi neu cac ban muon xem 5-points tren mat

                        # if(not isinstance(points_list, list)):
                        #     points_list= points_list.tolist()
                        # for usr in points_list:
                        #     for points in usr:
                        #         frame = cv2.circle(frame, (int(points[0]), int(points[1])), radius=0, color=(0,0,255), thickness=10)
            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = str(int(fps))
            #cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1)&0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
#my = camera()
#my.add_face('test')
import PCA
import SVM
import pickle as pk
from camera import camera
from sklearn.preprocessing import LabelEncoder

datafile = open('PJ1\\model\\PCA_Data.pkl','rb')
data = pk.load(datafile)
Y = data.Y
labelencoder = LabelEncoder()
Y_label = labelencoder.fit_transform(Y)

"""PCA.PCA()
X_train_pca = data.X_train_pca
Y_train = data.Y_train
X_test_pca = data.X_test_pca
Y_test = data.Y_test
svm = SVM.SVM(X_train_pca ,Y_train, X_test_pca, Y_test)"""

PCAfile = open('PJ1\\model\\PCA.pkl','rb')
pca = pk.load(PCAfile)
SVMfile = open('PJ1\\model\\SVM.sav','rb')
svm = pk.load(SVMfile)

def SVMpredict(img_test):
    img_test = img_test.reshape(160,160)
    img_test = img_test.reshape(1,-1)
    img_test = pca.transform(img_test)
    person_test = svm.predict(img_test)
    #score = svm.decision_function(img_test)
    return labelencoder.inverse_transform(person_test), None

my_camer = camera()
my_camer.detect_face_mtcnn(predicter = SVMpredict)
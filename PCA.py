import load_img
import numpy as np
from sklearn.decomposition import PCA as my_pca
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle as pk


# Split Data
def split_data(X, Y):
    split_index = list(range(0,X.shape[0], 20))
    X_test = X[split_index]
    Y_test = Y[split_index]

    # preprare training set by removing items in test set
    X_train = X.copy()
    Y_train =  Y.copy()
    for i in split_index[::-1]:
        X_train  = np.delete(X_train,i,axis = 0 )
        Y_train = np.delete(Y_train,i,axis = 0 )
    print('X_train: ', X_train.shape)
    print('Y_train: ', Y_train.shape)
    print('X_test: ', X_test.shape)
    print('Y_test: ', Y_test.shape)
    return X_train, Y_train, X_test, Y_test

def split_data_random(X, Y):
    X_train, X_test, Y_train ,Y_test = train_test_split(X, Y, test_size=0.15)
    print('X_train: ', X_train.shape)
    print('Y_train: ', Y_train.shape)
    print('X_test: ', X_test.shape)
    print('Y_test: ', Y_test.shape)
    return X_train, Y_train, X_test, Y_test


class PCA_Data():
    def __init__(self, X, Y, X_train, X_test ,X_train_pca, Y_train, X_test_pca, Y_test):
        self.X, self.Y = X, Y
        self.X_train, self.X_test = X_train, X_test
        self.X_train_pca, self.Y_train = X_train_pca, Y_train
        self.X_test_pca, self.Y_test = X_test_pca, Y_test

def PCA():
    # Load Image
    loader = load_img.load_img()
    X, Y, df = loader.load_im('PJ1\\Caltech_face\\')
    le = LabelEncoder()
    Y_label = le.fit_transform(Y)
    X_train, Y_train, X_test, Y_test = split_data(X, Y_label)
    print("Running PCA")
    print('X.shape = ', X.shape)
    print('Y.shape = ', Y.shape)
    # PCA
    pca = my_pca(svd_solver="randomized", n_components= 120, whiten=True)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    
    # Save data
    data = PCA_Data(X, Y, X_train, X_test ,X_train_pca, Y_train, X_test_pca, Y_test)
    pk.dump(data, open("PJ1\\model\\PCA_Data.pkl","wb"))
    
    # Save model
    pk.dump(pca, open("PJ1\\model\\PCA.pkl","wb"))  # Save PCA model
    
    print('X_train_pca: ', X_train_pca.shape)
    print('X_test_pca: ', X_test_pca.shape)
    print("DONE !!")
    print('---------------------------------------')
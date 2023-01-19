from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import pickle as pk



def SVM(X_train_pca, Y_train, X_test_pca, Y_test):
    print("Running SVM")
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],  
                'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], 
                'kernel': ['rbf']} 
    svm = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'),
                    param_grid, cv=5, refit = True)
    svm = svm.fit(X_train_pca, Y_train)
    pk.dump(svm, open('PJ1\\model\\SVM.sav', 'wb'))
    print("Best estimator found by grid search:")
    print(svm.best_estimator_)
    
    Y_predict = svm.predict(X_test_pca)
    
    count = 0
    for i in range(len(Y_test)):
        if Y_test[i] == Y_predict[i]:
            count += 1
    print('Result:' , round((count/len(Y_test)) * 100, 2), '%')
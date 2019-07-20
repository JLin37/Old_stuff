import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')	
from sklearn.externals import joblib
from utils.classifications_utils import *
from utils.data_processing_utils import *
from utils.data_visualization_utils import *
from utils.metrics_utils import *
from utils.grid_search_utils import *
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, AdaBoostClassifier
from sklearn.preprocessing import MinMaxScaler

import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
FOLDER_PATH = "pickled_models/"
df_acc = pd.read_csv("acc_transformed_1_min.csv", index_col=0)
X_acc = df_acc.iloc[:, :-1]
y_acc = df_acc["label"]
print("Accelerometer: " + str(df_acc.shape[0]))

df_sta = pd.read_csv("sta_transformed_1_min.csv", index_col=0)
X_sta = df_sta.iloc[:, :-1]
y_sta = df_sta["label"]
print("Stabilizer: " + str(df_sta.shape[0]))

df_gyro = pd.read_csv("gyro_transformed_1_min.csv", index_col=0)
X_gyro = df_gyro.iloc[:, :-1]
y_gyro = df_gyro["label"]
print("Accelerometer: " + str(df_gyro.shape[0]))

X_gyro_acc = pd.concat([X_gyro, X_acc], axis=1)
y_gyro_acc = y_gyro

X_train, X_test, y_train, y_test = train_test_split(X_gyro_acc, y_gyro_acc, test_size=0.2, random_state=42)

Cs = [12, 15]
gammas = [1, 3, 5]
param_grid = {'C': Cs, 'gamma' : gammas}
clf = SVC(kernel='rbf')

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

best_model_svm = model_selection(clf, param_grid, X_train, y_train)

joblib.dump(best_model_svm, FOLDER_PATH + 'svm_gyro_acc.pkl')

X_gyro_sta = pd.concat([X_gyro, X_sta], axis=1)
y_gyro_sta = y_gyro


X_train, X_test, y_train, y_test = train_test_split(X_gyro_sta, y_gyro_sta, test_size=0.2, random_state=42)

Cs = [3, 10]
gammas = [0.1, 1]
param_grid = {'C': Cs, 'gamma' : gammas}
clf = SVC(kernel='rbf')

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

best_model_svm = model_selection(clf, param_grid, X_train, y_train)

joblib.dump(best_model_svm, FOLDER_PATH + 'svm_gyro_stb.pkl')

X_acc_sta = pd.concat([X_acc, X_sta], axis=1)
y_acc_sta = y_gyro

X_train, X_test, y_train, y_test = train_test_split(X_acc_sta, y_acc_sta, test_size=0.2, random_state=42)

Cs = [3, 10]
gammas = [0.1, 1]
param_grid = {'C': Cs, 'gamma' : gammas}
clf = SVC(kernel='rbf')

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

best_model_svm = model_selection(clf, param_grid, X_train, y_train)

joblib.dump(best_model_svm, FOLDER_PATH + 'svm_acc_stb.pkl')

X_all = pd.concat([X_gyro, X_acc, X_sta], axis=1)
y_all = y_gyro

X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=0.2, random_state=42)

Cs = [3, 10]
gammas = [0.1, 1]
param_grid = {'C': Cs, 'gamma' : gammas}
clf = SVC(kernel='rbf')

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

best_model_svm = model_selection(clf, param_grid, X_train, y_train)

joblib.dump(best_model_svm, FOLDER_PATH + 'svm_all.pkl')
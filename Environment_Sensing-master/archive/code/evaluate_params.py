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

no_wind_data = load_data(0, 3)
no_wind_data = separate_data_based_on_apparatus(no_wind_data)

level_1_wind = load_data(1, 3)
level_1_wind = separate_data_based_on_apparatus(level_1_wind)

level_3_wind = load_data(3, 3)
level_3_wind = separate_data_based_on_apparatus(level_3_wind)

level_6_wind = load_data(6, 3)
level_6_wind = separate_data_based_on_apparatus(level_6_wind)

level_8_wind = load_data(8, 3)
level_8_wind = separate_data_based_on_apparatus(level_8_wind)

no_wind_transformed = transformed_all_data(no_wind_data, 0)
level_1_wind_transformed = transformed_all_data(level_1_wind, 1)
level_3_wind_transformed = transformed_all_data(level_3_wind, 2)
level_6_wind_transformed = transformed_all_data(level_6_wind, 3)
level_8_wind_transformed = transformed_all_data(level_8_wind, 4)

acc_no_wind, gyro_no_wind, mag_no_wind, stabilizer_no_wind = tuple(no_wind_transformed)
acc_level_1_wind, gyro_level_1_wind, mag_level_1_wind, stabilizer_level_1_wind = tuple(level_1_wind_transformed)
acc_level_3_wind, gyro_level_3_wind, mag_level_3_wind, stabilizer_level_3_wind = tuple(level_3_wind_transformed)
acc_level_6_wind, gyro_level_6_wind, mag_level_6_wind, stabilizer_level_6_wind = tuple(level_6_wind_transformed)
acc_level_8_wind, gyro_level_8_wind, mag_level_8_wind, stabilizer_level_8_wind = tuple(level_8_wind_transformed)

def plot_params_accuracy_rf(X_train, y_train, label):
	param_grid = {
	"n_estimators": np.arange(50, 350, 50),
	"max_depth": np.arange(1, 28, 2),
	"max_features": np.arange(0.1, 1, 0.1),
	"min_samples_split": [2],
	"min_samples_leaf": [1],
	"max_leaf_nodes": np.arange(100, 1000, 200),
	"min_weight_fraction_leaf": [0]
			}

	clf = RandomForestClassifier(random_state=0)

	index = 1
	plt.figure(figsize=(24,16))

	for param, param_values in dict.items(param_grid):
		evaluate_param(clf, param, param_values, index, X_train, y_train)
		index += 1

	plt.savefig("graphs/rf_params/"+label+".png")

def plot_params_accuracy_et(X_train, y_train, label):
	param_grid = {
	"n_estimators": np.arange(50, 350, 50),
	"max_depth": np.arange(1, 28, 2),
	"max_features": np.arange(0.1, 1, 0.1),
	"min_samples_split": [2],
	"min_samples_leaf": [1],
	"max_leaf_nodes": np.arange(100, 1000, 200),
	"min_weight_fraction_leaf": [0]
			}

	clf = ExtraTreesClassifier(random_state=0)
	index = 1
	plt.figure(figsize=(24,16))

	for param, param_values in dict.items(param_grid):
		evaluate_param(clf, param, param_values, index, X_train, y_train)
		index += 1

	plt.savefig("graphs/et_params/"+label+".png")

def plot_params_accuracy_adaBoost(X_train, y_train, label):
	param_grid = {
	"n_estimators": np.arange(100, 500, 100),
	"learning_rate": [0.001, 0.01, 0.1, 1]
		}

	clf = AdaBoostClassifier(random_state=0)

	index = 1
	plt.figure(figsize=(24,16))

	for param, param_values in dict.items(param_grid):
		evaluate_param(clf, param, param_values, index, X_train, y_train)
		index += 1

	plt.savefig("graphs/adaBoost_params/"+label+".png")

def plot_params_accuracy_SVM(X_train, y_train, label):
	Cs = [10, 12, 15]
	gammas = [1, 3, 5]
	param_grid = {'C': Cs, 'gamma' : gammas}
	clf = SVC(kernel='rbf')

	scaler = MinMaxScaler()
	X_train = scaler.fit_transform(X_train)

	index = 1
	plt.figure(figsize=(24,16))

	for param, param_values in dict.items(param_grid):
		evaluate_param(clf, param, param_values, index, X_train, y_train)
		index += 1

	plt.savefig("graphs/svm_params/"+label+".png")

def main():
	# Accelerometer
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

	# df_sta = stabilizer_no_wind.append(stabilizer_level_1_wind, ignore_index=True)
	# df_sta = df_sta.append(stabilizer_level_3_wind, ignore_index=True)
	# df_sta = df_sta.append(stabilizer_level_6_wind, ignore_index=True)
	# df_sta = df_sta.append(stabilizer_level_8_wind, ignore_index=True)
	# X_sta = df_sta.iloc[:, :-1]
	# y_sta = df_sta["label"]
	# print("Stabilizer: " + str(df_sta.shape[0]))
	# df_sta.to_csv("sta_transformed_1_min.csv")

	# df_gyro = gyro_no_wind.append(gyro_level_1_wind, ignore_index=True)
	# df_gyro = df_gyro.append(gyro_level_3_wind, ignore_index=True)
	# df_gyro = df_gyro.append(gyro_level_6_wind, ignore_index=True)
	# df_gyro = df_gyro.append(gyro_level_8_wind, ignore_index=True)
	# X_gyro = df_gyro.iloc[:, :-1]
	# y_gyro = df_gyro["label"]
	# print("Gyro: " + str(df_gyro.shape[0]))
	# df_gyro.to_csv("gyro_transformed_1_min.csv")

	X_train_acc, X_test_acc, y_train_acc, y_test_acc = train_test_split(X_acc, y_acc, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_acc, y_train_acc, "Accelerometer")
	# plot_params_accuracy_et(X_train_acc, y_train_acc, "Accelerometer")
	# plot_params_accuracy_adaBoost(X_train_acc, y_train_acc, "Accelerometer")

	# # Stabilizer
	X_train_sta, X_test_sta, y_train_sta, y_test_sta = train_test_split(X_sta, y_sta, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_sta, y_train_sta, "Stabilizer")
	# plot_params_accuracy_et(X_train_sta, y_train_sta, "Stabilizer")
	# plot_params_accuracy_adaBoost(X_train_sta, y_train_sta, "Stabilizer")

	# # Gyro
	X_train_gyro, X_test_gyro, y_train_gyro, y_test_gyro = train_test_split(X_gyro, y_gyro, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_gyro, y_train_gyro, "Gyro")
	# plot_params_accuracy_et(X_train_gyro, y_train_gyro, "Gyro")
	# plot_params_accuracy_adaBoost(X_train_gyro, y_train_gyro, "Gyro")

	# Gyro + Accelerometer
	# X_gyro_acc = pd.concat([X_gyro, X_acc], axis=1)
	# y_gyro_acc = y_gyro
	# X_train_gyro_acc, X_test_gyro_acc, y_train_gyro_acc, y_test_gyro_acc = train_test_split(X_gyro_acc, y_gyro_acc, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_gyro_acc, y_train_gyro_acc, "Gyro + Accelerometer")
	# plot_params_accuracy_et(X_train_gyro_acc, y_train_gyro_acc, "Gyro + Accelerometer")
	# plot_params_accuracy_adaBoost(X_train_gyro_acc, y_train_gyro_acc, "Gyro + Accelerometer")


	# Gyro + Stabilizer
	# X_gyro_sta = pd.concat([X_gyro, X_sta], axis=1)
	# y_gyro_sta = y_gyro
	# X_train_gyro_sta, X_test_gyro_sta, y_train_gyro_sta, y_test_gyro_sta = train_test_split(X_gyro_sta, y_gyro_sta, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_gyro_sta, y_train_gyro_sta, "Gyro + Stabilizer")
	# plot_params_accuracy_et(X_train_gyro_sta, y_train_gyro_sta, "Gyro + Stabilizer")
	# plot_params_accuracy_adaBoost(X_train_gyro_sta, y_train_gyro_sta, "Gyro + Stabilizer")

	# Accelerometer + Stabilizer
	# X_acc_sta = pd.concat([X_acc, X_sta], axis=1)
	# y_acc_sta = y_gyro
	# X_train_acc_sta, X_test_acc_sta, y_train_acc_sta, y_test_acc_sta = train_test_split(X_acc_sta, y_acc_sta, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_acc_sta, y_train_acc_sta, "Accelerometer + Stabilizer")
	# plot_params_accuracy_et(X_train_acc_sta, y_train_acc_sta, "Accelerometer + Stabilizer")
	# plot_params_accuracy_adaBoost(X_train_acc_sta, y_train_acc_sta, "Accelerometer + Stabilizer")

	# All
	# X_all = pd.concat([X_gyro, X_acc, X_sta], axis=1)
	# y_all = y_gyro
	# X_train_all, X_test_all, y_train_all, y_test_all = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
	# plot_params_accuracy_rf(X_train_all, y_train_all, "All")
	# plot_params_accuracy_et(X_train_all, y_train_all, "All")
	# plot_params_accuracy_adaBoost(X_train_all, y_train_all, "All")

	plot_params_accuracy_SVM(X_train_acc, y_train_acc, "Accelerometer")
	plot_params_accuracy_SVM(X_train_sta, y_train_sta, "Stabilizer")
	plot_params_accuracy_SVM(X_train_gyro, y_train_gyro, "Gyro")
	# plot_params_accuracy_SVM(X_train_gyro_acc, y_train_gyro_acc, "Gyro + Accelerometer")
	# plot_params_accuracy_SVM(X_train_gyro_sta, y_train_gyro_sta, "Gyro + Stabilizer")
	# plot_params_accuracy_SVM(X_train_acc_sta, y_train_acc_sta, "Accelerometer + Stabilizer")
	# plot_params_accuracy_SVM(X_train_all, y_train_all, "All")

if __name__ == '__main__':
	main()
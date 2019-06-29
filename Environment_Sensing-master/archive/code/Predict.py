import pandas as pd
import numpy as np
from Utils import *
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

def predict(clf, X, y):
	train_acc = []
	test_acc = []
	auc_score = []
	sensitivity = []
	specificity = []
	f1_score = []
	positive_predictive_value = []
	negative_predictive_value = []

	X, y = np.array(X), np.array(y)

	kf = KFold(n_splits=10, shuffle=True, random_state=0)

	for train_index, test_index in kf.split(X):
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]

		clf.fit(X_train, y_train)
		y_pred = clf.predict(X_test)
		tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
		sen, spc, f1s, ppr, npr = compute_performance_measures(tn, fp, fn, tp)

		train_acc.append(clf.score(X_train, y_train))
		test_acc.append(clf.score(X_test, y_test))
		auc_score.append(roc_auc_score(y_test, y_pred))
		sensitivity.append(sen)
		specificity.append(spc)
		f1_score.append(f1s)
		positive_predictive_value.append(ppr)
		negative_predictive_value.append(npr)

	scores = list([train_acc, test_acc, auc_score, sensitivity, 
		specificity, f1_score, positive_predictive_value, 
		negative_predictive_value])
	return compute_mean_scores(scores)

def predict_all(no_wind_data, level_1_wind_data, classifiers):   
	apparatuses = ["stabilizer", "gyro", "acc", "mag"]
	clf_names = ["Extra Trees", "Random Forests", "Ada Boost"]
	columns = ["Apparatus", "Classifier", "Train Accuracy", "Test Accuracy", 
	"AUC Score", "Sensitivity", "Specificity", "F1-Score", "PPR", "NPR"]
	summary = pd.DataFrame(data=[], columns=columns)
	
	for (apparatus, no_wind, level_1_wind) in zip(apparatuses, no_wind_data, level_1_wind_data):
		no_wind_transformed = transform_data(no_wind, 0)
		level_1_wind_transformed = transform_data(level_1_wind, 1)
		df = no_wind_transformed.append(level_1_wind_transformed, ignore_index=True)

		X = df.iloc[:, :-1]
		y = df["label"]

		for clf, clf_name in zip(classifiers, clf_names):
			row = predict(clf, X, y)
			row.insert(0, clf_name)
			row.insert(0, apparatus)
			summary = summary.append(pd.Series(row, index=columns), ignore_index=True)

	return summary
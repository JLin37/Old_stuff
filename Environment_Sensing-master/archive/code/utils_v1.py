import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.utils import safe_indexing
import matplotlib.patches as mpatches

PATH = "data/"
JASON= "Jason/"
LABEL_0_NO_WIND = "label_0_no_wind/"
LABEL_1_SETTING_1 = "label_1_setting_1/"
LABEL_2_SETTING_2 = "label_2_setting_2/"
LABEL_3_SETTING_3 = "label_3_setting_3/"
FILE_PREFIX = "data_set_label_"
FILE_MIDDLE = "_packet_"
FILE_SUFFIX = ".csv"

sliding_window = 1

def load_data(label, total_files, person="Suwen"):
	if person is "Jason":
		path = PATH + JASON
	else:
		path = PATH

	if label == 0:
		path += LABEL_0_NO_WIND
	elif label == 1:
		path += LABEL_1_SETTING_1
	elif label == 2:
		path += LABEL_2_SETTING_2
	elif label == 3:
		path += LABEL_3_SETTING_3

	data = pd.DataFrame(data=[], columns=["timestamp_start", "timestamp_end", "stabilizer.roll", "stabilizer.pitch", "stabilizer.yaw", "gyro.x", "gyro.y", "gyro.z", "acc.x", "acc.y", "acc.z", "mag.x", "mag.y", "mag.z","label"])
	
	for i in range(total_files):
		fileName = FILE_PREFIX+str(label)+FILE_MIDDLE+str(i)+FILE_SUFFIX
		temp_file = pd.read_csv(path+fileName, index_col=0)
		data = data.append(temp_file)

	return data

def separate_data_based_on_apparatus(data):
	acc = data.iloc[:, 2:5]
	gyro = data.iloc[:, 5:8]
	mag = data.iloc[:, 8:11]
	stabilizer = data.iloc[:, 11:14]

	return acc, gyro, mag, stabilizer

def compute_mean_scores(scores):
	train_acc = np.array(scores[0]).mean()
	test_acc = np.array(scores[1]).mean()
	auc_score = np.array(scores[2]).mean()
	spec = np.array(scores[3]).mean()
	sens = np.array(scores[4]).mean()
	f1_score = np.array(scores[5]).mean()
	ppr = np.array(scores[6]).mean()
	npr = np.array(scores[7]).mean()

	results = [train_acc, test_acc, auc_score, sens, spec, f1_score, ppr, npr]
	return results

def compute_performance_measures(tn, fp, fn, tp):
    with np.errstate(divide='ignore'):
        sen = 0 if tp+fn == 0 else (1.0*tp)/(tp+fn)
    
    with np.errstate(divide='ignore'):
        spc = 0 if tn+fp == 0 else (1.0*tn)/(tn+fp)
    
    with np.errstate(divide='ignore'):
        f1s = 0 if (2.0*tp+fn+fp)==0 else (2.0*tp)/(2.0*tp+fn+fp)
        
    with np.errstate(divide='ignore'):
        ppr = 0 if (tp+fp)==0 else (1.0*tp)/(tp+fp)
    
    with np.errstate(divide='ignore'):
        npr = 0 if (tn+fn)==0 else (1.0*tn)/(tn+fn)
    
    with np.errstate(divide='ignore'):
        acc = 0 if tp+fp+tn+fn==0 else (tp+tn)/(tp+fp+tn+fn)
        
    with np.errstate(invalid='ignore'):
        didx = math.log(1+acc, 2)+math.log(1+(sen+spc)/2, 2)
        
    return (sen, spc, f1s, ppr, npr)

def pca(X):
    X = np.array(X)
    pca = PCA()
    
    return pca.fit_transform(X)

def plot_data_2D(X, y, apparatus):
	X = pca(X)   
	y = np.array(y)

	no_wind = np.flatnonzero(y == 0)
	level_1_wind = np.flatnonzero(y == 1) 
	indices = [no_wind, level_1_wind]

	fig = plt.figure()   

	for i, c in zip(indices, ['b', 'r']):
		data = safe_indexing(X, i)
		xs = data[:, 0]
		ys = data[:, 1]
		plt.scatter(xs, ys, color=c)  

	plt.xlabel("$PC^{1st}$")  
	plt.ylabel("$PC^{2nd}$")   

	plt.title(apparatus)

	no_wind = mpatches.Patch(color='blue', label="No wind")
	level_1_wind = mpatches.Patch(color='red', label="level_1_wind")
	plt.legend(handles=[level_1_wind, no_wind])

	plt.show()

def plot_data_3D(X, y, apparatus):
    X = pca(X)   
    y = np.array(y)

    no_wind = np.flatnonzero(y == 0)
    level_1_wind = np.flatnonzero(y == 1) 
    indices = [no_wind, level_1_wind]
    
    fig = plt.figure()  
    ax = Axes3D(fig) 
    
    for i, c in zip(indices, ['b', 'r']):
        data = safe_indexing(X, i)
        xs = data[:, 0]
        ys = data[:, 1]
        zs = data[:, 2]
        ax.scatter(xs, ys, zs, color=c)  

    ax.set_xlabel("$PC^{1st}$")  
    ax.set_ylabel("$PC^{2nd}$")  
    ax.set_zlabel("$PC^{3rd}$")  
    
    plt.title(apparatus)
    
    level_1_wind = mpatches.Patch(color='blue', label='level_1_wind')
    no_wind = mpatches.Patch(color='red', label='no_wind')
    plt.legend(handles=[level_1_wind, no_wind])
    
    plt.show()
        
    plt.close()

def set_sliding_window(window_length):
	global sliding_window
	sliding_window = window_length

def get_avg_resultant_acc(vals):
    pwd = np.power(vals, 2)
    sum_xyz = np.sum(pwd, 1)
    sqrt_xyz = np.sqrt(sum_xyz)
    sum_resultant_acc = np.sum(sqrt_xyz)
    avg_resultant_acc = sum_resultant_acc/100

    return avg_resultant_acc

def get_binned_distribution_for_one_axis(vals):
    vals = np.array(vals)
    bins = []
    max_value = np.max(vals)
    min_value = np.min(vals)
    diff = max_value - min_value
    bin_size = diff/10
    
    for i in range(10):
        lower_bound = min_value + i*bin_size if i is not 0 else min_value - 1
        upper_bound = min_value + (i+1)*bin_size if (i+1) is not 10 else max_value
        bins.append(((lower_bound < vals) & (vals <= upper_bound)).sum())

    return np.array(bins)

def get_binned_distribution(data):
    results = []
    for axis in data:
        result = get_binned_distribution_for_one_axis(data[axis])
        assert (result.sum() == data.shape[0])
        results.append(result)

    return results

def construct_row(data):
	features = np.array([])

	mu = data.mean()
	features = np.hstack((features, np.array(mu)))

	std = data.std()
	features = np.hstack((features, np.array(std)))

	avg_resultant_acc = get_avg_resultant_acc(data)
	features = np.append(features, avg_resultant_acc)

	binned_distribution = get_binned_distribution(data)

	features = np.hstack((features, np.array(binned_distribution[0])))
	features = np.hstack((features, np.array(binned_distribution[1])))
	features = np.hstack((features, np.array(binned_distribution[2])))

	#mean absoutle difference
	mad = data.mad()
	features = np.hstack((features, np.array(mad)))

	return features

def make_columns():
    columns = []
    types = ["mu", "std", "avg_resultant_acc", "bin", "mean_average_difference"]
    for t in types:
        if t is "bin":
            for i in range(30):
                columns.append("bins_"+str(i))
        elif t is "avg_resultant_acc":
            columns.append("avg_resultant_acc")
        else:
            for axis in ["x", "y", "z"]:
                columns.append(t+"_"+axis)
    return columns

def transform_data(data, label):
    rows, _ = data.shape
    columns = make_columns()
    df = pd.DataFrame(data=[], columns=columns)
    #rows needed to calculate one sliding window amount of data
    #1s = 1000(ms); each row of data corresponds to 10(ms)
    rows_needed = int(sliding_window * 1000 / 10)

    if rows_needed > rows:
        print('Not enough data.')
        return None

    num_data_points = data.shape[0]
    remainder = num_data_points % rows_needed
    for k in range(num_data_points):
        if k + 100 <= num_data_points:
            rows = data.iloc[k:(100+k), :]
            transformed_features = construct_row(rows).reshape((1, 40))
            df = df.append(pd.DataFrame(transformed_features, columns=columns), ignore_index=True)
        else:
            break
            
    if remainder / 100 > 0.9:
        rows = data.iloc[-remainder:, : ]
        transformed_features = construct_row(rows).reshape((1, 40))
        df = df.append(pd.DataFrame(transformed_features, columns=columns), ignore_index=True)
        
    df["label"] = label

    return df

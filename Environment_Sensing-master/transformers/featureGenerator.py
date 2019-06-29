from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class FeatureGenerator(BaseEstimator, TransformerMixin):
	def __init__(self, sliding_window):
		self.sliding_window = sliding_window

	def get_avg_resultant_acc(self, vals):
		pwd = np.power(vals, 2)
		sum_xyz = np.sum(pwd, 1)
		sqrt_xyz = np.sqrt(sum_xyz)
		sum_resultant_acc = np.sum(sqrt_xyz)
		avg_resultant_acc = sum_resultant_acc/100

		return avg_resultant_acc

	def get_binned_distribution_for_one_axis(self, vals):
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

	def get_binned_distribution(self, data):
		results = []
		for axis in data:
			result = self.get_binned_distribution_for_one_axis(data[axis])
			assert (result.sum() == data.shape[0])
			results.append(result)

		return results

	def construct_row(self, data):
		features = np.array([])

		mu = data.mean()
		features = np.hstack((features, np.array(mu)))

		std = data.std()
		features = np.hstack((features, np.array(std)))

		avg_resultant_acc = self.get_avg_resultant_acc(data)
		features = np.append(features, avg_resultant_acc)

		binned_distribution = self.get_binned_distribution(data)

		features = np.hstack((features, np.array(binned_distribution[0])))
		features = np.hstack((features, np.array(binned_distribution[1])))
		features = np.hstack((features, np.array(binned_distribution[2])))

		#mean absoutle difference
		mad = data.mad()
		features = np.hstack((features, np.array(mad)))

		return features

	def make_columns(self, sensor):
		columns = []
		types = ["mu", "std", "avg_resultant_acc", "bin", "mean_average_difference"]
		for t in types:
			if t is "bin":
				for i in range(30):
					columns.append("bins_"+str(i)+"_"+sensor)
			elif t is "avg_resultant_acc":
				columns.append("avg_resultant_acc_"+sensor)
			else:
				for axis in ["x", "y", "z"]:
					columns.append(t+"_"+axis+"_"+sensor)
		return columns

	def generate_features(self, data, sensor):
		rows, _ = data.shape
		columns = self.make_columns(sensor)
		df = pd.DataFrame(data=[], columns=columns)

		rows_needed = int(self.sliding_window * 1000 / 10)
		if rows_needed > rows:
			print('Not enough data.')
			return None

		num_data_points = data.shape[0]
		remainder = num_data_points % rows_needed
		for k in range(num_data_points):
			if k + 100 <= num_data_points:
				rows = data.iloc[k:(100+k), :]
				transformed_features = self.construct_row(rows).reshape((1, 40))
				df = df.append(pd.DataFrame(transformed_features, columns=columns), ignore_index=True)
			else:
				break
		        
		if remainder / 100 > 0.9:
			rows = data.iloc[-remainder:, : ]
			transformed_features = self.construct_row(rows).reshape((1, 40))
			df = df.append(pd.DataFrame(transformed_features, columns=columns), ignore_index=True)
		    
		return df

	def transform(self, X, sensor):
		columns = self.make_columns(sensor)
		df = pd.DataFrame(data=[], columns=columns)
		#rows needed to calculate one sliding window amount of data
		#1s = 1000(ms); each row of data corresponds to 10(ms)

		for c in range(self.num_classes):
			df = df.append(self.generate_features(X.iloc[c*self.cut_off_number:(c+1)*self.cut_off_number, :], sensor), ignore_index = True)

		return df

	# we have to set the cut off number so that we know 
	# how many data points belong to each class
	def fit(self, X, num_classes):
		self.num_classes = num_classes
		self.cut_off_number = X.shape[0]//num_classes
		return self

	
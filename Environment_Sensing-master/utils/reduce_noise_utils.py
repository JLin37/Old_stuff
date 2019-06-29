import numpy as np
import pandas as pd
from scipy import signal

def reduce_noise_with_FFT(data, cut_off_points):
	columns = data.columns.values

	for c, cut_off in zip(columns, cut_off_points):
		data_fft = np.fft.fft(data[c])
		indices = data_fft > cut_off
		data_fft = data_fft*indices
		data_ifft = np.fft.ifft(data_fft)
		data[c] = data_ifft.real

	return data
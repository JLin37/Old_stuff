import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.utils import safe_indexing
import matplotlib.patches as mpatches
from scipy import signal

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
		plt.scatter(xs, ys, 12, color=c)  

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
        ax.scatter(xs, ys, zs, 8, color=c)  

    ax.set_xlabel("$PC^{1st}$")  
    ax.set_ylabel("$PC^{2nd}$")  
    ax.set_zlabel("$PC^{3rd}$")  
    
    plt.title(apparatus)
    
    level_1_wind = mpatches.Patch(color='blue', label='level_1_wind')
    no_wind = mpatches.Patch(color='red', label='no_wind')
    plt.legend(handles=[level_1_wind, no_wind])
    
    plt.show()

def plot_in_frequency_domain(data, wind_level, sensor):
    x = data[sensor+'.x']
    y = data[sensor+'.y']
    z = data[sensor+'.z']
    f = plt.figure(figsize=(15, 3))
    ax = f.add_subplot(131)
    ax2 = f.add_subplot(132)
    ax3 = f.add_subplot(133)
    
    x_fft = np.fft.fft(x)
    f_x = np.fft.fftfreq(x.shape[0])
    Pxx_den_x = (x_fft*np.conj(x_fft))/x_fft.shape[0]
    ax.set_title(sensor + ': X axis, ' + str(wind_level))
    ax.plot(f_x, Pxx_den_x)
    
    y_fft = np.fft.fft(y)
    f_y = np.fft.fftfreq(y.shape[0])
    Pxx_den_y = (y_fft*np.conj(y_fft))/y_fft.shape[0]
    ax2.set_title(sensor + ': Y axis, ' + str(wind_level))
    ax2.plot(f_y, Pxx_den_y)
    
    z_fft = np.fft.fft(z)
    f_z = np.fft.fftfreq(z.shape[0])
    Pxx_den_z = (z_fft*np.conj(z_fft))/z_fft.shape[0]
    ax3.set_title(sensor + ': Z axis, ' + str(wind_level))
    ax3.plot(f_z, Pxx_den_z)

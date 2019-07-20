import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.dates import strpdate2num
import numpy as np

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def graphRawFX():
    date,bid,ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
                              delimiter=',',
                              converters={0:bytespdate2num('%Y%m%d%H%M%S')})
    fig = plt.figure(figsize =(10,8))
    ax1 = plt.subplot2grid((40,40),(0,0), rowspan=40, colspan=40)

    ax1.plot(date,bid)
    ax1.plot(date,ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H: %M: %S'))
    for label in ax1.xaxis.get_ticklabels():
    	label.set_rotation(45)

    ax1_2 =ax1.twinx()
    ax1_2.fill_between(date, 0, (ask-bid), facecolor = 'g', alpha = .3)

    
    plt.grid(True)
    plt.show()

graphRawFX()

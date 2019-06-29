import pandas as pd
import numpy as np

def get_baseline_result(y):
    class_counts = []
    class_num = np.unique(y)

    for i in range(len(class_num)):
        class_counts.append(np.flatnonzero(y == i).shape[0])
        
    class_counts = np.array(class_counts)
    idx = np.argmax(class_counts)
    
    return class_counts[idx]/(class_counts.sum())
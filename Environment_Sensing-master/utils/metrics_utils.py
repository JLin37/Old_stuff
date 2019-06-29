import math
import pandas as pd
import numpy as np
from sklearn.utils import safe_indexing

def generate_confusion_matrix(counts, class_labels):
    for key, item in counts.items():
        if len(item) < len(class_labels):
            for i in range(len(class_labels) - len(item)):
                counts[key] = np.append(counts[key], 0)

    index = ["actual_" + str(c) for c in class_labels]

    confusion_matrix = pd.DataFrame(data=counts, index=index)
    return confusion_matrix.T

def get_confusion_matrix(y_pred, y_true):
    counts = {}
    class_labels = np.unique(y_true)
    
    for label in class_labels:
        idx = np.flatnonzero(y_pred == label)
        counts[str("predicted_")+str(label)] = np.bincount(safe_indexing(y_true, idx))
 
    confusion_matrix = generate_confusion_matrix(counts, class_labels)

    return confusion_matrix

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
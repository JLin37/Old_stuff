import pandas as pd
import numpy as np

PATH = "data/"
DRONE1 = "drone1/"
DRONE2 = "drone2/"
DRONE3 = "drone3/"
LABEL_0_NO_WIND = "label_0_no_wind/"
LABEL_1_SETTING_1 = "label_1_setting_1/"
LABEL_2_SETTING_2 = "label_2_setting_2/"
LABEL_3_SETTING_3 = "label_3_setting_3/"
LABEL_6_SETTING_6 = "label_6_setting_6/"
LABEL_8_SETTING_8 = "label_8_setting_8/"
FILE_PREFIX = "data_set_label_"
FILE_MIDDLE = "_packet_"
FILE_SUFFIX = ".csv"

sliding_window = 1

def load_data(label, total_files, person="drone1"):
    path = ""
    if person is "drone1":
        path = PATH + DRONE1
    elif person is "drone2":
        path = PATH + DRONE2
    elif person is "drone3":
        path = PATH + DRONE3
    else:
        path = PATH + DRONE1

    if label == 0:
        path += LABEL_0_NO_WIND
    elif label == 1:
        path += LABEL_1_SETTING_1
    elif label == 2:
        path += LABEL_2_SETTING_2
    elif label == 3:
        path += LABEL_3_SETTING_3
    elif label == 6:
        path += LABEL_6_SETTING_6
    elif label == 8:
        path += LABEL_8_SETTING_8

    columns = ["timestamp_start", "timestamp_end", "stabilizer.roll", "stabilizer.pitch", "stabilizer.yaw", "gyro.x", "gyro.y", "gyro.z", "acc.x", "acc.y", "acc.z", "mag.x", "mag.y", "mag.z","label"]
    data = pd.DataFrame(data=[], columns=columns)

    for i in range(total_files):
        fileName = FILE_PREFIX+str(label)+FILE_MIDDLE+str(i)+FILE_SUFFIX
        temp_data = pd.read_csv(path+fileName, index_col=0)
        temp_data["label"] = label
        # cut the first and last 200
        temp_data = temp_data.iloc[200:-200, :]
        # only need 6000 data points, which is equivalent to 1 min of data
        temp_data = temp_data.iloc[:6000, :]
        data = data.append(temp_data, ignore_index=True)

    return data

def separate_data_based_on_apparatus(data):
    acc = data.iloc[:, 0:3]
    gyro = data.iloc[:, 3:6]
    mag = data.iloc[:, 7:10]
    stabilizer = data.iloc[:, 10:13]

    data_collection = {
        "acc": acc,
        "gyro": gyro,
        "mag": mag,
        "stabilizer": stabilizer
    }

    return data_collection

# after performing feature transformation on the training data
# the amount of data points will decrease becasue of the usage of sliding windwo.
# as a result, we need to reduce the number of label for each class, accordingly.
def reduce_label_amount(labels, num_classes):
    rows = labels.shape[0]
    rows_needed = int(sliding_window * 1000 / 10)

    if rows_needed > rows:
        print('Not enough data.')
        return None

    # calculate how many rows for one class
    num_data_points = rows//num_classes
    remainder = num_data_points % rows_needed
    counter = 0
    for k in range(num_data_points):
        if k + 100 <= num_data_points:
            counter += 1
        else:
            break
            
    if remainder / 100 > 0.9:
        counter += 1
    
    print(counter)
    # generate new labels
    labels = []
    for c in range(num_classes):
        label = [c for x in range(counter)]
        labels.append(label)

    return np.array(labels).flatten()
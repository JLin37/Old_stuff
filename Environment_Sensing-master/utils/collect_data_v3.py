# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2016 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Simple example that connects to the crazyflie at `URI` and runs a figure 8
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

Change the URI variable to your Crazyflie configuration.
"""
import sys
import logging
import time
import pandas as pd
import numpy as np
from collections import OrderedDict
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.log import LogConfig
from cflib.positioning.motion_commander import MotionCommander
import warnings
warnings.filterwarnings("ignore")

URI = 'radio://0/80/2M'
#URI = 'radio://0/92/2M/E7E7E7E7E4'
#URI = 'radio://0/86/2M/E7E7E7E7E6'

df = pd.DataFrame(columns=['timestamp_start', 'timestamp_end', 
    'stabilizer.roll', 'stabilizer.pitch', 'stabilizer.yaw', 
            'gyro.x', 'gyro.y', 'gyro.z',
            'acc.x', 'acc.y', 'acc.z', 
            'mag.x', 'mag.y', 'mag.z','label'])
globalCounter = 0
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def write_to_file(data, class_label, packet_num):
    if len(data) % 2 is not 0:
        data = data[:len(data)- 1]

    temp_df = pd.DataFrame(data)
    m, _ = temp_df.shape
    even_rows = temp_df.iloc[np.arange(0, m, 2), :]
    odd_rows = temp_df.iloc[np.arange(1, m, 2), :]

    columns = ['timestamp_start', 'timestamp_end',
               'acc.x', 'acc.y', 'acc.z', 
               'gyro.x', 'gyro.y', 'gyro.z', 
               'mag.x', 'mag.y', 'mag.z', 
               'stabilizer.pitch', 'stabilizer.roll', 'stabilizer.yaw']

    df = pd.DataFrame(data=np.zeros((int(m/2), 14)), columns=columns)
    df[['gyro.x', 'gyro.y', 'gyro.z']] = np.array(even_rows[['gyro.x', 'gyro.y', 'gyro.z']])
    df[['stabilizer.pitch', 'stabilizer.roll', 'stabilizer.yaw']] = np.array(even_rows[['stabilizer.pitch', 'stabilizer.roll', 'stabilizer.yaw']])
    df[["acc.x", "acc.y", "acc.z"]] = np.array(odd_rows[["acc.x", "acc.y", "acc.z"]])
    df[["mag.x", "mag.y", "mag.z"]] = np.array(odd_rows[["mag.x", "mag.y", "mag.z"]])
    df['timestamp_start'] = np.array(even_rows.timestamp)
    df['timestamp_end'] = np.array(odd_rows.timestamp)
    
    df.to_csv(df.to_csv("data_set_label_"+class_label+"_packet_"+packet_num+".csv"))

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)

    cflib.crtp.init_drivers(enable_debug_driver=False)

    data = []
        
    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # logs data
        lg_1 = LogConfig(name='stabilizer_gyro', period_in_ms=10)
        lg_1.add_variable('stabilizer.roll', 'float')
        lg_1.add_variable('stabilizer.pitch', 'float')
        lg_1.add_variable('stabilizer.yaw', 'float')
        lg_1.add_variable('gyro.x', 'float')
        lg_1.add_variable('gyro.y', 'float')
        lg_1.add_variable('gyro.z', 'float')

        lg_2 = LogConfig(name='acc_mag', period_in_ms=10)
        lg_2.add_variable('acc.x', 'float')
        lg_2.add_variable('acc.y', 'float')
        lg_2.add_variable('acc.z', 'float')
        lg_2.add_variable('mag.x', 'float')
        lg_2.add_variable('mag.y', 'float')
        lg_2.add_variable('mag.z', 'float')

        switch = 0
        class_label = sys.argv[1]
        packet_num = sys.argv[2]
        
        with MotionCommander(scf, default_height=0.35) as mc:
            with SyncLogger(scf, lg_1) as logger1, SyncLogger(scf, lg_2) as logger2:
                # we collect data for 
                endTime = time.time() + 64
                while time.time() < endTime:
                    if switch == 0: 
                        logger = logger1
                    elif switch == 1:
                        logger = logger2

                    for log_entry in logger:
                        row = log_entry[1]
                        row["timestamp"] = log_entry[0]
                        data.append(row)
                        switch += 1
                        break

                    if switch == 2:
                        switch = 0 

        write_to_file(data, str(class_label), packet_num)
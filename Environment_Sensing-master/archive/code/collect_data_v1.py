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
import warnings
warnings.filterwarnings("ignore")

URI = 'radio://0/80/250K'
df = pd.DataFrame(columns=['timestamp_start', 'timestamp_end', 
    'stabilizer.roll', 'stabilizer.pitch', 'stabilizer.yaw', 
            'gyro.x', 'gyro.y', 'gyro.z',
            'acc.x', 'acc.y', 'acc.z', 
            'mag.x', 'mag.y', 'mag.z','label'])
globalCounter = 0
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def Logger(label, switch):
    global globalCounter, df
    timestamp = log_entry[0]
    data = log_entry[1]
    logconf_name = log_entry[2]
    # log data into a data frame
    if switch == 0 :
        data["timestamp_start"] = timestamp
        data["label"] = label
        current_data = pd.DataFrame(data, columns=['timestamp_start', 'timestamp_end', 
            'stabilizer.roll', 'stabilizer.pitch', 'stabilizer.yaw', 
            'gyro.x', 'gyro.y', 'gyro.z',
            'acc.x', 'acc.y', 'acc.z', 
            'mag.x', 'mag.y', 'mag.z', 
            'label'], index=[globalCounter])
        df = df.append(current_data, ignore_index=True)
    elif switch == 1:
        current_data = df.iloc[globalCounter, :]
        current_data["gyro.x"] = data["gyro.x"]
        current_data["gyro.y"] = data["gyro.y"]
        current_data["gyro.z"] = data["gyro.z"]
        df.iloc[globalCounter, :] = current_data
    elif switch == 2:
        current_data = df.iloc[globalCounter, :]
        current_data["acc.x"] = data["acc.x"]
        current_data["acc.y"] = data["acc.y"]
        current_data["acc.z"] = data["acc.z"]
        df.iloc[globalCounter, :] = current_data
    elif switch == 3:
        current_data = df.iloc[globalCounter, :]
        current_data["mag.x"] = data["mag.x"]
        current_data["mag.y"] = data["mag.y"]
        current_data["mag.z"] = data["mag.z"]
        current_data["timestamp_end"] = timestamp
        df.iloc[globalCounter, :] = current_data
        globalCounter += 1

    #print('[%d][%s]: %s' % (timestamp, logconf_name, data))

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)

    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)

        # logs data
        lg_stab = LogConfig(name='stabilizer', period_in_ms=10)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')

        lg_gyro = LogConfig(name='gyro', period_in_ms=10)
        lg_gyro.add_variable('gyro.x', 'float')
        lg_gyro.add_variable('gyro.y', 'float')
        lg_gyro.add_variable('gyro.z', 'float')

        lg_acc = LogConfig(name='acc', period_in_ms=10)
        lg_acc.add_variable('acc.x', 'float')
        lg_acc.add_variable('acc.y', 'float')
        lg_acc.add_variable('acc.z', 'float')

        lg_mag = LogConfig(name='mag', period_in_ms=10)
        lg_mag.add_variable('mag.x', 'float')
        lg_mag.add_variable('mag.y', 'float')
        lg_mag.add_variable('mag.z', 'float')

        switch = 0
        label = sys.argv[1]
        with SyncLogger(scf, lg_stab) as logger1, SyncLogger(scf, lg_gyro) as logger2, SyncLogger(scf, lg_acc) as logger3, SyncLogger(scf, lg_mag) as logger4:
            # takes off
            for y in range(10):
                cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
                time.sleep(0.1)

            # hovering
            start = time.time()
            for _ in range(400):
                cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
                time.sleep(0.1)

                if switch == 0: 
                    logger = logger1
                elif switch == 1:
                    logger = logger2
                elif switch == 2:
                    logger = logger3
                elif switch == 3:
                    logger = logger4

                for log_entry in logger:
                    Logger(label, switch)
                    switch += 1
                    break

                if switch == 4:
                    switch = 0 
            end = time.time()

            print(end - start)

            """
            # turns around
            for _ in range(10):
                cf.commander.send_hover_setpoint(0, 0, 180, 0.4)
                time.sleep(0.1)

                for log_entry in logger:
                    Logger()
                    break
            # move forward
            for _ in range(20):
                cf.commander.send_hover_setpoint(0.3, 0, 0, 0.4)
                time.sleep(0.1)

                for log_entry in logger:
                    Logger()
                    break
            """
            
            # landing
            for y in range(10):
                cf.commander.send_hover_setpoint(0, 0, 0, (10-y)/25)
                time.sleep(0.1)
           

        cf.commander.send_stop_setpoint()

        df.to_csv("data_set_label_"+str(label)+"_packet_"+sys.argv[2]+".csv")
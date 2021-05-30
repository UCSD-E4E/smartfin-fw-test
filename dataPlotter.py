#!/usr/bin/env python3

import e4e.decoder
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import IPython
import traceback

def plotFile(fileName:str)->str:
    ensembles = []
    with open(fileName, 'r') as dataFile:
        for line in dataFile:
            try:
                ensembles.extend(e4e.decoder.decodeRecord(line.strip()))
            except Exception as e:
                traceback.print_exc()
                print(e)
                IPython.embed()

    df = pd.DataFrame(ensembles)
    df = e4e.decoder.convertToSI(df)
    
    outputDir = os.path.splitext(fileName)[0]
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)

    plt.scatter(df.index, df['timestamp'])
    plt.xlabel('Ensemble Number by decode order')
    plt.ylabel('Timestamp (s)')
    plt.title('Time vs Ensemble Number')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'EnsembleNumber.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Temperature'])
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (C)')
    plt.title("Temperature vs Time")
    plt.grid()
    plt.savefig(os.path.join(outputDir, "Temperature.png"))
    plt.close()

    plt.scatter(df['timestamp'], df['Water Detect'])
    plt.xlabel('Time (s)')
    plt.ylabel('Water Detect Reading')
    plt.title('Water Detect Reading')
    plt.grid()
    plt.savefig(os.path.join(outputDir, "WaterDetect.png"))
    plt.close()

    plt.scatter(df['timestamp'], df['X Acceleration'])
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.title('X Acceleration')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Acceleration_x.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Y Acceleration'])
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.title('Y Acceleration')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Acceleration_y.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Z Acceleration'])
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.title('Z Acceleration')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Acceleration_z.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['X Angular Velocity'])
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (deg/s)')
    plt.title('X Angular Velocity')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'AngularVel_x.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Y Angular Velocity'])
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (deg/s)')
    plt.title('Y Angular Velocity')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'AngularVel_y.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Z Angular Velocity'])
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (deg/s)')
    plt.title('Z Angular Velocity')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'AngularVel_z.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['X Magnetic Field'])
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field Strength (uT)')
    plt.title('X Magnetic Field')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Magfield_x.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Y Magnetic Field'])
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field Strength (uT)')
    plt.title('Y Magnetic Field')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Magfield_y.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['Z Magnetic Field'])
    plt.xlabel('Time (s)')
    plt.ylabel('Magnetic Field Strength (uT)')
    plt.title('Z Magnetic Field')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Magfield_z.png'))
    plt.close()

    plt.scatter(df['timestamp'], df['battery'])
    plt.xlabel('Time (s)')
    plt.ylabel('Battery Voltage (mV)')
    plt.title('Battery Voltage')
    plt.grid()
    plt.savefig(os.path.join(outputDir, 'Battery.png'))
    plt.close()


if __name__ == "__main__":
    folder = '/home/ntlhui/workspace/smartfin-fw-test/test_results/smartfin5_SF_DeployCycle_2021-05-30-00-54-58/'
    for logFile in glob.glob(os.path.join(folder, 'Sfin*.log')):
        print("Graphing %s", logFile)
        plotFile(logFile)
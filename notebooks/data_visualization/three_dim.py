import mindwave, time, datetime
import matplotlib.pyplot as plt
import collections
import numpy as np
from matplotlib.animation import FuncAnimation
import pandas as pd
import os
from mpl_toolkits.mplot3d import axes3d


def check_device():
    command = "find /dev/ -name rfcomm*"
    result = os.popen(command).read()
    items = result.split('\n')
    items.remove('')
    check = -999
    for i in range(len(items)):
        if int(items[i][-1]) > check:
            check = int(items[i][-1])
    for i in range(len(items)):
        if int(items[i][-1]) == check:
            device = items[i]
    return device

def connect_device(new_device): 
    headset = mindwave.Headset(new_device)
    print("Device is connected!! id: %s\n"%new_device)
    time.sleep(2)
    
    return headset

device = check_device()
headset = connect_device(device)
data = collections.defaultdict(list)
proj = 'Carnival'
title = 'title here'
resol = 0.5
t = 0

fig, ax = plt.subplots(figsize = (10, 5),
                        subplot_kw = {"projection": "3d"})
fontlabel = {"fontsize":"large", "color":"gray", "fontweight":"bold"}

def animate(i):
    data['attention'].append(headset.attention)
    data['meditation'].append(headset.meditation)
    data['time'].append(len(data['attention']))
    if len(data['attention']) > 500:
        check = sum(data['attention'])
        if check != 0:
            ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            fname = f'./data/{proj}_{ts}.csv'
            df = pd.DataFrame.from_dict(data)
            df.to_csv(fname, sep = ';', columns = ['attention', 'meditation'], index = False)
        data['attention'] = []
        data['meditation'] = []
        data['time'] = []
    plt.cla()
    ax.plot(data['attention'], data['meditation'], data['time'])
    ax.set_title(title, fontsize = 20, pad = 30.)
    ax.set_xlabel("signal 1", fontsize = 20, labelpad = 20.)
    ax.set_ylabel("signal 2", fontsize = 20, labelpad = 20.)
    ax.set_zlabel("time", fontsize = 20, rotation = 90, labelpad = 10.)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.tick_params(axis = 'x', labelsize = 15)
    ax.tick_params(axis = 'y', labelsize = 15)
    ax.tick_params(axis = 'z', labelsize = 15)
    


    
    
ani = FuncAnimation(fig, animate, interval = 1000)
plt.tight_layout()
plt.show()
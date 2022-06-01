import mindwave, time, datetime
import matplotlib.pyplot as plt
import collections
import numpy as np
from matplotlib.animation import FuncAnimation
import pandas as pd
import os


proj = 'Carnival'
title = 'title here'

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
resol = 0.5
t = 0

def animate1(i):
    data['attention'].append(headset.attention)
    data['meditation'].append(headset.meditation)
    if len(data['attention']) > 500:
        check = sum(data['attention'])
        if check != 0:
            ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            fname = f'./data/{proj}_{ts}.csv'
            df = pd.DataFrame.from_dict(data)
            df.to_csv(fname, sep = ';', columns = ['attention', 'meditation'], index = False)
        data['attention'] = []
        data['meditation'] = []      

    plt.cla()
    plt.title(title, fontsize = 20)
    plt.plot(data['attention'], label = 'attention')
    plt.plot(data['meditation'], label = 'meditation')
    plt.legend(loc = 'lower left')
    plt.ylabel('signal', fontsize = 20)
    plt.xlabel('time', fontsize = 20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    
def animate2(i):
    data['attention'].append(headset.attention)
    data['meditation'].append(headset.meditation)
    if len(data['attention']) > 500:
        check = sum(data['attention'])
        if check != 0:
            ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            fname = f'./data/{proj}_{ts}.csv'
            df = pd.DataFrame.from_dict(data)
            df.to_csv(fname, sep = ';', columns = ['attention', 'meditation'], index = False)
        data['attention'] = []
        data['meditation'] = []
    
    plt.cla()
    plt.title(title, fontsize = 20)
    plt.plot(data['attention'], data['meditation'])
    plt.ylabel('signal 1', fontsize = 20)
    plt.xlabel('signal 2', fontsize = 20)
    #plt.xlim(0, 100)
    #plt.ylim(0, 100)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    
    
    
def animate3(i):
    scat_sz = [50, 100, 200, 400, 600, 800, 1000, 1500]
    scat_c = ['r', 'g', 'b', 'c', 'm', 'k', 'orange', 'lime', 'cornflowerblue', 'hotpink']
    scat_mk = ['s', 'o', 'p', '*', 'P', '+', 'v', '^', '>', '<', 'D', 'h']
    data['attention'].append(headset.attention)
    data['meditation'].append(headset.meditation)
    data['size'].append(np.random.choice(scat_sz))
    data['color'].append(np.random.choice(scat_c))
    data['symbol'].append(np.random.choice(scat_mk))
    
    if len(data['attention']) > 100:
        check = sum(data['attention'])
        if check != 0:
            ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            fname1 = f'./data/{proj}_{ts}.csv'
            df = pd.DataFrame.from_dict(data)
            df.to_csv(fname1, sep = ';', columns = ['attention', 'meditation', 'size', 'color', 'symbol'], index = False)
        data['attention'] = []
        data['meditation'] = []
        data['size'] = []
        data['color'] = []
        data['symbol'] = []
    
    plt.cla()
    for i in range(len(data['attention'])):
        plt.scatter(data['attention'][i], data['meditation'][i],
                    s = data['size'][i],
                    c = data['color'][i],
                    edgecolors = 'none',
                    marker = data['symbol'][i],
                    alpha = 0.4)
   
    plt.title(title, fontsize = 20)
    plt.ylabel('signal 1', fontsize = 20)
    plt.xlabel('signal 2', fontsize = 20)
    #plt.xlim(0, 100)
    #plt.ylim(0, 100)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    
#ani1 = FuncAnimation(plt.gcf(), animate1, interval = int(resol*500))    
#ani2 = FuncAnimation(plt.gcf(), animate2, interval = int(resol*2000))
ani3 = FuncAnimation(plt.gcf(), animate3, interval = int(resol*1000))

plt.tight_layout()
plt.show()
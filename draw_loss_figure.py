import matplotlib.pyplot as plt
import re
from mpl_toolkits.axes_grid1 import host_subplot
import numpy as np
import os

def get_loss_data(file_dir):
    data = []
    data_list = []
    fp = open(file_dir, 'r')
    for ln in fp:
        if 'epoch: ' in ln:
            # eopch
            epoch_data = re.findall(r'epoch: \b\d+\b', ln)
            epoch = int(epoch_data[0].strip(' ')[7:])
            data.append(epoch)
            # iters
            iters_data = re.findall(r'iters: \b\d+\b', ln)
            iters = int(iters_data[0].strip(' ')[7:])
            data.append(iters)
            # RMSE
            RMSE_data = re.findall(r'RMSE_m: \b\S+\b', ln)
            RMSE = float(RMSE_data[0].strip(' ')[8:])
            data.append(RMSE)
            # MAE
            MAE_data = re.findall(r'MAE_m: \b\S+\b', ln)
            MAE = float(MAE_data[0].strip(' ')[7:])
            data.append(MAE)

            data_list.append(data)
        data = []
    fp.close()
    return data_list

def get_all_avg_loss(data, which):
    Sum = 0
    avg_list = []
    count = 0
    epoch = data[-1][0]
    iters = data[-1][1]

    if which == 'RMSE':
        for var in data:
            Sum += var[2]  # RMSE在列表中的第5位
            count += 1
            if count % iters == 0:
                avg_list.append(Sum / iters)
                Sum = 0
    elif which == 'MAE':
        for var in data:
            Sum += var[3]  # MAE在列表中的第6位
            count += 1
            if count % iters == 0:
                avg_list.append(Sum / iters)
                Sum = 0
    # print(avg_list)

    return avg_list

data_10per = get_loss_data('./train/train_errors_count0.1.txt')
avg_list_10per  = get_all_avg_loss(data_10per, 'MAE')

x = range(0, 300)
plt.plot(x,avg_list_10per,label='10%-Sparse',linewidth=1,color='r') 
plt.xlabel('epoch') 
plt.ylabel('error') 
plt.title('MAE') 
plt.axis([0, 310, 0.6, 1])  
plt.grid(True)
plt.legend() # 用于显示图例
plt.savefig('./MAE.png')
plt.show()
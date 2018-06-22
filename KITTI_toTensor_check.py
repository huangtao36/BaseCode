
# coding: utf-8

# 这个代码用于检测将KITTI数据转为0-1之间的数时的分布情况

# In[2]:


import os
import os.path
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.utils.data as data
import numpy as np
import matplotlib.pyplot as plt


# In[18]:


class ToTensor_85(object):
    def __call__(self, pic):
        img = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))

        nchannel = len(pic.mode)
        img = img.view(pic.size[1], pic.size[0], nchannel)
        img = img.transpose(0, 1).transpose(0, 2).contiguous()

        return img.float().div(85)


# In[19]:


img = Image.open('./dataset/dataset10/train/groundtruth/801.png').convert('RGB')


# In[20]:


im3 = np.array(img).squeeze()
plt.hist(im3.flatten(), bins=200)
plt.xlim([0, 85])
plt.ylim([0, 50000])
plt.show()


# In[21]:


region = (0, 120, 1216, 352)
Crop_img = img.crop(region)

Crop_Again_img = transforms.CenterCrop((176, 608))(Crop_img)
Crop_Again_image_totensor = ToTensor_85()(Crop_Again_img)


# In[22]:


"""
使用NEAREST的时候数据分布差别不大，建议使用
"""
Scale_img = transforms.Scale((608,176), Image.NEAREST)(img)
Scale_image_totensor = ToTensor_85()(Scale_img)


# In[23]:


im3 = Crop_Again_image_totensor.numpy().squeeze()
plt.hist(im3.flatten() * 85, bins=200)
plt.xlim([0, 85])
plt.ylim([0, 20000])
plt.show()


# In[24]:


im4 = Scale_image_totensor.numpy().squeeze()
plt.hist(im4.flatten() * 85, bins=200)
plt.xlim([0, 85])
plt.ylim([0, 20000])
plt.show()


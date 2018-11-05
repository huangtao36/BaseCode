
# coding: utf-8

# 用于分析KITTI的数据

# In[61]:


import numpy as np
from scipy import misc
import matplotlib.pyplot as plt


# In[222]:


fake_b = misc.imread('./test/images/19_2011_09_26_drive_0036_sync_image_0000000107_image_02_fake_b.png')
real_b = misc.imread('./test/images/19_2011_09_26_drive_0036_sync_image_0000000107_image_02_real_b.png')
real_A = misc.imread('./test/images/19_2011_09_26_drive_0036_sync_image_0000000107_image_02_real_a.png')
rec_A = misc.imread('./test/images/19_2011_09_26_drive_0036_sync_image_0000000107_image_02_rec_a.png')
real_c = misc.imread('./test/images/19_2011_09_26_drive_0036_sync_image_0000000107_image_02_real_c.png')

fake_B = fake_b / 256.
real_B = real_b / 256.
real_C = real_c / 256.

mask = (real_B > 0).astype(float)


# In[223]:


image = np.abs(fake_B * mask - real_B)
image= (image > 10) * image
print(np.max(image))
plt.imshow(image)
plt.show()


# In[224]:


# fake_B = fake_B / 256.
# real_B = real_B / 256.

B_error = np.abs(fake_B * mask - real_B)
print(fake_B.size)


# In[225]:


b_error = B_error.flatten()
b_error = b_error ** 2
b_error = np.sort(b_error)

count = np.count_nonzero(mask > 0)
print("MAE = ", np.sum(B_error)/count)
# plt.hist(b_error, bins=100)
plt.plot( b_error)
plt.show()

fb_ = np.sort(fake_B.flatten() ** 2)
plt.plot(fb_)
plt.show()


# In[231]:


big_pred_msk = ((fake_B*mask) > 20).astype(np.float)
big_error_msk = (np.abs(fake_B * mask - real_B) > 50).astype(np.float)


# In[232]:


big_error = big_error_msk * fake_B * mask
big_error.nonzero()


# In[235]:


plt.imshow(real_B[130:170, 680:770])
plt.show()
plt.imshow(fake_B[130:170, 680:770])
plt.show()
plt.imshow(real_C[130:170, 680:770])
plt.show()
plt.imshow(real_A[130:170, 680:770])
plt.show()
plt.imshow(rec_A[130:170, 680:770])
plt.show()


# In[215]:


fake_B[130:170, 400:500]


# In[216]:


real_B[130:170, 400:500]


# In[83]:


plt.imshow(big_pred_msk)
plt.show()
plt.imshow(big_error_msk)
plt.show()
plt.imshow(big_pred_msk*big_error_msk)
plt.show()
plt.imshow(big_pred_msk+big_error_msk)
plt.show()


# In[97]:


B_error.shape


# In[12]:


real_a = misc.imread('./images/270_2011_10_03_drive_0047_sync_image_0000000491_image_02_real_a.png')
rec_a = misc.imread('./images/270_2011_10_03_drive_0047_sync_image_0000000491_image_02_rec_a.png')

real_a = np.dot(real_a[...,:3], [0.299, 0.587, 0.144])
rec_a = np.dot(rec_a[...,:3], [0.299, 0.587, 0.144])


# In[42]:


A_error = np.abs(real_a - rec_a)
A_error = A_error.flatten()
a_error = A_error[110000:250000]
print(np.mean(a_error))
# error2 = error2[0:3000]
# print(error2)
plt.plot(range(a_error.size), a_error)
plt.show()


#!/usr/bin/env python
# coding: utf-8

# In[1]:


from astropy.io import fits
import numpy as np


# #### 打开，读取FITS文件

# In[2]:


hdul = fits.open('glg_tte_b0_bn200716957_v00.fit')


# open()函数可以有别的可选参数。默认只读。  
# open()函数返回一个对象叫做 HDUList，这是一个HDU（[Header Data Unit](https://docs.astropy.org/en/stable/io/fits/api/hdus.html)）的list。  
# HDU（[Header Data Unit](https://docs.astropy.org/en/stable/io/fits/api/hdus.html)）是FITS文件结构的最高级构件，HDU下包含了Header, data array, or table.  

# 这里应该有个数据文件介绍。。。 

# In[3]:


hdul.info()


# 用fv软件([FV下载地址](https://heasarc.gsfc.nasa.gov/docs/software/ftools/fv/))打开是这样的:  
# ![image.png](attachment:3e2e56ed-416d-4409-a795-f20d79da8646.png)

# 可通过hdul[0,...]调取每一个元素（HDU）,然后可以再用HDU.header(/data)调取每一个HDU的下级header/data数据。

# In[4]:


hdul[0].header


# FITS文件某个HDU的header可以理解为这个HDU的名片？  
# 这个‘名片’的每一行包含3个元素：keyword, value, comment。  
# keyword 和 comment 必须字符串格式  
# value 可以是字符串，整数，浮点数，布尔数（true/fause）

# In[5]:


hdul[0].data


# 这里没有输出，应该是空值。

# In[6]:


hdul[1].header


# In[7]:


hdul[1].header['BITPIX']


# In[8]:


hdul[1].header.comments['BITPIX']


# In[9]:


hdul[1].data


# 对照软件打开的图形界面：  
# ![image.png](attachment:d99236f9-63ee-4b30-b024-1872401fd2c0.png)      
# 对应hdul [1].data  
# ![image.png](attachment:67cae395-2c3e-4713-9b54-b0cbde8b4aed.png)      
# hdul[1].data有128行，对应GBM探测器的128个能道（channel），每一行的E_MIN, E_MAX是对应能道的下边界，上边界。  

# 对应值的读取：

# In[10]:


hdul[1].data[2,]


# 也可通过对应数据名称读取：

# In[11]:


hdul[1].data['CHANNEL']


# In[12]:


hdul[1].data['E_MIN']


# 小结：  
# 通过 astropy.io.fits.open() 打开FITS文件，返回hdul。    
# 通过 hdul[#].header/data调取某个HDU的header/data数据。
# HDU至少（一般？）有Primary, 一般都还有别的extension，比如此文件就还有EBOUNDS, EVENTS, GTI。  
# 通过 hdul[#].data['...'] 调用相关数据，返回一个array

# #### 修改FITS文件

# 添加header

# In[13]:


hdul[1].header['TEST']=(100,'student')


# In[14]:


hdul[1].header


# 可以看到最后一行有刚添加的信息。

# In[15]:


hdul['EBOUNDS'].data
# or hdul[1].data


# In[16]:


#type(hdul['EBOUNDS'].data)


# In[17]:


hdul['EBOUNDS'].data[2][1]


# In[18]:


#hdul['EBOUNDS'].data[10:20]


# In[19]:


cols = hdul[1].columns
cols.info()
# or hdul[1].columns


# 可见fits文件包含了许多信息

# In[20]:


hdul[1].columns.names


# In[21]:


hdul[1].data['E_MAX']


# In[22]:


hdul[1].data['E_MAX'][:] = 0
hdul[1].data['E_MAX']


# In[23]:


hdul.writeto('test1.fits')


# ![image.png](attachment:2161f585-1ad0-418a-9ce0-1e3d079dfad3.png)

# #### 创建新的FITS文件, 修改已有的FIT文件

# ##### Creating a New Image File

# In[24]:


n = np.arange(100)
hduuu = fits.PrimaryHDU(n)
#hdul = fits.HDUList([hduuu])
#hduuu.info()
hduuu.writeto('newl1.fits')


# ##### Creating a New Table File

# In[25]:


from astropy.table import Table
t = Table([[1, 2], [4, 5], [7, 8]], names=('a', 'b', 'c'))
t.write('table11.fits', format='fits')


# ![image.png](attachment:f1ecb1dd-c5b0-42fa-9bfd-60c139813034.png)

# 或者

# In[26]:


c1 = fits.Column(name='a', array=np.array([1, 2]), format='K')
c2 = fits.Column(name='b', array=np.array([4, 5]), format='K')
c3 = fits.Column(name='c', array=np.array([7, 8]), format='K')
t = fits.BinTableHDU.from_columns([c1, c2, c3])
t.writeto('table2.fits')


# ![image.png](attachment:3db4c9cb-8819-418c-a646-7891ffea6eeb.png)

# In[27]:


a1 = np.array(['NGC1001', 'NGC1002', 'NGC1003'])
a2 = np.array([11.1, 12.3, 15.2])
col1 = fits.Column(name='target', format='20A', array=a1)
col2 = fits.Column(name='V_mag', format='E', array=a2)


# ColDefs:column-definitions

# In[28]:


cols = fits.ColDefs([col1, col2])
hdu = fits.BinTableHDU.from_columns(cols)


# In[29]:


hdu.writeto('table3.fits')


# ![image.png](attachment:95d40896-ccc2-4e7c-950d-aa62c5fe8dae.png)

# ##### Creating a File with Multiple Extensions  
# To create a file with multiple extensions we need to create extension HDUs and append them to an HDUList.

# In[30]:


n = np.ones((3, 3))
n2 = np.ones((100, 100))
n3 = np.ones((10, 10, 10))
primary_hdu = fits.PrimaryHDU(n)
image_hdu = fits.ImageHDU(n2)
image_hdu2 = fits.ImageHDU(n3)
c1 = fits.Column(name='a', array=np.array([1, 2]), format='K')
c2 = fits.Column(name='b', array=np.array([4, 5]), format='K')
c3 = fits.Column(name='c', array=np.array([7, 8]), format='K')
table_hdu = fits.BinTableHDU.from_columns([c1, c2, c3])
hdul = fits.HDUList([primary_hdu, image_hdu, table_hdu])
hdul.append(image_hdu2)


# In[31]:


hdul.writeto('multi.fits')


# ![image.png](attachment:b1837238-6bdb-4958-a1fd-19e9b675b68a.png)

# 修改已有的FITS文件

# In[32]:


hdul = fits.open('glg_tte_b0_bn200716957_v00.fit')
hdul.info()


# ![image.png](attachment:8deb2388-1bf7-479e-8596-426c5281ae5c.png)

# In[33]:


c1 = fits.Column(name='TIMES', array=np.ones(8), format='K')
c2 = fits.Column(name='RATES', array=np.ones(8), format='K')
c3 = fits.Column(name='ERRORS', array=np.ones(8), format='K')


# In[34]:


table_hdu = fits.BinTableHDU.from_columns([c1, c2, c3])


# In[35]:


hdul.append(table_hdu)


# In[36]:


hdul.writeto('append.fits')


# In[37]:


hdul.info()


# ![image.png](attachment:fae63891-2a40-4bee-b848-9684a9179f42.png)
# ![image.png](attachment:618dc3a7-4a2d-4e47-92c8-3668c18d57db.png)

# In[38]:


hdul[4].data['TIMES']


# In[ ]:





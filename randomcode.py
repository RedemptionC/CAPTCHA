# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 21:20:00 2018

@author: r
"""

import pandas as pd
from PIL import Image
import os
import knn as k

path=r'E:\downloadpic\randomcode'
newImgPath=r'E:\downloadpic\processedPic'
singleCharPath=r'E:\downloadpic\singlechar'
def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
 
    return table

#对图片Img降噪
def denoise(Img,newImgPath,index):
    img=Img
    #data=img.im
    w,h=img.size
    for i in range(1,w-1):
        for j in range(1,h-1):
            if img.getpixel((i,j))==0:
                left=img.getpixel((i-1,j))
                left_up=img.getpixel((i-1,j+1))
                left_down=img.getpixel((i-1,j-1))
                up=img.getpixel((i,j+1))
                down=img.getpixel((i,j-1))
                right=img.getpixel((i+1,j))
                right_up=img.getpixel((i+1,j+1))
                right_down=img.getpixel((i+1,j-1))
                if left+left_up+left_down+up+down+right+right_up+right_down>5:
                    img.putpixel((i,j),1)
                    #print('({},{})'.format(i,j))
            else:continue
    img.save(newImgPath+"\{}.png".format(index))

def singleChar(Img,index,path=singleCharPath):
    left=4
    up=4
    right=4+8
    down=16
    for i in range(4):
        childImg=Img.crop((left,up,right,down))
        left+=10#2+8，间隙加字宽
        right+=10
        childImg.save(path+r'\{}_{}.png'.format(index,i))

def img2str(img):
    img=Image.open(img)
    string=''
    table = get_bin_table()
    imgry=img.convert('L')
    out = imgry.point(table, '1')
    path=r'C:\Users\r\Desktop\temp'
    denoise(out,path,'1')
    img2=Image.open(os.path.join(path,'1.png'))
    singleChar(img2,'1',path)
    for i in range(4):
        img=Image.open(path+r'\{}_{}.png'.format(1,i))
        string+=k.knn(img)
    return string
if __name__ =='__main__':
    table = get_bin_table()
    for i in range(1,20):
    #path=r'C:\Users\r\Desktop\temp'
        img=Image.open(r'E:\downloadpic\randomcode'+r'\{}.png'.format(i))
        imgry=img.convert('L')
        out = imgry.point(table, '1')
        path=r'C:\Users\r\Desktop\temp'
        denoise(out,path,'1')
        img2=Image.open(os.path.join(path,'1.png'))
        singleChar(img2,'1',path)
        for i in range(4):
            img=Image.open(path+r'\{}_{}.png'.format(1,i))
            print(k.knn(img),end='')
        print('')


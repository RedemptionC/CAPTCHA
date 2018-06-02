# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:12:13 2018

@author: r
"""
from PIL import Image
import os

#img1是要进行测试的字符，img是对照的（labeled data）
def getdiff(img1,img):
    w,h=img1.size
    diff=0
    for i in range(w):
        for j in range(h):
            if img1.getpixel((i,j))!=img.getpixel((i,j)):
                diff+=1
    return diff

def knn(img):
    path=r'E:\downloadpic\classfication'
    allClass=os.listdir(path)
    path=r'E:\downloadpic\classfication'
    allClass=os.listdir(path)
    rank=dict()
    for i in allClass:
        classPath=os.path.join(path,i)
        allpic=os.listdir(classPath)
        sum=0
        for j in allpic:
            thispic=os.path.join(classPath,j)
            img2=Image.open(thispic)
            sum+=getdiff(img,img2)
        rank[sum/len(allpic)]=i
    l=list(rank.keys())
    l.sort()
    i=rank[l[0]]
    return i


if __name__=="__main__":
    img=Image.open(r'E:\downloadpic\singlechar\28_1.png')
    print(knn(img))
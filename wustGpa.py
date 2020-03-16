# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 15:47:26 2018

@author: r
"""

import requests as req
import os
import csv
from bs4 import BeautifulSoup as BS
import pandas as pd
from randomcode import img2str

loginUrl=r"http://jwxt.wust.edu.cn/whkjdx/Logon.do?method=logon"
randomCodeUrl=r"http://jwxt.wust.edu.cn/whkjdx/verifycode.servlet"
data={"USERNAME":"","PASSWORD":"","x":"0","y":"0"}
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko",
        "Referer":"http://jwxt.wust.edu.cn/whkjdx/Logon.do?method=logon",
        "Host": "jwxt.wust.edu.cn",
        "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
        "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive"
        }
#设置账号密码（data是全局变量，设置一次即可，不用在每个函数里设置）
def setaccount(id,pwd):
    data["USERNAME"]=id
    data["PASSWORD"]=pwd
#仅返回cookies
def getcookies(path=None):

    flag=None
    while flag==None:
        #首先获取验证码
        imgobj=req.get(randomCodeUrl)
        #验证码路径...
        with open("img.jpg","wb") as f:
            f.write(imgobj.content)
        #人工识别改为机器识别
        img=('img.jpg')
        code=img2str(img)
        data["RANDOMCODE"]=code
        login=req.post(loginUrl,data=data,cookies=req.utils.dict_from_cookiejar(imgobj.cookies),headers=header)
        b=BS(login.text,'html5lib')
        if b.title!=None:
            #登录失败
            errorinfo=b.find("span",{"id":"errorinfo"})
            if errorinfo!=None:
                
                if(errorinfo.string=='验证码错误!!'):
                    continue
                    print('验证码错误!!')
                elif errorinfo.string=='该帐号不存在或密码错误,请联系管理员!':
                    #这里是对一个账号进行爬取，如果不存在，应该函数中断，换下一个id
                    return None
                #continue
        else:
            break
    #只获取cookies，返回cookies和id密码
    cookies=req.utils.dict_from_cookiejar(imgobj.cookies)
    #访问sso接口，获取权限
    sso=req.get("http://jwxt.wust.edu.cn/whkjdx/Logon.do?method=logonBySSO",cookies=cookies,headers=header)
    #return cookies,id,pwd
    return cookies

def getgpa(cookies):
    #main=req.get("http://jwxt.wust.edu.cn/whkjdx/framework/main.jsp",cookies=cookies,headers=header)
    header["Referer"]="http://jwxt.wust.edu.cn/whkjdx/framework/main.jsp"
    gpa=req.post("http://jwxt.wust.edu.cn/whkjdx/xszqcjglAction.do?method=queryxscj",cookies=cookies,headers=header)
    return gpa.text

def getscheme(cookies):
    pass

def setpwd(cookies,pwd,newpwd):
    url=r"http://jwxt.wust.edu.cn/whkjdx/yhxigl.do?method=changMyUserInfo"
    data={"oldpassword":pwd,"password1":newpwd,"password2":newpwd,"button1":"保存"}
    rs=req.post(url,cookies=cookies,data=data,headers=header)
    return rs


            
def html2csv(html,id,path=None):
    bsobj=BS(html,"html5lib")
    trs=bsobj.find_all("tr")
    raw_data=trs[4:]
    raw_data.reverse()
    raw_data=raw_data[4:]
    raw_data.reverse()
    csvFile = open(r"C:\Users\r\Desktop\{}gpa.csv".format(id), "w+", encoding="utf-8",newline="")
    writer = csv.writer(csvFile)
    writer.writerow(("序号", "学号", "姓名", "学期", "课程", "分数", "成绩标志", "课程性质", "课程类别", "学时", "学分", "考试性质", "补重学期", "绩点"))
    for tr in raw_data:
        tds = tr.find_all("td")
        index = tds[0].string.strip()
        id = tds[1].string.strip()
        name = tds[2].string.strip()
        time_ = tds[3].string.strip()
        course = tds[4].string.strip()
        score = tds[5].string.strip()
        flag = tds[6].string.strip()
        charac = tds[7].string.strip()
        kind = tds[8].string.strip()
        length = tds[9].string.strip()
        weight = tds[10].string.strip()
        test_char = tds[11].string.strip()
        makeupTime = tds[12].string.strip()
        gpa = tds[13].string.strip()
        writer.writerow((index,id,name,time_,course,score,flag,charac,kind,length,weight,test_char,makeupTime,gpa))
    csvFile.close()
    return r"C:\Users\r\Desktop\{}gpa.csv".format(id)
    
def csv2gpa(csv):
    f=pd.read_csv(csv)
    sum=0.0
    weight=.0
    for i in range(len(f)):
        if f.loc[i,"绩点"]==0:
            print('绩点为0：')
            print(f.loc[i,"课程"])
            continue
        sum+=f.loc[i,"绩点"]*f.loc[i,"学分"]
        weight+=f.loc[i,"学分"]
    summary="总的平均绩点是{}".format(sum/weight)
    print(summary)
    
    sems=set(f.学期)
    sum=0
    weight=0
    for j in sems:
        for i in range(len(f)):
            if f.loc[i,"学期"]==j and f.loc[i,"绩点"]!=0:
                    print(str(f.loc[i,'课程'])+" ",end="")
                    print(str(f.loc[i,'学分'])+" ",end="")
                    print(str(f.loc[i,'绩点'])+" ",end="")
                    print(str(f.loc[i,'学期'])+" ",)
                    sum+=f.loc[i,"绩点"]*f.loc[i,"学分"]
                    weight+=f.loc[i,"学分"]
        summary+="\n{}的平均绩点是{}".format(j,sum/weight)
    print(summary)

if __name__=='__main__':
    id='201513158020'
    pwd=input("请输入密码：")
    setaccount(id,pwd)
    cookies=getcookies()
    if cookies!=None:
        gpa=getgpa(cookies)
        c=html2csv(gpa,id)
        csv2gpa(c)
        
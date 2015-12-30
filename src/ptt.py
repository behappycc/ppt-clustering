# -*- coding=UTF-8 -*-
import telnetlib
import sys
import Account #My file. It contains Account.id, Account.password 
import time
import re

tn = ""

def loginPtt():
    global tn
    tn = telnetlib.Telnet('ptt.cc')

    time.sleep(1)
    content = tn.read_very_eager().decode('big5','ignore')
    print("首頁顯示...")
    if "請輸入代號" in content:
        print("輸入帳號...")
        tn.write((Account.id+"\r").encode('big5') )
        time.sleep(1)
        content = tn.read_very_eager().decode('big5','ignore')

        print("輸入密碼...")
        tn.write((Account.password+"\r").encode('big5'))
        time.sleep(2)
        content = tn.read_very_eager().decode('big5','ignore')
        
        if "密碼不對" in content:
            print("密碼不對或無此帳號。程式結束")
            sys.exit()
        if "您想刪除其他重複登入的連線嗎" in content:
            print("發現重複連線,刪除他...")
            tn.write("y\r".encode('big5') ) 
            time.sleep(7)
            content = tn.read_very_eager().decode('big5','ignore')
        #print(content)
        while "任意鍵" in content:
            print("資訊頁面，按任意鍵繼續...")
            tn.write("\r".encode('big5') )
            time.sleep(2)
            content = tn.read_very_eager().decode('big5','ignore')
            
        if "要刪除以上錯誤嘗試" in content:
            print("發現嘗試登入卻失敗資訊，是否刪除?(Y/N)：",end= "")
            anser = input("")
            tn.write((anser+"\r").encode('big5') )
            time.sleep(1)

            content = tn.read_very_eager().decode('big5','ignore')
        print("----------------------------------------------")
        print("----------- 登入完成，顯示操作介面 -----------")
        print("----------------------------------------------")
    else:
        print("沒有可輸入帳號的欄位，網站可能掛了")
    
def enterUserList():
    # 進入使用者列表
    tn.write("\x15".encode("big5"))
    time.sleep(1)
    content = tn.read_very_eager().decode('big5', 'ignore')

def getUserIP(user_id):
    user_id += '\r'
    # 輸入Q
    tn.write("Q".encode("big5"))
    time.sleep(1)
    content = tn.read_very_eager().decode('big5', 'ignore')
    # 輸入帳號
    tn.write(user_id.encode("big5"))
    time.sleep(1)
    content = tn.read_very_eager().decode('big5', 'ignore')

    pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = re.search(pattern, content)
    while match is None:
        enterUserList()
        # 輸入Q
        tn.write("Q".encode("big5"))
        time.sleep(1)
        content = tn.read_very_eager().decode('big5', 'ignore')
        # 輸入帳號
        tn.write(user_id.encode("big5"))
        time.sleep(1)
        content = tn.read_very_eager().decode('big5', 'ignore')

    ip = match.group()
    tn.write("q".encode("big5"))
    
    return ip
    

def logoutPtt():
    print("----------------------------------------------")
    print("------------------- 登出 ----------------------")
    print("----------------------------------------------")
    tn.write("qqqqqqqqqg\r\ny\r\n".encode('big5') )
    time.sleep(1)
    tn.write("\r\n".encode('big5') )
     

if __name__ == "__main__":
    loginPtt()
    enterUserList()
    getUserIP('behappycc')
    logoutPtt()
    


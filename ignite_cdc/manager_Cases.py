from ast import And
from pyignite import Client
import random
client = Client()
client.connect('127.0.0.1', 10800)

import time
import os, sys

# Accounts management
check = input("請輸入驗證碼: ")

if( check != "0000" ):
    print("您並未取得權限!")
    os._exit(0)


now = time.localtime()
nowTime = "此系統提供查詢截至 " + time.strftime("%Y-%m-%d, %H:%M:%S", now) + " 之確診者資料"
print(nowTime)

CONFIRMED_SELECT_QUERY = "SELECT Name, ID, Date FROM Confirmed"
Confirmed = client.sql(CONFIRMED_SELECT_QUERY)

print("\n序號: 註冊名 / 電話 / 通報日期\n",end="\n")
count = 1
for row in Confirmed:
    print(count ,end=": ")
    print(*row)
    count += 1  

print("\n通報日隔天起算起7日後應刪除資料")
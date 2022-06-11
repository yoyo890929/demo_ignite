from cmath import e
import email
from matplotlib.collections import Collection
import certifi
from pyignite import Client
from flask import *
import random

client = Client()
client.connect('127.0.0.1', 10800)
print("資料庫連線成功")

app = Flask(
    __name__,
    static_folder="static",  #控制 static 的位置
    static_url_path="/"
)
app.secret_key = "abchahaha"


@app.route("/")
def homepage():
    msg = request.args.get("msg","")
    if msg == "success":
        return render_template("homepage.html",msg="註冊成功")
    else:
        return render_template("homepage.html")


@app.route("/signin",methods = ["POST"])
def signin():

    #前端接收資料
    phone = request.form["phone"]
    password= request.form["password"]

    #根據資料與資料庫互動
    # ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone + "' AND password = " + "'"+password +"'"
    ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone +"'"
    accounts = client.sql(ACCOUNT_SELECT_QUERY)
    
    
    # 判斷電話號碼資料庫裡有沒有
    # 有 -> 密碼錯誤 -> 再輸入一次
    # 有 -> 密碼正確 -> 導入會員頁面(memberpage) -> 印出接觸史
    #沒有-> 註冊頁面註冊(signin) -> 成功 -> 導回登入頁面(homepage)
    #(問題：為什麼輸入太短會error)

    ###############       有問題       ###################
    count = 0
    for row in accounts:
        count=count+1
    if count == 0 :
        return render_template("homepage.html",msg="帳號或密碼輸入錯誤")  
    else :
        ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone + "' AND password = " + "'"+password +"'"
        ac = client.sql(ACCOUNT_SELECT_QUERY)
        cnt = 0
        for row in ac:
            cnt=cnt+1
        if cnt == 0 :
            return render_template("homepage.html",msg="帳號或密碼輸入錯誤")  
        else:
            session["phone"] = phone
            return redirect("\member") 
    #####################################################

    # return redirect("/?msg=success")

@app.route("/signup",methods=["POST"])
def signup():
    return render_template("signuppage.html")  
    
@app.route("/signuppage",methods=["POST"])
def signuppage():
    name = request.form["name"]
    phone = request.form["phone"]
    password = request.form["password"]
    password_2 = request.form["password_2"]
    

    #註冊
    #輸入電話及密碼、確認密碼(不得與其他手機號碼重複)
    #確認後將資料輸入到SQL（怎麼插入）
    #導回首頁(homepage)，印出註冊成功

    ###############       怎麼插       ###################
    
    #ACCOUNT_SELECT_QUERY = "SELECT * FROM Account WHERE ID ='" + phone +"'"
    ACCOUNT_SELECT_QUERY = "SELECT Name, ID FROM Account"
    accounts = client.sql(ACCOUNT_SELECT_QUERY)

    for row in accounts:
        if( row[0] == name):
            return render_template("homepage.html",msg="此帳號已被註冊!!")
    #count = 0 #如果accounts篩出來是空的 count就會是0 檢測是否有註冊

    #for row in accounts:
    #    count=count+1

    #if count == 0 :
    if password != password_2:
        return render_template("signuppage.html",msg="兩次密碼不符")
    ACCOUNT_INSERT_QUERY = "INSERT INTO Account(Name, ID, Password) VALUES ("
    ACCOUNT_INSERT_QUERY += "\'" + name + "\', "
    ACCOUNT_INSERT_QUERY += "\'" + phone + "\', "
    ACCOUNT_INSERT_QUERY += "\'" + password + "\')"

    client.sql(ACCOUNT_INSERT_QUERY)

        #ACCOUNT_DATA = [
        #    [name,phone,password, '#','#']
        #]

        #for row in ACCOUNT_DATA:
            #client.sql(ACCOUNT_INSERT_QUERY, query_args=row)
    return render_template("homepage.html",msg="註冊成功")
    #else :
    #    return render_template("homepage.html",msg="手機已被註冊")

    #####################################################


@app.route("/signout")
def signout():
    #登出
    del session["phone"]
    return redirect("/")


@app.route("/member") 
def memberpage():
    #有接觸史 -> 印出接觸的日期、時間、地點等等
    #無接觸史 
    #要有一個登出按鈕 -> 導回首頁

    if "phone" in session:
        return render_template("memberpage.html") 
    else:
        return redirect("/")

## 主要寫這 ##
## 搜尋接觸史 ##

@app.route("/connectsearch",methods=["POST"])
def connectsearch():
    ##將帳號密碼對應帳號的 phone 日期 地點 匯入
    if "phone" in session:
        phone = session["phone"]
        #FOOTPRINT_SELECT_QUERY = "SELECT Name, Date, Place FROM Footprint WHERE ID = '" + phone +"'"
        #footprints = client.sql(FOOTPRINT_SELECT_QUERY)
        ##將確診者的資料匯入
        CONFIRMED_SELECT_QUERY = "SELECT Name, ID FROM Confirmed"
        confirmeds = client.sql(CONFIRMED_SELECT_QUERY)
        c = 0
        msg2 = '0'
        msg3 = ''
        ##交叉比對
        for row in confirmeds :
            if row[1] == phone :
                continue
            name = row[0]
            #date = row[1]
            INPUT_CASE = "SELECT Date, Place FROM Footprint WHERE Name = '" + name + "'"
            input_case = client.sql(INPUT_CASE)
            for row_s in input_case :
                date = row_s[0]
                place = row_s[1]
                CHECK_PRINT = "SELECT Date, Place FROM Footprint WHERE ID = '" + phone +"' AND Place = '" + place + "' AND Date = '" + date + "'"
                check_print = client.sql(CHECK_PRINT)
                
                count = 0
                for r in check_print:
                    count += 1
                if count != 0 :
                    print("有接觸")
                    s = ''.join(ch for ch in row_s[0] if ch.isdigit())
                    s_o = ''.join(ch for ch in msg2 if ch.isdigit())
                    #print(msg2)
                    if( s >= s_o ) :
                        msg2 = row_s[0]
                        msg3 = row_s[1]
                    c = c+1                   
        #print(c)      
        if( c!=0 ) :
            return render_template("connectpage.html",msg=phone,msg2=msg2,msg3=msg3)
        msg2 = "無"
        msg3 = "無"
        return render_template("connectpage.html",msg=phone,msg2=msg2,msg3=msg3) 

    else:
        return redirect("/") 

        """
        count = 0
        c = 0 
        ##遍歷所有資料
        for row in footprints :
            place = row[2]
            date = row[1]
            ##將確診者與足跡中地點時間相同者的資料匯入
            #(變數) = SELECT 目標欄位 WHERE 條件相符
            CONFIRMED_SELECT_QUERY = "SELECT Name, Date, Place FROM Confirmed WHERE Place = '"+place+"' AND Date = '"+date +"'"
            #一定要加client.sql才會執行 要不然只是字串
            confirmeds = client.sql(CONFIRMED_SELECT_QUERY)
            count = 0
            for r in confirmeds:
                count = count+1
            if count != 0 :
                print("有接觸")
                msg2=r[1]
                msg3=r[2]
                c = c+1
                return render_template("connectpage.html",msg=phone,msg2=msg2,msg3=msg3)  
        if c == 0 :
            msg2 = "無"
            msg3 = "無"
        return render_template("connectpage.html",msg=phone,msg2=msg2,msg3=msg3) 

        """
    


## 主要寫這 ##
## 確診回報系統、輸入驗證碼、填入資料 ##
@app.route("/diagnosedpage",methods=["POST"])
def diagnosedpage():
    return render_template("diagnosedpage.html")

@app.route("/diagnosed",methods=["POST"])
def diagnosed():
    name = request.form.get("name")
    Date = request.form.get("date")
    Place = request.form.get("place")
    phone = session["phone"]
        
    if( len(str(name))!=0 and len(str(Date))!=0 and len(str(Place))!=0) :
        ##這是insert to sql 的方法 每一個問號對應一個標籤 
        r = random.randint(0, 100000000)
        FOOTPRINT_INSERT_QUERY = "INSERT INTO Footprint(Name, ID, Date , Place, key) VALUES ("
        FOOTPRINT_INSERT_QUERY += "\'" + name + "\', "
        FOOTPRINT_INSERT_QUERY += "\'" + phone + "\', "
        FOOTPRINT_INSERT_QUERY += "\'" + Date + "\', "
        FOOTPRINT_INSERT_QUERY += "\'" + Place + "\', "
        FOOTPRINT_INSERT_QUERY += "\'" + str(r) + "\')"
        #FOOTPRINT_INSERT_QUERY = '''INSERT INTO Footprint(
        #    Name, ID, Password, Date , Place,key    
        #) VALUES (?, ?, ?, ?,?,?)'''
        ##將資料存進一個DATA 再將整個DATA insert
        #NEW_DATA = [
        #    [name,phone,"",Date,Place,random.randint(0, 100000000)]  
        #]
        #for row in NEW_DATA:
        client.sql(FOOTPRINT_INSERT_QUERY)
        return render_template("memberpage.html", msg="輸入成功!")
    else :
        return render_template("memberpage.html", msg="您未輸入資料!")
        


#/error?msg=錯誤訊息
@app.route("/error")
def error():
    msg = request.args.get("msg","發生錯誤")
    return render_template("errorpage.html", msg=msg) #傳入錯誤msg



app.run() #這要放最後面
import random
import string
import mysql.connector
mydb = mysql.connector.connect(host='localhost', user='root', password='root123', database= 'bankify')

def getacc(act_no):
    sql = ('select Acc_No from account where Acc_No =%s')
    data = (act_no,)
    x = mydb.cursor()
    x.execute(sql,data)
    result = x.fetchone()
    mydb.commit()
    if(result !=None):
        return True
    else:
        print("Account Doesnot Exist..")
        return False

def openacc(): 
    n = input("Enter your Name:- ")
    acc = '624' +''.join(random.choice(string.digits) for _ in range(8))
    db = input("Enter your Date of Birth[YYYY/MM/DD]:- ")
    add = input("Enter your Address:- ")
    cno = int(input("Enter your Contact Number:- ")) 
    ob = int(input("Enter Opening Balance:- "))
    pas = input("Set Password:- ")
    data1 = (n, acc, pas, db, add, cno, ob)
    data2 = (n, acc, pas, ob)
    sql1 = ('insert into  account values (%s,%s,%s,%s,%s,%s,%s)')
    sql2 = ('insert into  amount values (%s,%s,%s,%s)')
    x = mydb.cursor()
    x.execute(sql1,data1)
    x.execute(sql2,data2)
    mydb.commit()
    print("Your Account No.:-",acc)
    print("Data Entered Successfully")

def depamt():
    act_no = input("Enter the Account number:- ")
    if(not getacc(act_no)):
        return
    
    if(not password(act_no)):
        print("Invalid Password...Try Again")
        return
    
    amt = int(input("Enter the Amount you want to deposit:- "))
    if(amt<=0):
        return print("Invalid Amount")            
    sql3 = ('select Balance from amount where Acc_No =%s')
    data3 = (act_no,)
    x = mydb.cursor()
    x.execute(sql3,data3)
    result = x.fetchone()
    t = result[0]+amt
    sql4 = ('update amount set Balance=%s where Acc_No=%s')
    data4 = (t,act_no)
    x.execute(sql4, data4)
    mydb.commit()
    print("Money has been Deposited.")

def withdraw():
    act_no = input("Enter the Account number:- ")
    if(not getacc(act_no)):
        return
    
    if(not password(act_no)):
        print("Invalid Password...Try Again")
        return
    
    amt = int(input("Enter the Amount you want to Withdraw:- "))
    if(amt<=0):
        return print("Invalid Amount")
    sql5 = ('select Balance from amount where Acc_No =%s')
    data5 = (act_no,)
    x = mydb.cursor()
    x.execute(sql5,data5)
    result = x.fetchone()
    t = result[0]-amt
    if(t>=0):
        sql6 = ('update amount set Balance=%s where Acc_No=%s and Balance>=%s')
        data6 = (t,act_no,amt)
        x.execute(sql6, data6)
        mydb.commit()
        print("Rs.",amt," Withdrawn.")
    else:
        print("Amount Not Available.")

def balenq():
    act_no = input("Enter the Account number:- ")
    if(not getacc(act_no)):
        return
    
    if(not password(act_no)):
        print("Invalid Password...Try Again")
        return
    
    sql7 = ('select Balance from amount where Acc_No =%s')
    data7 = (act_no,)
    x = mydb.cursor()
    x.execute(sql7,data7)
    result = x.fetchone()
    t = result[0]
    mydb.commit()
    print ("Your current balance is:-",t)


def disditails():
    act_no = input("Enter the Account number:- ")
    if(not getacc(act_no)):
        return
    
    if(not password(act_no)):
        print("Invalid Password...Try Again")
        return
    
    sql8 = ('select * from account where Acc_No =%s')
    data8 = (act_no,)
    x = mydb.cursor()
    x.execute(sql8,data8)
    result = x.fetchone()
    print()
    print("Customer Details:-")
    print()
    print(" Name  "," Account_No ", "   DoB   ", "  Addr ", " Contact ", "Open..Bal")
    count = 0
    for i in result:
        if(count == 2):
            count+=1
            continue
        print(i, end="  ")
        count+=1
    print()
        
def closeacc():
    act_no = input("Enter the Account number:- ")
    if(not getacc(act_no)):
        return
    
    if(not password(act_no)):
        print("Invalid Password...Try Again")
        return
    
    sql9 = ('delete from account where Acc_No =%s')
    data9 = (act_no,)
    sql10 = ('delete from amount where Acc_No =%s')
    data10 = (act_no,)
    x = mydb.cursor()
    x.execute(sql9,data9)
    x.execute(sql10,data10)
    mydb.commit()
    print("Account Closed.")
        

def password(act_no):
    pas = input("Enter Password:- ")
    sqlp = ('select password from amount where Acc_No =%s')
    datap = (act_no,)
    x = mydb.cursor()
    x.execute(sqlp,datap)
    result = x.fetchone()
    t = result[0]
    mydb.commit()
    return t == pas

def main():
    choice = 0
    while(choice!=7):
        print('''
---------------------------------
|    1.Open Account             |
|    2.Deposit Amount           |
|    3.Withdraw Money           |
|    4.Balance Enquiry          |
|    5.Display Customer Details |
|    6.Close Account            |
|    7.Exit                     |
---------------------------------
        ''')
        choice = int(input("Enter The Task:- "))
        if(choice == 1):
            openacc()
        elif(choice == 2):
            depamt()
        elif(choice == 3):
            withdraw()
        elif(choice == 4):
            balenq()
        elif(choice == 5):
            disditails()
        elif(choice == 6):
            closeacc()
        elif(choice == 7):
            print()
            print("**Thanks For Visiting**")
            print()
        else:
            print("Invalid Choice.")

main()
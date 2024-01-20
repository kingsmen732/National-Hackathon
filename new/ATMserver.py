import socket
import json
import firebase_admin
from firebase_admin import db
from MessageTransfer import *

from _thread import *
import threading

lock = threading.Lock()

balance=0
min_balance = 100
max_withdrawal_limit = 15000
firebaseKeyFile = 'firebase-key.json'
firebaseDBUrl = 'https://cn-atm-simulation-default-rtdb.firebaseio.com/'

def threaded(a, mt):
    print('Start')
    global balance
    userData = mt.receiveJson(a)
    accno = userData["accno"]
    pin = userData["pin"]
    count=3
    strrs = '/' + accno
    dbRef = db.reference(strrs)
    account = dbRef.get()
    if account:
        while pin != account['pin']:
            count-=1
            if count==0:
                mt.sendJson(a, { "validPin": "X" })
                print('Account locked')
                lock.release()
                break
            else:
                mt.sendJson(a, { "validPin": "N", "remainingCount": str(count)})
                pin = mt.receiveString(a)
        print('Login successful')
        dataToSend = { "validPin": "Y", "name": account['name']}
        mt.sendJson(a, dataToSend)
                
    
    while True:
        
            if pin == account['pin']:
                selectedOption = mt.receiveJson(a)
                balance=account['balance']
                if selectedOption["option"] == '1':
                    print('Balance: ',balance)
                    mt.sendString(a, str(balance))
        
                if selectedOption["option"] == '2':
                    withdraw = selectedOption["amount"]
                    print("Withdraw: ", withdraw)
                    if int(withdraw)>max_withdrawal_limit:
                        mt.sendString(a, "N")
                        print('Max limit error')
                    elif int(withdraw) < balance:
                        if (balance - int(withdraw))<min_balance:
                            print('Min balance error')
                            mt.sendString(a, "0")
                        else:
                            balance = balance - int(withdraw)
                            print("New balance: ", balance)
                            account['balance']=balance
                            dbRef.update({ "balance": balance })
                            mt.sendString(a, str(balance))
                    else:
                        mt.sendString(a, "No")
        
                if selectedOption["option"] == '3':
                    deposit = selectedOption["amount"]
                    print("Deposit: ", deposit)
                    balance = balance + int(deposit)
                    print("New balance: ", balance)
                    account['balance']=balance
                    dbRef.update({ "balance": balance })
                    mt.sendString(a, str(balance))
                if selectedOption["option"] == 'e':
                    print('Session ended')
                    break
    a.close()


def Main():

    port = 1708
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
    s.bind((socket.gethostname(), port))
    print("socket binded to port", port)
    cred_obj = firebase_admin.credentials.Certificate(firebaseKeyFile)
    firebase_admin.initialize_app(cred_obj, {
        'databaseURL': firebaseDBUrl,
    })
    # messageTransfer = MessageTransfer()
    print("app initialized")
    s.listen(5)
    print("socket is listening")

    while True:
        clientsocket, address = s.accept()

        lock.acquire()
        print('Connected to :', address[0], ':', address[1])

        start_new_thread(threaded, (clientsocket,messageTransfer))
    s.close()

if __name__ == '__main__':
    Main()
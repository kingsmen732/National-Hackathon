import socket
import json
from MessageTransfer import *

def Main():

    port = 1708
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
    s.connect((socket.gethostname(), port))

    mt = MessageTransfer()

    print('Welcome to our ATM!')
    accno = input('Enter your account number: ')
    pin = input('Enter pin: ')
    inputData = { "accno": accno, "pin": pin }
    mt.sendJson(s, inputData)
    d=mt.receiveJson(s)
    print("data received", d)
    
    while d["validPin"] == "N":
        print("Incorrect pin! You have " + d["remainingCount"] + "more attempts.")
        pin = input('Enter pin: ')
        mt.sendString(s, pin)
        d=mt.receiveJson(s)
        
    if d["validPin"] == "X":
        print('Account locked')
    if d["validPin"] == "Y":
        print("got Y")
        print("got data")
        print('Welcome '+d["name"]+'!')
        while True:
            op = input('\nWhat would you like to do?'
                    '\n1: Check balance'
                    '\n2: Withdrawal'
                    '\n3: Deposit'
                    '\ne: End the current session\n: ')

            if op == '1':
                mt.sendJson(s, { "option": op })
                data = mt.receiveString(s)
                print('\nCurrent balance :', data)
                continue
        
            if op == '2':
                amount = input('\n Enter the amount to withdraw : ')
                mt.sendJson(s, { "option": op, "amount": amount })
                data = mt.receiveString(s)
                if data == 'N':
                    print("Withdrawal amount larger than max limit(15000)")
                elif data == 'O':
                    print("Minimum balance of 100 should be present")
                elif data == 'No':
                    print("Withdrawal amount larger than current balance.")
                else:
                    print('\nCurrent Balance :', data)
                continue

            if op == '3':
                amount = input('\n Enter the amount to deposit : ')
                mt.sendJson(s, { "option": op, "amount": amount })
                data = mt.receiveString(s)
                print('\nCurrent Balance :', data)
                continue
    
            if op == 'e':
                print("\nEnding session")
                mt.sendJson(s, { "option": op })
                break
            else:
                print("\nNot a valid input, try again.")
                continue

    s.close()


if __name__ == '__main__':
    Main()

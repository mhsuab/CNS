#!/usr/sbin/python3

from Crypto.Cipher import AES
import binascii
import os
from userClass import User
from myErrors import *
import secret

def pad(m):
    length = 16-len(m)%16
    return m+chr(length).encode()*length

def unpad(c):
    length = c[-1]
    for char in c[-length:]:
        if char!=length:
            raise paddingError('incorrect padding')
    return c[:-length]

def encrypt(m):
    aes = AES.new(secret.key,AES.MODE_CBC,secret.iv)
    return binascii.hexlify(secret.iv+aes.encrypt(pad(m.encode()))).decode()

def decrypt(c):
    aes = AES.new(secret.key,AES.MODE_CBC,secret.iv)
    return unpad(aes.decrypt(binascii.unhexlify(c)[0x10:])).decode()

def get_token():
    token = secret.user.serialize()
    return encrypt(token)

def create_user():
    try:
        username =input('Username : ')
        description = input('Description : ')
        newUser = secret.User.construct(username,0,0,description)
        token = newUser.serialize()
        return encrypt(token)
    except Exception as e:
        if e.__class__.__name__=='UnicodeDecodeError':
            print('Unicode Decode Error')
        else:
            print(e)
        return None

def login(ctoken):
    global LOGIN,USER
    try:
        token = decrypt(ctoken)
        USER = User.deserialize(token)
        LOGIN = True
    except Exception as e:
        if e.__class__.__name__=='UnicodeDecodeError':
            print('Unicode Decode Error')
        else:
            print(e)
        USER = None
        LOGIN = False
		

def logout():
    global LOGIN,USER
    USER = None
    LOGIN = False

def menu():
    print(f"{' menu ':=^20}")
    if LOGIN is False:
        print('1. get token')
        print('2. login')
        print('3. give up')
    else:
        print('1. account info')
        print('2. create user')
        print('3. get secret')
        print('4. logout')
    print(f"{'':=^20}")

if __name__=='__main__':
    LOGIN = False
    USER = None
    while True:
        menu()
        choice = input('your choice : ').strip()
        try:
            choice=int(choice)
        except:
            print('Invalid Command')
            continue
        if LOGIN is False:
            if choice==1:
                print(f'Here is your token : {get_token()}')
            elif choice==2:
                ctoken = input('Please provide your login token (hex encoded) : ').strip()
                login(ctoken)
            elif choice==3:
                print('Goodbye')
                break
            else:
                print('Invalid Command')
        else:
            if choice==1:
                if USER.isvip==1 or USER.isadmin==1:
                    print(f'Another cat! {secret.flag2}')
                    USER.print_user()
                else:
                    print('Privilege not granted')
            elif choice==2:
                if USER.isvip==1 and USER.isadmin==1:
                    print(f'Here is a cat gif : {secret.flag3}')
                    token = create_user()
                    if token is not None:
                        print(f'Here is your token : {token}')
                else:
                    print('Privilege not granted')
            elif choice==3:
                if USER.isvip==1 and USER.isadmin==1 and USER.name=='king of the cats':
                    print(f'Congratulations, here is the final cat : \n{secret.flag4}')
                else:
                    print('Access Denied')
            elif choice==4:
                logout()
            else:
                print('Invalid Command')

# importing required modules
import socket
import os
import pybase64
import time
import csv
from Crypto.PublicKey import RSA
from tkinter import Tk, filedialog
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP
from getpass import getpass
from pwn import *

# assigning necessary information for the initialization of the server
ip = socket.gethostbyname(socket.gethostname())
port = 5002
addr = (ip,port)

# generation of RSA key pair
key_gen = RSA.generate(2048, e=65537) 
public_key = key_gen.publickey().exportKey("PEM") 
private_key = key_gen.exportKey("PEM") 

# saving private key for decryption purposes
private_key_file = open('private_key.pem','wb')
private_key_file.write(private_key)
private_key_file.close()

# importing public key and implementing Pkcs1 padding
pub = RSA.importKey(public_key)
rsa_public_key = PKCS1_OAEP.new(pub)

# formally getting client's name
log.info('client starting')
x = input('Enter Client Name: ')

# initialization of Tkinter GUI for selection of file in an interactive enironment
root = Tk()
root.withdraw()
root.attributes('-topmost', True)

# intiating socket connection to the server and throws an exception if the server is not initiated before client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(addr)
except:
    log.info('[Exception] Server not found Exiting')   
    exit() 
client.send(x.encode())

try:
    # selecting file to transfer
    print('Choose the file which you want to transfer:')
    time.sleep(2)
    filepath = filedialog.askopenfilename()
    fileshared = open(filepath,'rb')
    filename = filepath.split('/')

    # reading the file data and sending the filename to the server
    data = fileshared.read()
    client.send(filename[-1].encode())
    msg = client.recv(1024).decode()
    

    # encoding the file first and then encrypting it and sending it to the server
    data = pybase64.b64encode(data)
    data = rsa_public_key.encrypt(data)
    print('File encrypted successfully')
    client.send(data)
    print('File transferred Successfully')
    print(f'[server] {msg}')
    fileshared.close()
    client.close()

# This excpetion is triggered when file of size more than 1 kb is uploaded. This exception is included because for files more than 1kb value error of 'plaintext is too long' is shown.
except ValueError as e:
    log.info("File size of 1kb can only be transferred!!!")
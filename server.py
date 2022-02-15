# importing all required libraries
import socket
import os
import pybase64
import time
import csv
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from art import *
from getpass import getpass
from pwn import *

# this is the server side program of the project
tprint('Secure Server')

def server_code():

    # assigning necessary information for the initialization of the server
    ip = socket.gethostbyname(socket.gethostname())
    port = 5002
    addr = (ip,port)

    # creating a log file to write server activities based on server run time
    log_name = time.ctime()
    log_name = 'server_log_'+log_name.replace(' ','-')
    log_file = open('server_logs_'+str(time.ctime()).replace(' ','-').replace(':','.')+'.txt','w')
    log.info('[' + datetime.now().strftime('%H:%M:%S')+'] server starting')
    log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] server starting\n')

    # initialization of the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    log.info('listening to the server')
    log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] listening to the server\n')

    # client connecting to the server
    while True:
        conn,addr = server.accept()
        name = conn.recv(4096).decode()
        log.info(f'new connection established with {addr} on {port}\nClient Name:{name}')
        log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] new connection established '+ip+'\n['+datetime.now().strftime('%H:%M:%S')+'] Client Name : '+name+'\n')
        
        try:
            # receiving the filename and writing it in the server side
            filename = conn.recv(1024).decode('utf-8')    
            file = open(filename, 'w')
            conn.send('file received from client'.encode())
            log_file.write('[' + datetime.now().strftime('%H:%M:%S')+f'] file {filename} received from client\n')

            # Collecting file data
            data = conn.recv(1024)
            log.info('file received from client')
            log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] file data collected\n')

            # Decrypting file data using RSA
            f = open('private_key.pem','rb')
            private_key = RSA.importKey(f.read())
            rsa_private_key = PKCS1_OAEP.new(private_key)
            data = rsa_private_key.decrypt(data)

            # decoding file data using base64 and writing it into a file
            data = pybase64.b64decode(data)
            file.write(data.decode())
            conn.send('[server] file data received from client'.encode())
            log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] file data received from client\n')
            file.close()
            conn.close()
            log.info('file successfully decrypted')
            log.info('client disconnected')
            log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] client disconnect\n')
            log_file.close()
            exit()

        # This excpetion is triggered when the file is not uploaded from the client
        except ValueError:
            log.info('Valid file not uploaded from Client Side')
            log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] Valid file not uploaded from Client Side\n')
            log_file.write('[' + datetime.now().strftime('%H:%M:%S')+'] client disconnect\n')
            exit()

# checking user and password credentials for server side initialization access        
user_ip = input('Enter Username: ').strip('\n')
pass_ip = getpass('Enter Password: ')
flag = 0
with open('names.csv',newline='') as csvreadfile:
    spamreader = csv.reader(csvreadfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        if user_ip == row[0] and pass_ip == row[1]:
            flag=1
if flag == 1:
    server_code()
else:
    log.info('Wrong Admin credentials Exiting!!')
            
            
                
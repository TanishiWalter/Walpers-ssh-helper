import paramiko
import json
from colorama import Fore
import logging
import time

#Just in case
print(Fore.RESET)

#ssh stuff
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connect(hostname,username,password,savePassword):
    if savePassword:
        try:
            ssh.connect(hostname=hostname,username=username,password=password)
        except Exception as e:
            logging.error(f"Could not connect. Check hostname and password. {e}")
        else:
            logging.info("Successfully connected!")
    else:
        password = input(Fore.GREEN + "Enter your password: ")
        try:
            ssh.connect(hostname=hostname,username=username,password=password)
        except Exception as e:
            logging.error(f"Could not connect. Check hostname and password. {e}")

        else:
            logging.info("Successfully connected!")

#json stuff
def getJson(path): 
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)
        return(data)

def writeItemsJson(path,itemToEditList): #Edits multiple items in a json file
    try:
        with open(path,"r+") as jsonFile:
            data = json.load(jsonFile)
            for i in itemToEditList:
                data[i[0]] = i[1]
            json.dump(data,jsonFile,indent=4)
            jsonFile.truncate()
    except Exception as e:
        logging.error(f"Failed to write into json file, error: {e}")

def writeJson(path,itemToEdit,newData): #Edits one item in a json file
    try:
        with open(path,"r+") as jsonFile:
            data = json.load(jsonFile)
            data[itemToEdit] = newData
            json.dump(data,jsonFile,indent=4)
            jsonFile.truncate()
    except Exception as e:
        logging.error(f"Failed to write into json file, error: {e}")

#Misc stuff 
def addServer():
    hostname = input(Fore.GREEN + "Enter hostname: ")
    useSavedPassword = input("Do you want to save password for this server [y/n]: ")
    username = input("Enter username: ")
    if useSavedPassword.lower() == "y":
        useSavedPassword = True
    else:
        useSavedPassword = False
    if useSavedPassword:
        password = input(f"What is the password for {username}")
    formatVar = getJson("src\programfiles\saveddata.json")
    formatVar["hostname"] = hostname
    formatVar["useSavedPassword"] = useSavedPassword
    formatVar["username"] = username
    formatVar["password"] = password
    writeJson("src\programfiles\saveddata.json",hostname,formatVar)

def mainMenu():
    inputVar = input("What do you want to do? \n [1] Connect to server \n [2] Add server \n [3] Exit \n")
    match inputVar:
        case 1:
            hostToConnect = input(Fore.GREEN + "The hostname of server you want to connect to: ")
            serverInfo = getJson("src\programfiles\saveddata.json")[hostToConnect]
            if serverInfo["useSavedPassword"]:
                connect(hostname=serverInfo["hostname"],username=serverInfo["username"],password=serverInfo["password"])
            else:
                passwordVar = input(Fore.GREEN + "useSavedPassword is set to false, you need to input password manualy: ")
                connect(hostname=serverInfo["hostname"],username=serverInfo["username"],password=passwordVar)
        case 2:
            addServer()
        case 3:
            print(Fore.RED + "Bye!")
            quit()

def getTime():
    t = time.localtime()
    current_time = time.strftime("%H-%Y-%H",t)
    return(current_time)

#logging stuff
logFileName = getJson("src\programfiles\config.json")["logpath"] + str(getTime()) + "-" + str(getJson("src\programfiles\config.json")["todaysLogs"] and ".log")
logging.basicConfig(filename=logFileName,encoding="utf-8",level=logging.DEBUG)
fileHandler = logging.FileHandler(logFileName)
fileHandler.setLevel(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)


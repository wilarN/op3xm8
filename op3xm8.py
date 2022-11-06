import random
import time
import os
from argparse import ArgumentError
from ast import arg
import socket
import subprocess
import sys
from datetime import datetime
import shutil
import json
from geolite2 import geolite2


globalLogPath = "./logs/globalLogFile.log"
globalLatestLogPath = "./logs/latest.log"
global_settings_path = "./settings.json"
now = datetime.now()


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def logOutput(msg, logType):
    # Log
    if logType == 1:
        # print("\n[ LOG ] " + msg)
        write_to_file("\n[LOG] " + msg, globalLogPath, "a+")
        write_to_file("\n[LOG] " + msg, globalLatestLogPath, "a+")
    # Error
    elif logType == 2:
        # print("\n[ ERROR ] " + msg)
        write_to_file("\n[ERROR] " + msg, globalLogPath, "a+")
        write_to_file("\n[ERROR] " + msg, globalLatestLogPath, "a+")
    # Warning
    elif logType == 3:
        # print("\n[ WARNING ] " + msg)
        write_to_file("\n[WARNING] " + msg, globalLogPath, "a+")
        write_to_file("\n[WARNING] " + msg, globalLatestLogPath, "a+")


def read_from_json(json_path: str):
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    json_file.close()
    return data

global interfaceToCaptureOn
global my_ip
global protocol

settings = {
    "_comment": "Settings Used with the geolocation module:",
    "log": False,
    "network_interface": "cH4nG3_tH1S",
    "self_local_ip": "cH4nG3_tH1S",
    "protocol_to_capture": "cH4nG3_tH1S"
}


def createGlobalLogFile():
    # Create Master Logs Dir
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    # Master Global Log File
    if not os.path.exists(globalLogPath):
        logFile = open(globalLogPath, "w+")
        logFile.close()

    # Json settings file
    if not os.path.exists(global_settings_path):
        json_settings = json.dumps(settings)

        with open("settings.json", "w") as jsonfile:
            jsonfile.write(json_settings)
        jsonfile.close()

    # Master Global Latest Log File
    if os.path.exists(globalLatestLogPath):
        os.remove(globalLatestLogPath)
    if not os.path.exists(globalLatestLogPath):
        logFile = open(globalLatestLogPath, "a+")
        logFile.close()


def write_to_file(text_to_write, path_to_file, typeOfWrite):
    if os.path.exists(path_to_file):
        write_file = open(path_to_file, typeOfWrite)
        write_file.write(text_to_write)
        write_file.close()



def get_lines(text_obj, output: bool):
    logo_lines = []
    if type(text_obj) == list:
        for line in text_obj[random.randint(0, len(text_obj)-1)].split("\n"):
            logo_lines.append(line)
    else:
        for line in text_obj.split("\n"):
            logo_lines.append(line)

    if output:
        for line in logo_lines:
            time.sleep(0.1)
            print(line)

global reader

def get_loc(ip):
    global reader
    location = reader.get(ip)

    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown Country"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown Subdivision"

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown City"

    return country, subdivision, city


global logging


def op3x_geolocate():

    createGlobalLogFile()

    usr_clr_sel = input("Would you like to clear previous session logs? [Y/y]\n")

    if usr_clr_sel.lower() == "Y" or usr_clr_sel.lower() == "y":
        if os.path.exists("./logs"):
            shutil.rmtree("./logs", ignore_errors=True)
            print("All previous logs cleared.")
            time.sleep(0.6)
            clear()

    createGlobalLogFile()

    interface_instructions = '''
    ###################################################################################
    ##         - To get your network information depending on your OS -              ##
    ##                - LINUX --> $~:       ifconfig -a                              ##
    ##                - WINDOWS --> $~:     ipconfig/all                             ##
    ##                - MAC --> $~: Honestly no fkn clue, guess ur out of luck lol.  ##
    ###################################################################################
    '''

    logging_reminder = '''
    ###################################################################################
    ##                 - To enable logging for your session -                        ##
    ##                - Edit the settings.json file in the .py file directory.       ##
    ###################################################################################
    '''

    global interfaceToCaptureOn
    global my_ip
    global logging
    global protocol
    global reader

    if os.path.exists('./settings.json'):
        data = read_from_json(global_settings_path)
        try:
            if data["network_interface"] == "cH4nG3_tH1S":
                print("Please Change The Targeted Network Interface...")
                get_lines(interface_instructions, True)
                time.sleep(1)
                interfaceToCaptureOn = "enp5s0"
                print(f"Defaulting to {interfaceToCaptureOn} as interface.")
                time.sleep(1)
                clear()
            elif data["network_interface"] == "":
                print("Targeted Network Interface can't be left empty...")
                time.sleep(1)
                interfaceToCaptureOn = "enp5s0"
                print(f"Defaulting to {interfaceToCaptureOn} as interface.")
                get_lines(interface_instructions, True)
                time.sleep(1)
                clear()
            else:
                interfaceToCaptureOn = data["network_interface"]
        except Exception as e:
            raise

        try:
            if data["self_local_ip"] == "cH4nG3_tH1S":
                print("Please Change The Local Ip Address To avoid log output from own system...")
                get_lines(interface_instructions, True)
                time.sleep(1)
                my_ip = "0.0.0.0"
                print(f"Defaulting to {my_ip} as local Ipv4.")
                time.sleep(1)
                clear()
            elif data["self_local_ip"] == "":
                print("Local IP can't be left empty...")
                time.sleep(1)
                my_ip = "0.0.0.0"
                print(f"Defaulting to {my_ip} as local Ipv4.")
                get_lines(interface_instructions, True)
                time.sleep(1)
                clear()
            else:
                my_ip = data["self_local_ip"]
        except Exception as e:
            raise

        try:
            if data["log"] == False:
                print("Logging is set to False, no logging to files will be activated for this session.")
                get_lines(logging_reminder, True)
                time.sleep(1)
                logging = False
                time.sleep(1)
            elif data["log"] == True:
                print("Logging Enabled in this session. All events will be logged to ´global.log´ and ´latest.log´ files.")
                time.sleep(1)
                logging = True
            else:
                pass
        except Exception as e:
            raise

        try:
            if data["protocol_to_capture"] == "cH4nG3_tH1S":
                print("Please Change The Targeted protocol in the ´settings.json´...")
                protocol = "UDP"
                time.sleep(5)
            elif data["protocol_to_capture"] == "":
                print("Protocol Can't be left empty please specify in the ´settings.json´.")
                protocol = "UDP"
                print(f"Defaulting to {protocol} as protocol.")
                time.sleep(1)
            else:
                protocol = data["protocol_to_capture"]
        except Exception as e:
            raise


    cmd = f"sudo tshark -i {interfaceToCaptureOn}"
    print(f"---------------------- Capturing on {interfaceToCaptureOn}. ----------------------")
    time.sleep(0.3)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(0.7)

    # my_ip = socket.gethostbyname(socket.gethostname())

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if logging == True:
        logOutput("-------------" + dt_string + "-------------", 3)
        write_to_file("-------------" + dt_string + "-------------", globalLatestLogPath, "w")
        write_to_file(dt_string, globalLatestLogPath, "w")
        logOutput(f"Capturing on protocol: ´{protocol}´", 1)
        print(f"Capturing on protocol: ´{protocol}´")
        print("\n[ WARNING ] " + "[ Logging to file activated... ]")
    elif logging == False:
        print("\n[ WARNING ] " + "[ Not logging to file... ]")
    else:
        print("\n[ ERR-WARN ] " + "[ Please Specify if logging should be enabled or not... ]")
    time.sleep(1)
    print("\n[ LOG ] " + "Local_IP: " + my_ip)
    if logging:
        logOutput(f"Local_IP = {my_ip}", 1)

    reader = geolite2.reader()

    for line in iter(process.stdout.readline, b""):
        columns = str(line).split(" ")

# CSGO P2P LOBBY VC--> CLASSIC-STUN or classicstun
        # UDP SELECTED (DEFAULT IF NOT SPECIFIED)

        # Custom protocol
        # PROGRAM            # PROTOCOL
        #if "TCP" in columns or "tcp" in columns:
        if protocol in columns or protocol.lower() in columns:
            if "->" in columns:
                src_ip = columns[columns.index("->") - 1]

            elif "→" in columns:
                src_ip = columns[columns.index("→") - 1]
            elif "\\xe2\\x86\\x92" in columns:
                src_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
            else:
                continue

            if "192" in src_ip:
                continue

            if src_ip == my_ip:
                continue

            try:
                country, sub, city = get_loc(src_ip)
                if logging:
                    logOutput(("<" + src_ip + "> " + country + ", " + sub + ", " + city), 1)
                print("<" + src_ip + "> " + country + ", " + sub + ", " + city)
            except:
                try:
                    real_ip = socket.gethostbyname(src_ip)
                    country, sub, city = get_loc(real_ip)
                    if logging:
                        logOutput(("<" + src_ip + "> " + ">>> " + country + ", " + sub + ", " + city), 1)
                    print("<" + src_ip + "> " + ">>> " + country + ", " + sub + ", " + city)
                except:
                    print("Not found")


op3x_text = ["""
                      /$$$$$$                           /$$$$$$ 
                     /$$__  $$                         /$$__  $$
  /$$$$$$   /$$$$$$ |__/  \\ $$ /$$   /$$ /$$$$$$/$$$$ | $$  \\ $$
 /$$__  $$ /$$__  $$   /$$$$$/|  $$ /$$/| $$_  $$_  $$|  $$$$$$/
| $$  \\ $$| $$  \\ $$  |___  $$ \\  $$$$/ | $$ \\ $$ \\ $$ >$$__  $$
| $$  | $$| $$  | $$ /$$  \\ $$  >$$  $$ | $$ | $$ | $$| $$  \\ $$
|  $$$$$$/| $$$$$$$/|  $$$$$$/ /$$/\\  $$| $$ | $$ | $$|  $$$$$$/
 \\______/ | $$____/  \\______/ |__/  \\__/|__/ |__/ |__/ \\______/ 
          | $$                                                  
          | $$                                                  
          |__/                                                  
""",
             """                                                                              
                            .x~~"*Weu.                                       u+=~~~+u.    
       u.    .d``          d8Nu.  9888c     uL   ..      ..    .     :     z8F      `8N.  
 ...ue888b   @8Ne.   .u    88888  98888   .@88b  @88R  .888: x888  x888.  d88L       98E  
 888R Y888r  %8888:u@88N   "***"  9888%  '"Y888k/"*P  ~`8888~'888X`?888f` 98888bu.. .@*   
 888R I888>   `888I  888.       ..@8*"      Y888L       X888  888X '888>  "88888888NNu.   
 888R I888>    888I  888I    ````"8Weu       8888       X888  888X '888>   "*8888888888i  
 888R I888>    888I  888I   ..    ?8888L     `888N      X888  888X '888>   .zf""*8888888L 
u8888cJ888   uW888L  888' :@88N   '8888N  .u./"888&     X888  888X '888>  d8F      ^%888E 
 "*888*P"   '*88888Nu88P  *8888~  '8888F d888" Y888*"  "*88%""*88" '888!` 88>        `88~ 
   'Y"      ~ '88888F`    '*8"`   9888%  ` "Y   Y"       `~    "    `"`   '%N.       d*"  
               888 ^        `~===*%"`                                        ^"====="`    
               *8E                                                                        
               '8>                                                                        
                "                                                                         
""",
             '''                             
                          ad888888b,                                   ad88888ba  
                         d8"     "88                                  d8"     "8b 
                                 a88                                  88       88 
                                ,88P                                  Y8a     a8P 
                              aad8"                                    "Y8aaa8P"  
   ,ggggg,    gg,gggg,        ""Y8,      ,gg,   ,gg  ,ggg,,ggg,,ggg,   ,d8"""8b,  
  dP"  "Y8ggg I8P"  "Yb         `88b    d8""8b,dP"  ,8" "8P" "8P" "8, d8"     "8b 
 i8'    ,8I   I8'    ,8i         "88   dP   ,88"    I8   8I   8I   8I 88       88 
,d8,   ,d8'  ,I8 _  ,d8' Y8,     a88 ,dP  ,dP"Y8,  ,dP   8I   8I   Yb,Y8a     a8P 
P"Y8888P"    PI8 YY88888P "Y888888P' 8"  dP"   "Y888P'   8I   8I   `Y8 "Y88888P"  
              I8                                                                  
              I8                                                                  
              I8                                                                  
              I8                                                                  
              I8                                                                  
              I8                                                                  
''',
             '''
                       .oooo.                                  .ooooo.   
                     .dP""Y88b                                d88'   `8. 
 .ooooo.  oo.ooooo.        ]8P' oooo    ooo ooo. .oo.  .oo.   Y88..  .8' 
d88' `88b  888' `88b     <88b.   `88b..8P'  `888P"Y88bP"Y88b   `88888b.  
888   888  888   888      `88b.    Y888'     888   888   888  .8'  ``88b 
888   888  888   888 o.   .88P   .o8"'88b    888   888   888  `8.   .88P 
`Y8bod8P'  888bod8P' `8bd88P'   o88'   888o o888o o888o o888o  `boood8'  
           888                                                           
          o888o                                                          
''',
             '''                                                                          
                           ad888888b,                                    ad88888ba   
                          d8"     "88                                   d8"     "8b  
                                  a8P                                   Y8a     a8P  
 ,adPPYba,   8b,dPPYba,        aad8"   8b,     ,d8  88,dPYba,,adPYba,    "Y8aaa8P"   
a8"     "8a  88P'    "8a       ""Y8,    `Y8, ,8P'   88P'   "88"    "8a   ,d8"""8b,   
8b       d8  88       d8          "8b     )888(     88      88      88  d8"     "8b  
"8a,   ,a8"  88b,   ,a8"  Y8,     a88   ,d8" "8b,   88      88      88  Y8a     a8P  
 `"YbbdP"'   88`YbbdP"'    "Y888888P'  8P'     `Y8  88      88      88   "Y88888P"   
             88                                                                      
             88                                                                      
''',
             '''                                                        
 @@@@@@   @@@@@@@   @@@@@@   @@@  @@@  @@@@@@@@@@    @@@@@@   
@@@@@@@@  @@@@@@@@  @@@@@@@  @@@  @@@  @@@@@@@@@@@  @@@@@@@@  
@@!  @@@  @@!  @@@      @@@  @@!  !@@  @@! @@! @@!  @@!  @@@  
!@!  @!@  !@!  @!@      @!@  !@!  @!!  !@! !@! !@!  !@!  @!@  
@!@  !@!  @!@@!@!   @!@!!@    !@@!@!   @!! !!@ @!@   !@!!@!   
!@!  !!!  !!@!!!    !!@!@!     @!!!    !@!   ! !@!   !!@!!!   
!!:  !!!  !!:           !!:   !: :!!   !!:     !!:  !!:  !!!  
:!:  !:!  :!:           :!:  :!:  !:!  :!:     :!:  :!:  !:!  
::::: ::   ::       :: ::::   ::  :::  :::     ::   ::::: ::  
 : :  :    :         : : :    :   ::    :      :     : :  :   
                                                              
''',
             '''
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄       ▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌ ▐░▌   ▐░▌ ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀█░▌
▐░▌       ▐░▌▐░▌       ▐░▌          ▐░▌  ▐░▌ ▐░▌  ▐░▌▐░▌ ▐░▌▐░▌▐░▌       ▐░▌
▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌   ▐░▐░▌   ▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄█░▌
▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌    ▐░▌    ▐░▌  ▐░▌  ▐░▌ ▐░░░░░░░░░▌ 
▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌   ▐░▌░▌   ▐░▌   ▀   ▐░▌▐░█▀▀▀▀▀▀▀█░▌
▐░▌       ▐░▌▐░▌                    ▐░▌  ▐░▌ ▐░▌  ▐░▌       ▐░▌▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄█░▌▐░▌           ▄▄▄▄▄▄▄▄▄█░▌ ▐░▌   ▐░▌ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░▌     ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀ 
''']

op3x_menu = '''
######################################################################
##                       - This Menu(H/h)                           ##
##                       - GeoIP (I/i)                              ##
##                       - This Menu(H/h)                           ##
##                       - This Menu(E/e/Q/q)                       ##
######################################################################
'''


def main():

    while True:
        clear()
        get_lines(op3x_text, True)
        get_lines(op3x_menu, True)

        usr_sel = input("~$: ")

        if usr_sel.lower() == "H" or usr_sel.lower() == "h":
            continue

        elif usr_sel.lower() == "I" or usr_sel.lower() == "i":
            clear()
            op3x_geolocate()
            input()

        elif usr_sel.lower() == "E" or usr_sel.lower() == "e" or usr_sel.lower() == "Q" or usr_sel.lower() == "q":
            clear()
            get_lines(op3x_text, True)
            print(" - Come back sometime, friend. - ")
            time.sleep(1)
            exit(0)

        else:
            print("Please Input A Valid Selection!")            
            time.sleep(1)


if __name__ == '__main__':
    main()

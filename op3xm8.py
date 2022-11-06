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


settings = {
    "log": False,
    "network_interface": "cH4nG3_tH1S",
}



def createGlobalLogFile():
    # Master Global Log File
    if not os.path.exists(globalLogPath):
        logFile = open(globalLogPath, "a+")
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



def get_loc(ip):
    location = reader.get(ip)

    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown"

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown"

    return country, subdivision, city


global logging


def op3x_geolocate():
    global interfaceToCaptureOn

    interfaceToCaptureOn = "enp5s0"

    if os.path.exists('./settings.json'):
        data = read_from_json(global_settings_path)
        try:
            if data["network_interface"] == "cH4nG3_tH1S":
                print("Please Change The Targeted Network Interface...")
        except Exception as e:
            raise


    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    createGlobalLogFile()

    interfaceToCaptureOn = read_from_json("./settings.json")

    cmd = f"sudo tshark -i {interfaceToCaptureOn}"
    print(f"---------------------- Capturing on {interfaceToCaptureOn}. ----------------------")
    time.sleep(1)
    print(" - Use argument ´-l // --log´ to log to a file. And ´-c // --clear´ to clear logs.")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    time.sleep(2)

    # my_ip = socket.gethostbyname(socket.gethostname())

    argument = str(sys.argv[1] if len(sys.argv) > 1 else '.')

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if argument == "-l" or argument == "--log":
        logging = True
        logOutput("-------------" + dt_string + "-------------", 3)
        write_to_file("-------------" + dt_string + "-------------", globalLatestLogPath, "w")
        write_to_file(dt_string, globalLatestLogPath, "w")
        print("\n[ WARNING ] " + "[ Logging to file activated... ]")
        # logOutput("[ Logging to file activated... ]", 3)
    elif argument == "-c" or argument == "--clear":
        if os.path.exists("./logs"):
            shutil.rmtree("./logs", ignore_errors=True)
        logging = False
        print("Deleted all logs and exited with code 0.")
        exit(1)
    else:
        logging = False
        print("\n[ WARNING ] " + "[ Not logging to file... ]")
        # logOutput("[ Not logging to file... ]", 3)

    time.sleep(1)

    my_ip = "192.168.1.72"
    print("\n[ LOG ] " + "Local_IP: " + my_ip)
    if logging:
        logOutput(f"Local_IP = {my_ip}", 1)

    reader = geolite2.reader()







op3x_text = ["""
                      /$$$$$$                           /$$$$$$ 
                     /$$__  $$                         /$$__  $$
  /$$$$$$   /$$$$$$ |__/  \ $$ /$$   /$$ /$$$$$$/$$$$ | $$  \ $$
 /$$__  $$ /$$__  $$   /$$$$$/|  $$ /$$/| $$_  $$_  $$|  $$$$$$/
| $$  \ $$| $$  \ $$  |___  $$ \  $$$$/ | $$ \ $$ \ $$ >$$__  $$
| $$  | $$| $$  | $$ /$$  \ $$  >$$  $$ | $$ | $$ | $$| $$  \ $$
|  $$$$$$/| $$$$$$$/|  $$$$$$/ /$$/\  $$| $$ | $$ | $$|  $$$$$$/
 \______/ | $$____/  \______/ |__/  \__/|__/ |__/ |__/ \______/ 
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
____ ____ ____ ____ ____ ____ 
||o |||p |||3 |||x |||m |||8 ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|
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
     _        _        _        _        _        _    
   _( )__   _( )__   _( )__   _( )__   _( )__   _( )__ 
 _|     _|_|     _|_|     _|_|     _|_|     _|_|     _|
(_ O _ (_(_ P _ (_(_ 3 _ (_(_ X _ (_(_ M _ (_(_ 8 _ (_ 
  |_( )__| |_( )__| |_( )__| |_( )__| |_( )__| |_( )__|
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
########################################
##        - This Menu(H/h)            ##
##        - GeoIP (I/i)                ##
##        - This Menu(H/h)            ##
##        - This Menu(E/e/Q/q)        ##
########################################
'''


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


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


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

        else:
            print("Please Input A Valid Selection!")            
            time.sleep(1)


if __name__ == '__main__':
    main()

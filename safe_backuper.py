'''
run:
python3 .../safe_backuper.py original_path backup_path (repeat_flag)
'''

import codecs
from tkinter import Tk,messagebox
from random import randint
import os
from sys import argv
from time import sleep
import datetime

TEST_FILE_NAME = "backuper_for_linux.txt"
NAME_FOR_MESSAGEMOX = "backuper_for_linux"
DATETIME_BACKUP_DAY = 5 #20
DATETIME_BACKUP_HOUR = 17  #3

window = Tk()
window.withdraw()

def testDisk(test_catalog):

    def myMessagebox(line):
        messagebox.showerror(NAME_FOR_MESSAGEMOX,"ERROR: " + line + " - " + test_catalog)

    def openFile(path,key='r'):
        #path = str(os.path.dirname(os.path.abspath(__file__))) + "/" + path
        file = 0
        for a in ['utf-8','unicode','ansi']:
            try: 
                file = codecs.open(path, key, a)
                if key!='w': b = file.readlines()
                file.close()
                file = codecs.open(path, key, a)
                return file
            except UnicodeDecodeError: pass   
            except LookupError: pass
        # print("ERROR: unknow file format")
        myMessagebox("неизвестный кодек файла")
        return None
    
    def generateKey(leight=32):
        key_dictionary = "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
        key = ""
        for i in range(leight):
            key += key_dictionary[randint(0, len(key_dictionary)-1)]
        return key
    
    if not os.path.isdir(test_catalog):
        myMessagebox("этого каталога не существует")
        return None
    test_file_catalog = test_catalog + "/" + TEST_FILE_NAME
    try:
        # write
        file = openFile(test_file_catalog,'w')
        key = generateKey()
        file.write(key)
        file.close()
        # read
        file = openFile(test_file_catalog,'r')
        if file.readlines()!=[key]:
            myMessagebox("тестовый файл прочитан неверно")
            return None
        file.close()
        return True
    except: myMessagebox("неизвестная ошибка при тестировании диска")
    return False

def backupDisk(original_disk, backup_disk):
    if testDisk(original_disk):
        if testDisk(backup_disk):
            # backupDisk(original_disk,backup_disk)
            print("test backupDisk")

if __name__ == "__main__":
    try:
        print(argv)
        if len(argv)<3: # develop
            print("WARNING: develop mode, NOT BACKUP")
            testDisk("test")
        else:
            if len(argv)>3:
                while True:
                    # wait new backup
                    while datetime.datetime.now().day!=DATETIME_BACKUP_DAY or datetime.datetime.now().hour!=DATETIME_BACKUP_HOUR:
                        sleep(900)
                        # print("x")
                    backupDisk(argv[1],argv[2])
                    sleep(3600)
            else: backupDisk(argv[1],argv[2])
                
    except KeyboardInterrupt: print("OFF")

    
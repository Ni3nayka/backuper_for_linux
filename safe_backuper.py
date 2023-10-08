'''
run:
python3 .../safe_backuper.py original_path backup_path (repeat_flag, backup_day=20, backup_hour=3)
repeat_flag = 0 - делать копирование в день и час указанный в следующих аргументах
repeat_flag > 0 - делать копирование раз в n секунд
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
DATETIME_BACKUP_DAY = 20
DATETIME_BACKUP_HOUR = 3

window = Tk()
window.withdraw()

def myMessagebox(line,path=""):
    if path!="": path = "\n" + path
    messagebox.showerror(NAME_FOR_MESSAGEMOX,"ERROR: " + line + path)

def testDisk(test_catalog):

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
        myMessagebox("неизвестный кодек файла",test_catalog)
        return None
    
    def generateKey(leight=32):
        key_dictionary = "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
        key = ""
        for i in range(leight):
            key += key_dictionary[randint(0, len(key_dictionary)-1)]
        return key
    
    if not os.path.isdir(test_catalog):
        myMessagebox("этого каталога не существует",test_catalog)
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
            myMessagebox("тестовый файл прочитан неверно",test_catalog)
            return None
        file.close()
        return True
    except: myMessagebox("неизвестная ошибка при тестировании диска",test_catalog)
    return False

def backupDisk(original_path, backup_path):
    # https://losst.pro/rsync-primery-sinhronizatsii
    # https://tokmakov.msk.ru/blog/item/445
    # https://pythononline.ru/osnovy/sistemnye-komandy-s-pomoschyu-python-os-system
    if testDisk(original_path):
        if testDisk(backup_path):
            print(datetime.datetime.now().strftime("%Y.%m.%d - %H:%M:%S"),"\nSTART OPERATING")
            backup = os.system(f"rsync -azh --delete --progress {original_path} {backup_path}")
            print("END OPERATING\n")
            if backup!=0: 
                myMessagebox("неизвестная ошибка при копировании диска")
                return False
            return True
            
if __name__ == "__main__":
    try:
        # print(argv)
        if len(argv)<3: # develop
            print("WARNING: develop mode, NOT BACKUP")
            testDisk("test")
        else:
            print("original path:",argv[1])
            print("backup path:",argv[2])
            if len(argv)>3:
                # настройка режима бекапа
                dt = int(argv[3])
                wait_flag = True
                if dt<=0: 
                    dt = 4000 # чуть больше часа, чтобы не бекапить 1 час после него
                    # настройка даты и времени бекапа
                    try:
                        DATETIME_BACKUP_DAY = int(argv[4])
                        DATETIME_BACKUP_HOUR = int(argv[5])
                    except: pass
                    print("РЕЖИМ: копирования раз в месяц:")
                    print("число:",DATETIME_BACKUP_DAY)
                    print("час:",DATETIME_BACKUP_HOUR)
                else: 
                    wait_flag = False
                    print("РЕЖИМ: копирования раз в N секунд:",dt)
                print()
                while True:
                    if wait_flag:
                        while datetime.datetime.now().day!=DATETIME_BACKUP_DAY or datetime.datetime.now().hour!=DATETIME_BACKUP_HOUR:
                            sleep(900) # 15 мин
                    backupDisk(argv[1],argv[2])
                    sleep(dt)
            else: 
                print("РЕЖИМ: одиночное копирование\n")
                backupDisk(argv[1],argv[2])
                print("press ctrl+C")
                sleep(9999)
    except KeyboardInterrupt: print("OFF")
    except Exception as err:
        myMessagebox(f"Unexpected {err=}, {type(err)=}")
        print("UNKNOW ERROR")
        raise

    
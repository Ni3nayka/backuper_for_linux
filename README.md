# backuper_for_linux
backuper_for_linux - a set of scripts for planned and actual data backup for linux OS

## Setup:
```
sudo apt install rsync
sudo apt install python3-pip
sudo apt install python3-tk
```
## guide:
```
python3 .../safe_backuper.py original_path backup_path (repeat_flag, backup_day=20, backup_hour=3)
repeat_flag = 0 - делать копирование в день и час указанный в следующих аргументах
repeat_flag > 0 - делать копирование раз в n секунд
# сделать копию один раз
python3 ../safe_backuper.py ../1 ../2
# делать копию раз в N секунд (пусть будет 5 секунд)
python3 ../safe_backuper.py ../1 ../2 5
# делать копию раз в месяц (по умолчанию: 20 числа в 3 часа)
python3 ../safe_backuper.py ../1 ../2 0
# делать копию раз в месяц (например: 15 числа в 20 часов)
python3 ../safe_backuper.py ../1 ../2 0 15 20
```

## example 2:
`rsync -azh —delete /mnt/0a3c64bf-a6f1-464b-bfb3-bc15b097ec71 /mnt/7f4c9d39-95db-4a02-8f1e-9c1e0ec4cf2e`

## lync:
https://losst.pro/rsync-primery-sinhronizatsii
https://tokmakov.msk.ru/blog/item/445

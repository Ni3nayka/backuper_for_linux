import codecs
from tkinter import messagebox

def open_file(path,key='r'):
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
    print("ERROR: unknow file format")
    messagebox.showerror('file error',"ERROR: unknow file codecs")
    return None

def test_disk(test_catalog):
    pass

if __name__ == "__main__":
    test_disk("test/test")
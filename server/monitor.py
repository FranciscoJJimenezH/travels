# -*- coding: utf-8 -*-

import sys
import json
import time 

from copy import deepcopy
from UX import UX

from pymongo import MongoClient
from bson.objectid import ObjectId
import subprocess
import json

class MonitorManager:
    
    def __init__(self, dbname, tp, unit_id):
        self.dbname = dbname
        self.tp = tp       
        self.unit_id = unit_id
      
    @classmethod
    def new_register(cls, unit_id):
        global UNIT_ID
        UNIT_ID = unit_id
        subprocess.Popen([f"gnome-terminal -- python3 monitor.py {UNIT_ID}"], shell=True)
        
        with open(f'unit{UNIT_ID}.json', 'w') as file:
            json.dump([], file)
    
    @classmethod
    def remove_register(self):
        subprocess.Popen([f"rm -fr unit{self.unit_id}.json"], shell=True)
        
    def add_register(self, e=[]):
        reg = [{'dbname': self.dbname, 'tp': self.tp}, 'DONE']
        if e:
            reg[0]['e'] = e
            reg[1] = 'ERROR'
        
        try:
            with open(f'unit{self.unit_id}.json', "r+") as file:
                data = json.load(file)
                data.append(reg)
                file.seek(0)
                json.dump(data, file)
        except Exception: pass
        
    def __call__(self, action):
        
        def wrapper(*args, **kwargs):
            client = MongoClient('mongodb://localhost:27017')
            db = client[self.dbname]
            ar = None
            try:
                ar = action(*args, **kwargs, db=db)
                self.add_register()
                
            except Exception as e: self.add_register(e)
                
            client.close()
            return ar
        
        return wrapper

def unit_monitor():
    
    UNIT_ID = int(sys.argv[1])
    sys.stdout.write(f'\x1b]2;DATABASE REGISTER UNIT[{UNIT_ID}]\x07')
    
    while 1:
        register = []
        try:
            with open(f'unit{UNIT_ID}.json') as file:
                register = json.load(file)
            
            if len(register) !=0:
                reg_copy = deepcopy(register)
                
                for ri,r in enumerate(reg_copy):
                    if r[1] == 'ERROR':
                        UX().error_msg('db', r[0]['dbname'], r[0]['tp'], r[0]['e'])
                    else:
                        UX().done_msg('db', r[0]['dbname'], r[0]['tp'])
                
                with open(f'unit{UNIT_ID}.json', 'w') as file:
                    json.dump([], file, indent=4)
        except Exception as e:
            
            if type(e) == FileNotFoundError:
                UX().finish_msg('db', '--terminal--', 'KILLED')
                time.sleep(5)
                break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        unit_monitor()
    else:
        MonitorManager(sys.argv[0],sys.argv[1], sys.argv[2])
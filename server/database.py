# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
import subprocess
import asyncio

class DBManager:
    
    def __init__(self, dbname, tp):
        self.dbname = dbname
        self.tp = tp       
        
    async def __call__(self, action):
        
        def wrapper(*args, **kwargs):
            client = MongoClient('mongodb://localhost:27017')
            db = client[self.dbname]
            ar = None
            try:
                ar = await action(*args, **kwargs, db=db)
                
            except Exception as e: pass
                
            client.close()
            return ar
        
        return wrapper

class Account:
    
    async def update_info(self, db, user):
        pass
    
    async def register(self, db, user):
        pass
    
    async def login(self, db, user):
        pass
    
    async def logout(self, db, user):
        pass
    
    
class Travels:
    
    @DBManager
    @classmethod
    async def getnewtravelid(self, db, user):
        pass
    
    @DBManager
    @classmethod
    async def upload_travel(self, db, user):
        pass
    
    @DBManager
    @classmethod
    async def upload_travel(self, db, user):
        pass
    
    @DBManager
    @classmethod
    async def update_travel(self, db, user, travel_id):
        pass
    
    @DBManager
    @classmethod
    async def get_travel(self, db, user, travel_id):
        pass
    
    @DBManager
    @classmethod
    async def get_travels(self, db, user):
        pass
    
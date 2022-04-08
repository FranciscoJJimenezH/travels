# -*- coding: utf-8 -*-

from gurobipy import *

from dataclasses import dataclass, field
from collections import Counter, ChainMap
from enum import Enum, auto

import database
import ayncio

class TravelType(Enum):
    
    LOCATION: auto()
    COST_IN: auto()
    COST_DISTANCE: auto()
    DISTANCE_FROM_POINT: auto()
    
@dataclass
class Schedule:
    
    schedule_data: dict
    schedule_id: int = filed(init=False)
    
    def __post_init__(self):
        self.shedule_id = database.Travels.new_schedule(schedule_data)
    
    async def update_schedule(self, schedule_info: dict) -> bool:
        req = await database.Travels.update_schedule_info(schedule_id)
        return req
        
@dataclass
class Travels:
    
    schedule_id: int
    travel_id: bool = field(init=False)
    trave_type: TravelType
    
    async def __post_init__(self):
        self.travel_id = await database.Travels.getnewtravelid(shedule_id)
    
    @classmethod
    async def new_travel(cls,schedule_id: int, travel_type: TravelType) -> tuple:
        req = await database.Travels.new_travel(schedule_id, travel_type)
        
        if req:
            new_travel = cls(travel_type)
            return req, new_travel
        return req,
    
    @classmethod
    async def update_travel(cls, schedule_id: int, travel_id: int) -> bool:
        req = await database.Travels.update_travel(schedule_id, travel_id)
        return req
    
    @classmethod
    async def remove_travel(cls, schedule_id: int, travel_id: int) -> bool:
        req = await database.Travels.remove_travel(schedule_id, travel_id)
        return req
    
    def add_restriction(cls):
        pass
    
    def update_restricion(cls):
        pass
        
    @classmethod
    async def optimizate(cls, schedule_id: int) -> bool:
           
        m = Model('travels')
        
        I = range(1,4)
        J = range(1,3) 
        
        Z = [0.025,0.02,0.015]
        V = [0.022,0.02] 
        
        X = [(i, j) for j in J for i in I]
        x = m.addVars(X, vtype=GRB.CONTINUOUS, name='x')
        
        m.addConstr(x[1,1] + x[1,2] <= 20000)
        m.addConstr(x[2,1] + x[2,2] <= 25000)
        m.addConstr(x[3,1] + x[3,2] <= 15000)
        
        m.addConstr(x[1,1] + x[2,1] + x[3,1] >= 35000)
        m.addConstr(x[1,2] + x[2,2] + x[3,2] >= 25000)
        
        m.addConstr(quicksum(((Z[i-1]*x[i,1])) for i in I) <= 2.2 * (x[1,1] + x[2,1] + x[3,1]))
        m.addConstr(quicksum(((Z[i-1]*x[i,2])) for i in I) <= 2.0 * (x[1,2] + x[2,2] + x[3,2]))
        
        m.setObjective(
            72*(x[1,1]+x[2,1]+x[3,1])
            +75*( x[1,2] + x[2,2] + x[3,2])
            -52*(x[1,1] + x[1,2])
            -50*(x[2,1] + x[2,2])
            -48*(x[3,1] + x[3,2]),GRB.MAXIMIZE)
        
        m.optimize()
        
        req = await database.Travels.update_optimization(schedule_id, data={
            'obj_function': str(round(m.objVal, 2)),
            'vars': m.getVars()
        })
        return req

        # print('-------------------------------------------')
        # print(f'Funcion objetivo: {str(round(m.objVal, 2))}')
        # print()
        # for v in m.getVars():
        #     print(f'\t +{str(v.VarName)} = {str(round(v.x,2))}')
from dataclasses import dataclass,field
from importlib import import_module
from typing import AnyStr,Any,Union,List,Dict
import yaml
import pandas as pd
import json
from create_db import fetchSqlite

DATA_BASE = 'db.yaml'

def retrive_yaml_data(file=DATA_BASE)->None:
    data = {}
    with open(file) as f:
        data=yaml.safe_load(f)
    return data

def write_yaml_data(data,file=DATA_BASE)->None:
    with open(file,'w') as f:
        yaml.dump(data,f)

@dataclass
class Handler:
    data:Dict = field(default_factory=lambda:dict())
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Handler, cls).__new__(cls)
        return cls.instance

    def __post_init__(self):
        # self.data = retrive_yaml_data()
        self.data = fetchSqlite['name']

    def refreshData(self)->List[str]:
        write_yaml_data(self.data)
        self.data = retrive_yaml_data()
        self.totalNumber(showText=True)
        self.showAllStudents()

    def totalNumber(self,showText=None)->Union[None,int]:
        currentNumber = len(self.data['students']['name'])
        document.getElementById("total").textContent= f"Total {currentNumber} students" if showText else currentNumber
    
    def showAllStudents(self,*args,**kargs)-> None:
        elements = document.getElementById("studentList").getElementsByTagName("li")
        exist = [str(x.textContent) for x in elements]
        for e in self.data['students']['name']:
            if e not in exist:
                node = document.createElement("li")
                node.setAttribute("class", "list-group-item")
                node.appendChild(document.createTextNode(e))
                document.getElementById("studentList").appendChild(node)
    
    def addStudent(self,*args,**kargs)-> None:
        inputName = document.getElementById("inputName").value
        self.data['students']['name'].append(str(inputName))
        self.refreshData()
    

def clearInput(*args,**kargs)->None:
    document.getElementById('inputName').value = ''

def actionPost(*ags, **kws):
    Handler().addStudent()
    
if __name__=='__main__':

    # write_yaml_data({'students':{'name':['Mary','Andy']}})
    h = Handler()
    h.totalNumber(showText=True)
    h.showAllStudents()



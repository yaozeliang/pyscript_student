from dataclasses import dataclass,field
from importlib import import_module
from typing import AnyStr,Any,Union,List,Dict
import yaml
import json

DATA_BASE = 'db.yaml'

@dataclass
class Handler:

    students: list[str] = field(default_factory=list)
    tmpData = {"students":{"name":[]}}
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Handler, cls).__new__(cls)
        return cls.instance

    def __post_init__(self):
        self.getData()

    def getData(self)-> List[str]:
        with open(DATA_BASE) as f:
            self.tmpData["students"]["name"]=yaml.safe_load(f)["students"]["name"]

    def refreshData(self)->List[str]:
        print(self.tmpData["students"]["name"])
        with open(DATA_BASE,'w') as f:
            yaml.dump(self.tmpData, f,default_flow_style=False)
            
        self.getData()
        self.totalNumber(showText=True)
        self.showAllStudents()
        
    
        
    def totalNumber(self,showText=None)->Union[None,int]:
        if showText:
            document.getElementById("total").textContent= f'Total {len(self.tmpData["students"]["name"])} students'
        else:
            return len(self.tmpData["students"]["name"])


    def showAllStudents(self,*args,**kargs)-> None:

        elements = document.getElementById("studentList").getElementsByTagName("li")
        exist = [str(x.textContent) for x in elements]
        print(exist)
        for e in tuple(self.tmpData['students']['name']):
            if e not in exist:
                node = document.createElement("li")
                node.setAttribute("class", "list-group-item")
                node.appendChild(document.createTextNode(e))
                document.getElementById("studentList").appendChild(node)
    
    def addStudent(self,*args,**kargs)-> None:
        inputName = document.getElementById("inputName").value
        self.tmpData['students']['name'].append(inputName)
        self.refreshData()
    


def clearInput(*args,**kargs)->None:
    document.getElementById('inputName').value = ''



def actionPost(*ags, **kws):
    Handler().addStudent()

  

if __name__=='__main__':
    h = Handler()
    h.totalNumber(showText=True)
    h.showAllStudents()




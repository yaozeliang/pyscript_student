from dataclasses import dataclass,field
from importlib import import_module
from typing import AnyStr,Any
import yaml

DATA_BASE = 'db.yaml'

@dataclass
class Handler:
    db = DATA_BASE
    students: list[str] = field(default_factory=list)
    def __post_init__(self):
        with open(self.db) as file:
            self.students = yaml.safe_load(file)['students']['name']
    
    def getTotalNumber(self):
        return len(self.students)

    def getAllStudents(self):
        for e in self.students:
            node = document.createElement("li")
            node.setAttribute("class", "list-group-item")
            node.appendChild(document.createTextNode(e))
            document.getElementById("studentList").appendChild(node)

def createStudent(*args,**kargs) -> None:
    node = document.createElement("li")
    node.setAttribute("class", "list-group-item")
    inputName = str(document.getElementById("inputName").value)
    node.appendChild(document.createTextNode(inputName))
    document.getElementById("studentList").appendChild(node)



h = Handler()
document.getElementById("total").textContent= f"Total {h.getTotalNumber()} students"
h.getAllStudents()
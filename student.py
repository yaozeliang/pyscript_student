from dataclasses import dataclass,field
from typing import AnyStr

@dataclass
class Handler:
    name: AnyStr =''
    students: list[str] = field(default_factory=list)



def createStudent(*args,**kargs) -> None:
    node = document.createElement("li")
    node.setAttribute("class", "list-group-item")
    inputName = str(document.getElementById("inputName").value)
    node.appendChild(document.createTextNode(inputName))
    document.getElementById("studentList").appendChild(node)



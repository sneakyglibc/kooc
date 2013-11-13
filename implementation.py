from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration
from call import Call
from print_error import print_error

implement = {"name":"", "type":""}
save = ""

class   Implementation(Grammar, Declaration):

    entry = "implementation"
    grammar =   """
                implementation ::=
                        ["@implementation" Base.id:n #is_imp(n) "{"
                        [
                               [ [declaration |
                                ["@member" #is_member declaration] |
                                ["@member" "{" #is_member declaration* "}"]
                                ]#not_member
                               ]*
                        ]
                "}"] #not_imp
                ;
                """
@meta.hook(Implementation)
def is_member(self):
    global implement
    if implement["type"] != "C":
        print_error("Error @member in module")
        return False
    implement["type"] = "CM"
    return True

@meta.hook(Implementation)
def not_member(self):
    global implement, save
    implement["type"] = save
    return True

@meta.hook(Implementation)
def is_imp(self, name):
    global implement, save
    from kooc import mlist, clist
    global mlist
    global clist
    if name.value in mlist:
        implement["type"] = "M"
        save = "M"
    elif name.value in clist:
        implement["type"] = "C"
        save = "C"
    else:
        print_error("Error module not declared : " + name.value)
        return False
    implement["name"] = name.value
    return True

@meta.hook(Implementation)
def not_imp(self):
    global implement
    implement = {"name":"", "type":""}
    return True


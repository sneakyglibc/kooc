from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration
from call import Call
from print_error import print_error

implement = {"name":"", "type":""}

class   Implementation(Grammar, Declaration):

    entry = "implementation"
    grammar =   """
                implementation ::=
                        ["@implementation" Base.id:n #is_imp(n) "{"
                        declaration*
                "}"] #not_imp
                ;
                """
@meta.hook(Implementation)
def is_imp(self, name):
    global implement
    from kooc import mlist, clist
    if name.value in mlist:
        implement["type"] = "M"
    elif name.value in clist:
        implement["type"] = "C"
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


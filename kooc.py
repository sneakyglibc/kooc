from pyrser import meta, directives
from pyrser.passes import to_yml
from pyrser.hooks import copy, echo
from pyrser.parsing.node import Node
from cnorm import nodes
from pyrser.grammar import Grammar
from cnorm.parsing.declaration import Declaration
from cnorm.parsing.expression import Idset
from weakref import ref
import sys
from cnorm.passes import to_c
from module_import import Import
from module import Module
from module_class import Mclass
from call import Call
from implementation import Implementation
from drecovery import Drecovery
import dumbXml
import mangle

mlist = {}
clist = {}
slist = {}
glist = {"__global__":[]}
ilist = []


class   Kooc(Grammar, Call, Drecovery, Declaration, Import, Module, Mclass, Implementation):
    entry = "kooc"
    grammar = """
        kooc ::=
            @ignore("C/C++")
            [
                "":current_block
                #new_root(_, current_block)
                [ [declaration] |
                  [Import.import:imp #add_import(_, imp)] |
                  [Module.module:mod #add_module(_, mod)] |
                  [Mclass.class:cl #add_cl(_, cl)] |
                  [Implementation.implementation]
                ]*
            ]
            Base.eof
        ;
"""

@meta.hook(Kooc)
def add_import(self, ast, ret):
    if ret.nimport != None:
        ast.node.body.extend(ret.nimport.node.body)
    return True

@meta.hook(Kooc)
def add_imp(self, ast, ret):
    global clist
    global mlist
    ttype = ""
    if ret.mname in mlist:
        ttype = "M"
    if ret.mname in clist:
        ttype = "C"
    if ttype == "":
        print("Error module or class not declared : " + ret.mname)
        return False
    for item in ret.node.body:
        mangle.mangle(item, ret.mname, ttype)
    ast.node.body.extend(ret.node.body)
    return True

@meta.hook(Kooc)
def add_cl(self, ast, ret):
    from cnorm import nodes
    global clist
    global mlist
    if ret.mname in mlist:
        print("Error module or class already declared : " + ret.mname)
        return False
    if not ret.mname in clist:
        clist[ret.mname] = []
    for item in ret.node.body:
        clist[ret.mname].append(mangle.mangle(item, ret.mname, "C"))
    ast.node.body.extend(ret.node.body)

    st = nodes.Decl("")
    st._ctype = nodes.ComposedType(ret.mname)
    st._ctype._specifier = 1
    st._ctype.fields = []
    ast.node.body.append(st)
    return True

@meta.hook(Kooc)
def add_module(self, ast, ret):
#    print(ret.node.to_dxml())
    global mlist
    global clist
    if ret.mname in clist:
        print("Error module or class already declared : " + ret.mname)
        return False
    if not ret.mname in mlist:
        mlist[ret.mname] = []
    for item in ret.node.body:
        mlist[ret.mname].append(mangle.mangle(item, ret.mname, "M"))
    ast.node.body.extend(ret.node.body)
    return True

@meta.hook(Kooc)
def printvalue(self):
    print(ilist)
    print(mlist)
    return True

@meta.hook(Kooc)
def printnode(self, ast):
    print(ast.node)
    return True


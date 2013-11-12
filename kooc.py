from pyrser import meta, directives
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
import mangle
from print_error import print_error

class   Kooc(Grammar, Call, Drecovery, Declaration, Import, Mclass, Module, Implementation):
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

mlist = {}
clist = {}
slist = {}
glist = {"__global__":[]}
ilist = []
vlist = {}

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
        print_error("Error module or class not declared : " + ret.mname)
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
    global vlist

    if ret.mname in mlist or ret.mname in clist:
        print_error("Error module or class already declared : " + ret.mname)
        return False
    if not ret.mname in clist:
        clist[ret.mname] = []
    for item in ret.node.body:
        clist[ret.mname].append(mangle.mangle(item, ret.mname, "C"))
    ast.node.body.extend(ret.node.body)

    test = "<class \'cnorm.nodes.FuncType\'>"
    private_var = [item for item in ret.private.body if str(type(item._ctype)) != test]
    private_func = [item for item in ret.private.body if str(type(item._ctype)) == test]

    if not hasattr(slist, ret.mname):
        slist[ret.mname] = []
    for item in private_var:
        slist[ret.mname].append(mangle.mangle(item, ret.mname, "CM"))
    st = nodes.Decl(ret.mname)
    st._ctype = nodes.ComposedType(ret.mname)
    st._ctype._specifier = 1
    st._ctype._storage = 2
    st._ctype.fields = private_var
    ast.node.body.append(st)

    if not hasattr(vlist, ret.mname):
        vlist[ret.mname] = []
    for item in private_func:
        vlist[ret.mname].append(mangle.mangle(item, ret.mname, "CM"))
        item._name = "(*" + item._name + ")"
    st = nodes.Decl("vtable_" + ret.mname)
    st._ctype = nodes.ComposedType("vtable_" + ret.mname)
    st._ctype._specifier = 1
    st._ctype._storage = 2
    st._ctype.fields = private_func
    ast.node.body.append(st)

    parse = Declaration()
    cl = ret.mname
    vt = "vtable_" + ret.mname
    dl = "struct " + ret.mname + " *K_C_new_"
    code = vt + " *ptr = (struct " + vt + " *) malloc(sizeof(struct " + cl + ") + sizeof(struct " + vt + ")); ptr->func = &func; return (struct " + ret.mname + " *)(ptr + sizeof(struct " + vt + "));"
    new = dl + ret.mname + "(){" + code + "}"    
    free = "void delete(struct " + cl + " *obj) { void *fr = (void*)(obj - sizeof(struct " + vt + ")); free(fr);}"
    mal = parse.parse(new + "\n" + free)
    ast.node.body.extend(mal.body)
    return True

@meta.hook(Kooc)
def add_module(self, ast, ret):
#    print(ret.node.to_dxml())
    global mlist
    global clist
    if ret.mname in clist:
        print_error("Error module or class already declared : " + ret.mname)
        return False
    if not ret.mname in mlist:
        mlist[ret.mname] = []
    for item in ret.node.body:
        mlist[ret.mname].append(mangle.mangle(item, ret.mname, "M"))
    ast.node.body.extend(ret.node.body)
    return True


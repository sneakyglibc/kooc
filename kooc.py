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
from mangle import mangle
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
    from copy import deepcopy
    global clist
    global mlist
    global vlist

    if ret.mname in mlist or ret.mname in clist:
        print_error("Error module or class already declared : " + ret.mname)
        return False
    if not ret.mname in clist:
        clist[ret.mname] = []
    for item in ret.node.body:
        clist[ret.mname].append(mangle(item, ret.mname, "C"))
    ast.node.body.extend(ret.node.body)

    test = "<class \'cnorm.nodes.FuncType\'>"
    private_var = [item for item in ret.private.body if str(type(item._ctype)) != test]
    private_func = [item for item in ret.private.body if str(type(item._ctype)) == test]

    if not hasattr(slist, ret.mname):
        slist[ret.mname] = []
    for item in private_var:
        slist[ret.mname].append(mangle(item, ret.mname, "CM"))
    st = nodes.Decl(ret.mname)
    st._ctype = nodes.ComposedType(ret.mname)
    st._ctype._specifier = 1
    st._ctype._storage = 2
    st._ctype.fields = private_var
    ast.node.body.append(st)

    if not hasattr(vlist, ret.mname):
        vlist[ret.mname] = []
    parse = Declaration()
    nod = parse.parse("struct " + ret.mname + " * self;");
    for item in private_func:
        vlist[ret.mname].append(mangle(item, ret.mname, "CM"))
        item._name = "(*" + item._name + ")"
        item._ctype._params.append(nod.body[0])
    st = nodes.Decl("vtable_" + ret.mname)
    st._ctype = nodes.ComposedType("vtable_" + ret.mname)
    st._ctype._specifier = 1
    st._ctype._storage = 2
    st._ctype.fields = private_func
    ast.node.body.append(st)

    parse = Declaration()
    cl = ret.mname
    vt = "vtable_" + cl    

    free = "void delete() { void *fr = (void*)(self - sizeof(struct " + vt + ")); free(fr);}"
    d_free = parse.parse(free)
    m_free = mangle(d_free.body[0], cl, "CM")
    vlist[cl].append(m_free)
    free = "void delete(struct " + cl + " *self) { void *fr = (void*)( ((struct " + vt + " *)(self)) - 1); free(fr);}"
    d_free = parse.parse(free)
    d_free.body[0]._name = m_free["mangle"]
    ast.node.body.append(d_free.body[0])
    tmp = deepcopy(d_free)
    tmp.body[0]._name = "(*" + tmp.body[0]._name + ")"
    tmp.body[0].body = None
    st._ctype.fields.append(tmp.body[0])

    ptr_func = ""
    for item in vlist[cl]:
        ptr_func += "ptr->" + item["mangle"] + " = &" + item["mangle"] + ";"
    dl = "struct " + cl + " *alloc"
    code = vt + " *ptr = (struct " + vt + " *) malloc(sizeof(struct " + cl + ") + sizeof(struct " + vt + "));" \
                + ptr_func + "return (struct " + cl + " *)(ptr + 1);"
    alloc = dl + "(){" + code + "}"    
    d_alloc = parse.parse(alloc)
    m_alloc = mangle(d_alloc.body[0], cl, "C")
    clist[cl].append(m_alloc)
    ast.node.body.append(d_alloc.body[0])

    dn = "struct " + cl + " *new"
    code = "struct " + cl + " *ptr = " + m_alloc["mangle"] + "(); return ptr;"
    new = dn + "(){" + code + "}"    

    d_new = parse.parse(new)
    m_new = mangle(d_new.body[0], ret.mname, "C")
    clist[cl].append(m_new)
    ast.node.body.append(d_new.body[0])

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


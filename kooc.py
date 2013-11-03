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
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from module_import import Import
from module import Module
from implementation import Implementation
import dumbXml
import mangle

class   Kooc(Grammar, Declaration, Import, Module, Implementation):

    entry = "kooc"
    grammar = """
        kooc ::=
            @ignore("C/C++")
            [
                "":current_block
                #new_root(_, current_block)
                [ [Declaration.declaration] |
                  [Import.import:imp #add_import(_, imp)] |
                  [Module.module:mod #add_module(_, mod)] |
                  [Implementation.implementation:ip #add_imp(_, ip)]
                ]*
            ]
            Base.eof
        ;
"""

@meta.hook(Kooc)
def add_import(self, ast, ret):
    if ret.nimport != None:
        ast.node.body.extend(ret.nimport.body)
    return True

@meta.hook(Kooc)
def add_imp(self, ast, ret):
    for item in ret.node.body:
        mangle.mangle(item, ret.mname, "C")
    ast.node.body.extend(ret.node.body)
    return True

@meta.hook(Kooc)
def add_module(self, ast, ret):
    print(ret.node.to_dxml())
    for item in ret.node.body:
        mangle.mangle(item, ret.mname, "M")
    ast.node.body.extend(ret.node.body)
    return True

@meta.hook(Kooc)
def printvalue(self, ast):
    print(ast.value)
    return True

@meta.hook(Kooc)
def printnode(self, ast):
    print(ast.node)
    return True

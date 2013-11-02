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
from module_import import Import
from cnorm.passes import to_c

class   Kooc(Grammar, Declaration, Import):

    entry = "translation_unit"
    grammar = """
        translation_unit ::=
            @ignore("C/C++")
            [
                "":current_block
                #new_root(_, current_block)
                [ [Declaration.declaration] | [Import.import:imp #add_import(_, imp)] ]*
            ]
            Base.eof
        ;
"""

@meta.hook(Kooc)
def add_import(self, ast, ret):
    ast.node.body.extend(ret.nimport.body)
    return True

@meta.hook(Kooc)
def printvalue(self, ast):
    print(ast.value)
    return True

@meta.hook(Kooc)
def printnode(self, ast):
    print(ast.node)
    return True


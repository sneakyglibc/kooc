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

class   Kooc(Grammar, Declaration):

    entry = "translation_unit"
    grammar = """
        translation_unit ::=
            @ignore("C/C++")
            [
                "":current_block
                #new_root(_, current_block)
                [
                  Declaration.declaration
                ]*
            ]
            Base.eof
        ;
    """

@meta.hook(Kooc)
def printvalu(self, ast):
    print(ast)

cparse = Declaration()
ast = cparse.parse("int a;")
print (ast.to_c())

cparse = Kooc()
ast = cparse.parse("int a;")
print (ast.node.to_c())


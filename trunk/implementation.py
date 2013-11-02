from pyrser.grammar import Grammar
from pyrser import meta, directives

class   Implementation(Grammar):

    entry = "implementation"
    grammar =   """
          implementation ::=
           "":imp_block
           #new_root(_, imp_block)
           "@implementation" Base.id:n #add_name(_, n) "{"
           [decl_mod]*
           "}" ;
                """
@meta.hook(Implementation)
def add_name(self, ast, name):
    ast.mname = name
    return True


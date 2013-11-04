from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration

class   Call(Grammar, Declaration):

    entry = "primary_expression"
    grammar =   """
        primary_expression ::=
            '(' expression:expr ')' #new_paren(_, expr)
            | [Literal.literal | identifier]:_ | call_kooc:_
        ;
        call_kooc ::=
                @ignore('null')
                [
                 "[" Base.id:mod ["." | " "] Base.id:var "]"
                ]:call  #add_call(call, mod, var) #new_id(_, call)
        ;
                """

@meta.hook(Call)
def add_call(self, call, mod, var):
    from kooc import mlist
    global mlist
    if not mod.value in mlist:
        print("error no module named", mod.value)
        return False;
    for item in mlist[mod.value]:
        if item[0] == var.value:
            call.value = item[1]
    return True

@meta.hook(Call)
def printv(self, ast):
    print(ast)
    return True

from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration
from mangle import mangle

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
                 specif:spe "[" Base.id:mod "." Base.id:var "]"
                ]:call  #add_call(call, mod, var, spe) #new_id(_, call)
        ;
        specif ::=
                ["@!(" [Base.id [" " Base.id]*]:_ ")"]?
        ;
                """

def algo(call, mod, var):
    from kooc import mlist
    global mlist
    result = []
    for item in mlist[mod.value]:
        if item["name"] == var.value and "V" == item["mangle"].split("_")[3]:
            result.append(item["mangle"])
    if len(result) == 1:
        call.value = result[0]
    elif len(result) > 1:
        print("ambiguous statement", mod.value, var.value)
        return False
    else:
        print("error no variable called", mod.value, var.value)
        return False
    return True

def algo_spe(call, mod, var, mangle):
    from kooc import mlist
    global mlist
    result = []
    for item in mlist[mod.value]:
        if item["mangle"] == mangle:
            result.append(mangle)
    if len(result) == 1:
        call.value = result[0]
    elif len(result) > 1:
        print("ambiguous statement", mod.value, var.value)
        return False
    else:
        print("error no variable called", mod.value, var.value)
        return False
    return True

@meta.hook(Call)
def add_call(self, call, mod, var, spe):
    from kooc import mlist
    global mlist
    if not mod.value in mlist:
        print("error no module called", mod.value)
        return False;
    if spe.value == "":
        return algo(call, mod, var)
    else:
        cparse = Declaration()
        ast = cparse.parse(spe.value + " " + var.value + ";")
        m = mangle(ast.body[0], mod.value, "M")["mangle"]
        return algo_spe(call, mod, var, m)
    return True

@meta.hook(Call)
def printv(self, ast):
    print(ast)
    return True

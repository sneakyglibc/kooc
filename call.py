from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration
from mangle import mangle, mangle_func_from
from print_error import print_error

class   Call(Grammar):

    entry = "primary_expression"
    grammar =   """
        primary_expression ::=
                ['(' expression:expr ')' #new_paren(_, expr)
                | [Literal.literal | identifier]:_ | call_kooc:_ | func_kooc:_ ]
        ;
        call_kooc ::=
                @ignore('null')
                [
                 specif:spe "[" Base.id:mod "." Base.id:var "]"
                ]:call  #add_call(call, mod, var, spe) #new_id(_, call)
        ;
        func_kooc ::=
                @ignore('null')
                [
                "":params
                "":call
                 specif:spe "[" Base.id:mod " " Base.id:var [" :" expression:expr #new_arg(params, expr)]* "]"
                ] #mangle_func(call, spe, mod, var, params) #new_id(_, call) #new_func_call(_, _, params)
        ;
        specif ::=
                ["@!(" [Base.id [" " [Base.id | '*']]*]:_ ")"]?
        ;
                """

def res(llist, name, inscope):
    for it in inscope:
        if hasattr(name, "_name"):
            if it["name"] == name._name:
                llist.append(it["type"])
        elif hasattr(name, "value"):
            if it["name"] == name.value:
                llist.append(it["type"])

def resolve(name, cur_scope):
    from kooc import glist
    from drecovery import scope
    from resolveType import resolveType
    global glist
    global scope
    llist = []
    for inscope in cur_scope:
        for item in inscope:
            for it in inscope[item]:
                if hasattr(name, "_name"):
                    if it["name"] == name._name:
                        llist.append(it["type"])
                    elif it["mangle"] == name._name:
                        llist.append(it["type"])
                elif hasattr(name, "value"):
                    if it["name"] == name.value:
                        llist.append(it["type"])
                    elif it["mangle"] == name.value:
                        llist.append(it["type"])
    res(llist, name, glist["__global__"])
    if scope != "__global__":
        res(llist, name, glist[scope])
    if hasattr(name, "_name"):
        llist += resolveType(name._name)
    else:
        llist += resolveType(name.value)
    return llist

@meta.hook(Call)
def mangle_func(self, call, spe, mod, var, params):
    from kooc import mlist, clist
    from listToStr import listToListStr
    global mlist
    global clist
    scope_list = []
    type_object = ""
    if mod.value in mlist:
        scope_list = mlist
        type_object = "M"
    elif mod.value in clist:
        scope_list = clist
        type_object = "C"
    else:
        print_error("error no module called : " + mod.value)
        return False
    cparse = Declaration()
    list_params = []
    all_params = [""]
    found = False
    if hasattr(params, "node"):
        for item in params.node:
            if "<class 'cnorm.nodes.Func'>" != str(type(item)):
                tmp = resolve(item, [mlist, clist])
            else:
                tmp = resolve(item.call_expr, [mlist, clist])
            if tmp == []:
                print_error("Error ambiguious statement")
                return False
            list_params.append(tmp)
        all_params = listToListStr(list_params)
    for item in all_params:
        if spe.value == "":
            m = mangle_func_from(mod.value, type_object, var.value, None, item)
            res = func_algo(call, mod, var, m, scope_list)
        else:
            ast = cparse.parse(spe.value + " " + var.value + "()" ";")
            m = mangle_func_from(mod.value, type_object, var.value, ast.body[0], item)
            res = func_algo_spe(call, mod, var, m, scope_list)
        if res == True and found == True:
            print_error("ambiguous function : " + mod.value + " " + var.value)
            return False
        if res == True:
            found = True
    if found == False:
        print_error("Don't found function : " + mod.value + " " + var.value)
        return False
    return True

def func_algo_spe(call, mod, var, mangle, scope_list):
    result = []
    for item in scope_list[mod.value]:
        if item["mangle"] == mangle:
            result.append(mangle)
    if len(result) == 1:
        call.value = result[0]
        return True
    return False

def func_algo(call, mod, var, mangle, scope_list):
    result = []
    for item in scope_list[mod.value]:
        test = item["mangle"].split("_")[5:]
        test = "_" + "_".join(test)
        if test == mangle:
            result.append(item["mangle"])
    if len(result) == 1:
        call.value = result[0]
        return True
    return False


def algo(call, mod, var, scope):
    result = []
    for item in scope[mod.value]:
        if item["name"] == var.value and "V" == item["mangle"].split("_")[3]:
            result.append(item["mangle"])
    if len(result) == 1:
        call.value = result[0]
    elif len(result) > 1:
        print_error("ambiguous statement : " + mod.value + " " + var.value)
        return False
    else:
        print_error("error no variable called : " + mod.value + " " + var.value)
        return False
    return True

def algo_spe(call, mod, var, mangle, scope): 
    result = []
    for item in scope[mod.value]:
        if item["mangle"] == mangle:
            result.append(mangle)
    if len(result) == 1:
        call.value = result[0]
    elif len(result) > 1:
        print_error("ambiguous statement : " + mod.value + " " + var.value)
        return False
    else:
        print_error("error no variable called : " + mod.value + " " + var.value)
        return False
    return True

@meta.hook(Call)
def add_call(self, call, mod, var, spe):
    from kooc import mlist, clist
    global mlist
    global clist
    scope_list = []
    type_object = ""
    if mod.value in mlist:
        scope_list = mlist
        type_object = "M"
    elif mod.value in clist:
        scope_list = clist
        type_object = "C"
    else:
        print_error("error no variable called : " + mod.value)
        return False
    if spe.value == "":
        return algo(call, mod, var, scope_list)
    else:
        cparse = Declaration()
        ast = cparse.parse(spe.value + " " + var.value + ";")
        m = mangle(ast.body[0], mod.value, type_object)["mangle"]
        return algo_spe(call, mod, var, m, scope_list)
    return True

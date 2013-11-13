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
        if it["name"] == name:
            llist.append(it["type"])

def resolve(name, cur_scope):
    from kooc import glist, slist
    from drecovery import scope
    from resolveType import resolveType
    global glist, slist, scope
    llist = []
    if hasattr(name, "_name"):
        test = name._name
    elif hasattr(name, "value"):
        test = name.value
    if "->" in test:
        test = test.split("->")[1]
        cur_scope = slist
        for inscope in cur_scope:
            for it in cur_scope[inscope]:
                if it["mangle"] == test:
                    llist.append(it["type"])
                elif it["name"] == test: 
                    llist.append(it["type"])
    else:
        for inscope in cur_scope:
            for item in inscope:
                for it in inscope[item]:
                    if it["mangle"] == test:
                        llist.append(it["type"])
                    elif it["name"] == test: 
                        llist.append(it["type"])
    res(llist, name, glist["__global__"])
    if scope != "__global__":
        res(llist, test, glist[scope])
    llist += resolveType(test)
    return llist

@meta.hook(Call)
def mangle_func(self, call, spe, mod, var, params):
    from kooc import mlist, clist, glist, vlist
    from drecovery import scope
    from listToStr import listToListStr
    global mlist, clist, glist, scope, vlist
    scope_list = []
    type_object = ""
    ptr = ""
    if mod.value in mlist:
        scope_list = mlist
        type_object = "M"
    elif mod.value in clist:
        scope_list = clist
        type_object = "C"
    else:
        tmp = None
        for item in glist[scope]:
            if item["name"] == mod.value and len(item["type"]) > 3 and item["type"][:3] == "2Sp":
                if item["type"][3:] in clist:
                    tmp = item
                    break
        if tmp == None:
            print_error("error no module called : " + mod.value)
            return False
        scope_list = vlist
        ptr = mod.value + "->"
        mod.value = tmp["type"][3:]
        type_object = "CM"
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
            res = func_algo(call, mod, var, m, scope_list, ptr)
        else:
            ast = cparse.parse(spe.value + " " + var.value + "()" ";")
            m = mangle_func_from(mod.value, type_object, var.value, ast.body[0], item)
            res = func_algo_spe(call, mod, var, m, scope_list, ptr)
        if res == True and found == True:
            print_error("ambiguous function : " + mod.value + " " + var.value)
            return False
        if res == True:
            found = True
    if found == False:
        print_error("Don't found function : " + mod.value + " " + var.value)
        return False
    return True

def func_algo_spe(call, mod, var, mangle, scope_list, ptr):
    result = []
    for item in scope_list[mod.value]:
        if item["mangle"] == mangle:
            result.append(mangle)
    if len(result) == 1:
        call.value = ptr + result[0]
        return True
    return False

def func_algo(call, mod, var, mangle, scope_list, ptr):
    result = []
    for item in scope_list[mod.value]:
        test = item["mangle"].split("_")[5:]
        test = "_" + "_".join(test)
        if test == mangle:
            result.append(item["mangle"])
    if len(result) == 1:
        call.value = ptr + result[0]
        return True
    return False


def algo(call, mod, var, scope, ptr):
    result = []
    for item in scope[mod.value]:
        if item["name"] == var.value and "V" == item["mangle"].split("_")[3]:
            result.append(item["mangle"])
    if len(result) == 1:
        call.value = ptr + result[0]
    elif len(result) > 1:
        print_error("ambiguous statement : " + mod.value + " " + var.value)
        return False
    else:
        print_error("error no variable called : " + mod.value + " " + var.value)
        return False
    return True

def algo_spe(call, mod, var, mangle, scope, ptr): 
    result = []
    for item in scope[mod.value]:
        if item["mangle"] == mangle:
            result.append(mangle)
    if len(result) == 1:
        call.value = ptr + result[0]
    elif len(result) > 1:
        print_error("ambiguous statement : " + mod.value + " " + var.value)
        return False
    else:
        print_error("error no variable called : " + mod.value + " " + var.value)
        return False
    return True

@meta.hook(Call)
def add_call(self, call, mod, var, spe):
    from kooc import mlist, clist, slist, glist
    from drecovery import scope
    global mlist
    global slist
    global clist
    global glist
    global scope
    scope_list = []
    type_object = ""
    ptr = ""
    if mod.value in mlist:
        scope_list = mlist
        type_object = "M"
    elif mod.value in clist:
        scope_list = clist
        type_object = "C"
    else:
        tmp = None
        for item in glist[scope]:
            if item["name"] == mod.value and len(item["type"]) > 3 and item["type"][:3] == "2Sp":
                if item["type"][3:] in clist:
                    tmp = item
                    break
        if tmp == None:
            print_error("error no module called : " + mod.value)
            return False
        scope_list = slist
        ptr = mod.value + "->"
        mod.value = tmp["type"][3:]
        type_object = "CM"
    if spe.value == "":
        return algo(call, mod, var, scope_list, ptr)
    else:
        cparse = Declaration()
        ast = cparse.parse(spe.value + " " + var.value + ";")
        m = mangle(ast.body[0], mod.value, type_object)["mangle"]
        return algo_spe(call, mod, var, m, scope_list, ptr)
    return True

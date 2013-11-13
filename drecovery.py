from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration
from print_error import print_error

class   Drecovery(Grammar, Declaration):

    entry = "c_decl"
    grammar =   """
        c_decl ::=
            "":local_specifier
            #create_ctype(local_specifier)
            declaration_specifier*:dsp
            init_declarator:decl
            #not_empty(current_block, dsp, decl)
            #end_decl(current_block, decl) #new_scope_decl(decl)
            [
                ',' 
                #copy_ctype(local_specifier, decl)
                init_declarator:decl
                #end_decl(current_block, decl)
            ]*
            [
                ';'
                |
                compound_statement:b
                #add_body(decl, b)
            ]#new_dcl(decl)
        ;
        compound_statement ::=
            [
            '{' #new_scope 
                "":current_block
                #new_blockstmt(_, current_block)
                [
                    line_of_code
                ]*
                #global_scope
            '}'
            ]
        ;
               """
scope = "__global__"
isscope = False
decl = ""

@meta.hook(Drecovery)
def global_scope(self):
    global scope
    scope = "__global__"
    return True

@meta.hook(Drecovery)
def new_scope_decl(self, name):
    global decl
    decl = name.node._name
    return True

@meta.hook(Drecovery)
def new_scope(self):
    from kooc import glist
    global glist
    global scope
    global isscope
    global decl
    isscope = True
    scope = decl
    if not hasattr(glist, scope):
        glist[scope] = []
    return True

@meta.hook(Drecovery)
def new_dcl(self, decl):
    from kooc import glist, mlist, clist, vlist
    from copy import deepcopy
    from mangle import mangle
    from implementation import implement
    global glist
    global scope
    global isscope
    global implement

    if isscope == True and implement["name"] != "":
        m = mangle(decl.node, implement["name"], implement["type"])
        test = clist
        if implement["type"] == "M":
            test = mlist
        if implement["type"] == "CM":
            parse = Declaration()
            nod = parse.parse("struct " + implement["name"] + " * self;");
            decl.node._ctype._params.append(nod.body[0])
            tmp = deepcopy(nod.body[0])
            glist[scope].append(mangle(tmp, "nonename", "M"))
            test = vlist
        found = False
        for item in test[implement["name"]]:
            if item["mangle"] == m["mangle"]:
                found = True
        if found == False:
            print_error("Error function not declared :" + implement["name"] + " " + m["name"])
            return False
    else:
        tmp = deepcopy(decl)
        m = mangle(tmp.node, "nonename", "M")
        for item in glist[scope]:
            if item["mangle"].split("_")[3] == "F":
                if item["mangle"] == m["mangle"]:
                    return True
        glist[scope].append(m)
    isscope = False
    return True

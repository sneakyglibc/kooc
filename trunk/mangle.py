def mangle_primary(decl, name, name_type):
    decl._name = "K" + "_" + name_type + "_" + name + "_" + "V" + "_" + gen_varname(decl) + "_" + str(decl._name)
    return decl._name

def mangle_func(decl, name, name_type):
    if (decl._ctype._params):
        params = ""
        for item in decl._ctype._params:
            params += gen_varname(item) + "_"
        decl._name = "K" + "_" + name_type + "_" + name + "_" + "F" + "_" + gen_varname(decl)  + "_" + str(len(decl._ctype._params)) + "_" +params + str(decl._name)
    else:
        decl._name = "K" + "_" + name_type + "_" + name + "_" + "F" + "_" + decl._ctype._identifier  + str(decl._name)
    return decl._name

def mangle_composed(decl, name, name_type):
    decl._name = "K" + "_" + name_type + "_" + name + "_" + "V" + "_" + gen_varname(decl) + "_" + str(decl._name)
    return decl._name

def mangle(decl, name, name_type):
    if str(type(decl._ctype)) == "<class 'cnorm.nodes.PrimaryType'>" :
        return mangle_primary(decl, name, name_type)
    elif str(type(decl._ctype)) == "<class 'cnorm.nodes.FuncType'>" :
        return mangle_func(decl, name, name_type)
    elif str(type(decl._ctype)) == "<class 'cnorm.nodes.ComposedType'>" :
        return mangle_composed(decl, name, name_type)
        
def gen_varname(decl):
        return gen_primaryname(decl)

def resolve_specifier(specifier):
    if (specifier == 1):
        return "S"
    elif (specifier == 2):
        return "U"
    elif (specifier == 3):
        return "E"
    elif (specifier == 4):
        return "l"
    elif (specifier == 5):
        return "L"
    elif (specifier == 6):
        return "s"

def resolve_qualifier(qual):
    if (qual == 1):
        return "c"
    elif (qual == 2):
        return "v"
    elif (qual == 3):
        return "r"

def resolve_sign(sign):
    if (sign == 2):
        return "u"

def gen_primaryname(decl):
    def recurse(item, nbr, retdata):
        typ = str(type(item))
        if (hasattr(item, '_specifier') and item._specifier != 0):
            retdata += resolve_specifier(item._specifier)
            nbr += 1
        if (hasattr(item, '_qualifier') and item._qualifier != 0):
            retdata += resolve_qualifier(item._qualifier)
            nbr += 1
        if (hasattr(item, '_sign') and item._sign != 0):
            retdata += resolve_sign(item._sign)
            nbr += 1
        elif (typ == "<class 'cnorm.nodes.PointerType'>"):
            retdata += "p"
            nbr += 1            
        elif (typ == "<class 'cnorm.nodes.ArrayType'>"):
            retdata += "t"
            nbr += 1
            if (hasattr(item, '_expr')):
                retdata += str(item._expr.value)
        if (hasattr(item, '_decltype')):
            return recurse(item._decltype, nbr, retdata)
        else:
            return str(nbr) + retdata
    item = decl._ctype
    retdata = recurse(item, 0, "")
    retdata += item._identifier
    return retdata

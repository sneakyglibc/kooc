def mangle_primary(decl, name, name_type):
    decl._name = "K" + "_" + name_type + "_" + name + "_" + "V" + "_" + decl._ctype._identifier  + "_" + str(decl._name)

def mangle_func(decl, name, name_type):
    if (decl._ctype._params):
        params = ""
        for item in decl._ctype._params:
            params += item._ctype._identifier + "_"
        decl._name = "K" + "_" + name_type + "_" + name + "_" + "F" + "_" + decl._ctype._identifier  + "_" + str(len(decl._ctype._params)) + "_" +params + str(decl._name)
    else:
        decl._name = "K" + "_" + name_type + "_" + name + "_" + "F" + "_" + decl._ctype._identifier  + str(decl._name)

def mangle_composed(decl, name, name_type):
    print("composed")

def mangle(decl, name, name_type):
    print(name)
    if str(type(decl._ctype)) == "<class 'cnorm.nodes.PrimaryType'>" :
        mangle_primary(decl, name, name_type)
    elif str(type(decl._ctype)) == "<class 'cnorm.nodes.FuncType'>" :
        mangle_func(decl, name, name_type)
    elif str(type(decl._ctype)) == "<class 'cnorm.nodes.ComposedType'>" :
        mangle_composed(decl, name, name_type)
        

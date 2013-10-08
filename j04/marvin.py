from cnorm.parsing.declaration import Declaration
from cnorm import nodes
from cnorm.passes import dump_nodes

Storages = ['AUTO', 'stocker dans un registre', 'un type', 'definie localement', 'definie dans une autre unite de compilation', 'INLINE', 'VIRTUAL', 'EXPLICIT']
Qualifiers = ['AUTO', 'constant', 'toujours mis a jour lorsqu\'on y accede', 'RESTRICT']
Specifiers = ['AUTO', 'STRUCT', 'UNION', 'ENUM', 'a la jack', 'a la super-jack', 'court']
Signs = ['AUTO', 'SIGNED', 'positif ou nul']
Type = {'int':'un entier', 'double':'un floattant', 'float':'un floattant', 'void':'rien', 'char':'un caractere'}


class   data:
    def __init__(self):
        self.identifier = ""
        self.specifier = 0
        self.storage = 0
        self.qualifier = 0
        self.name = ""
        self.llist = []
        self.literal = []
        self.sign = -1

def print_stro(llist, name, literal, node):
    if node.storage == 4 or node.storage == 2:
        return "je declare! "
    else:
        return "je definie! "

def print_iden(llist, name, literal, node):
    res = ""
    res += Type[node.identifier]
    if node.identifier == "double":
        res += " double precision"
    if node.specifier != 0:
        res += " " + Specifiers[node.specifier]
    if node.sign == 2:
        res += " " + Signs[node.sign] 
    return res

def print_l(llist, name, literal, node, p):
    res = ""
    point = 0
    array = 0
    cnt = 0
    const = ""
    tmp = ""
    res += print_stro(llist, name, literal, node)
    if p != 1:
        res += name + " est "
        if node.storage == 2:
            res += "un type "
            p = 1
        else:
            res += print_iden(llist, name, literal, node)
    else:
        res += name + " est un "
    for item in llist:
        if item == "*":
            if point == 0:
                res += "pointeur "
            else:
                res += "de pointeur "
            if tmp != "":
                res += tmp
                tmp = ""
            point = 1
        elif item == "[]":
            if array == 0:
                res += "tableau "
            else:
                res += "de tableau "
            if tmp != "":
                res += tmp
                tmp = ""
            if len(literal) > array:
                if literal[array] != "None":
                    res += "de taille " + literal[array] + " "
                else:
                    res += "depend d'une expression relou a calculer "
            array += 1
        elif len(llist) - 1 != cnt:
            tmp = item + " "
        else:
            const = item
        cnt += 1
    if p == 1:
        if array != 0:
            res += "ou chaque case contient " + print_iden(llist, name, literal, node)
        else:
            res += "sur " + print_iden(llist, name, literal, node)
    if const != "" and const != "AUTO":
        res += " " + const
    if node.storage != 0 and node.storage != 2:
        res += " " + Storages[node.storage]
    return res

def func(ast, node):
    res = ""
    if hasattr(ast, "body"):
        res += "je definie! " + node.name + " est une fonction qui retourne "
    else:
        res += "je declare! " + node.name + " est une fonction qui retourne "
    res += Type[ast._identifier] + " et qui prends " + str(len(ast._params))
    res += " parametres:"
    llist = ast._params
    for item in llist:
        res += "\n\t- le parametre " + item._name
        res += " comme " + Type[item._ctype._identifier]
    res += "\n"
    return res

def marvin(ast, node = None, level = 0):
    res = ""
    if level == 0:
        node = data()
        node.name = ast._name
        if str(type(ast._ctype)) == "<class 'FuncType'>":
            return func(ast.ctype, node)
        else:
            marvin(ast._ctype, node, level + 1)
        test = []
        p = 0
        print(node.llist)
        for item in node.llist:
            if item == "*" or item == "[]":
                p = 1
            test.append(item)
        tmp = []
        for item in reversed(node.literal):
            tmp.append(item)
        res = print_l(test, node.name, tmp, node, p) + "\n"
    elif level == 1:
        node.identifier = str(ast._identifier)
        node.specifier = ast._specifier
        node.storage = ast._storage
        if hasattr(ast, "_sign"):
            node.sign = ast._sign
        marvin(ast._decltype, node, level + 1)
    elif str(type(ast)) != "<class 'NoneType'>":
        ntype = str(type(ast)).split('.')[2][:-2]
        if ntype == "QualType":
            node.llist.append(Qualifiers[ast._qualifier])
        elif ntype == "PointerType":
            node.llist.append("*")
        elif ntype == "ArrayType":
            node.llist.append("[]")
            if hasattr(ast, "_expr"):
                tmp = ast._expr
                if hasattr(tmp, "value"):
                    node.literal.append(tmp.value)
                else:
                    node.literal.append("None")
        marvin(ast._decltype, node, level + 1)
    return res

#d = Declaration()
#v = d.parse("const int a;")
#print(v.body[0].to_dxml())
#print(marvin(v.body[0]))

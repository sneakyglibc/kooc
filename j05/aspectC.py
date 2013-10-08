from pyrser import meta
from pyrser import parsing
from cnorm import nodes
from pyrser.parsing import node
import binascii
from pyrser.grammar import Grammar
from cnorm.parsing.statement import Statement

def print_set(level, sset):
    res = ""
    for item in sorted(sset):
        ntype = str(type(item)).split()[1][1:-2]
        if ntype == "str":
            res += "{}<'".format('\t' * level) + item + "'/>\n"
        else:
            res += "{}<".format('\t' * level) + str(item) + "/>\n"
    return res

def print_line_dict(level, key, ntype, value):
    res = "{}<".format('\t' * level) + ".idx __key = '"  + str(key) + "' " + ntype + " = " + str(value) + "/>\n"
    return res

def print_object_dict(level, key, ntype, value):
    res = "{}<".format('\t' * level) + ".idx __key = '" + str(key) + "' " + ntype + " = " + str(value) + ">\n"
    return res

def print_dict(level, ddict, sstr, ast, fc):
    res = ""
    ret = 0
    for key in sorted(ddict.keys()):
        ntype = str(type(ddict[key])).split()[1][1:-2]
        if ntype == "bytes":
            res += print_object_dict(level, key, "type", "blob")
            res += "{}".format('\t' * (level + 1))
            par = str(binascii.hexlify(ddict[key])).split("'")[1].upper()
            for i, c in enumerate(par):
                if i % 2 == 0 and i != 0:
                    res += " "
                res += c
            res += "\n"
            res += "{}</".format('\t' * level) + ".idx __key = '" + str(key)  + "'>\n"        
        elif ntype == "dict":
            res += print_object_dict(level, key, "type", ntype)
            res += print_dict(level + 1, ddict[key], sstr, ast, fc)
            res += "{}</".format('\t' * level) + ".idx __key = '" + key  + "'>\n"
        elif ntype == "list":
            res += print_object_dict(level, key, "type", ntype)
            print_list(level + 1, ddict[key], sstr, ast, fc)
            res += "{}</".format('\t' * level)  + ".idx __key = '" + key  + "'>\n"
        elif ntype == "set":
            res += print_object_dict(level, key, "type", ntype)
            res += print_set(level + 1, ddict[key])
            res += "{}</".format('\t' * level)  + ".idx __key = '" + key  + "'>\n"
        elif len(ntype.split('.')) > 1 and ntype.split('.')[1] == "nodes":
            res += print_object_dict(level, key, "type", ntype)
            ret = ddict[key].to_dxml(sstr, ast, fc, level + 1)
            res += "{}</".format('\t' * level)  + ".idx __key = '" + key  + "'>\n"
        else:
            if ntype == "NoneType":
                res += "{}<".format('\t' * level) + ".idx __key = '"  + key + "'/>\n"
            elif ntype == "str":
                res += print_line_dict(level, str(key), ntype, "'" + str(ddict[key]) + "'")
            else:
                res += print_line_dict(level, str(key), ntype, str(ddict[key]))
    return ret


def print_line_list(level, key, ntype, value):
    res = "{}<".format('\t' * level) + ".idx __value = "  + str(key) + " " + ntype + " = " + value + "/>\n"
    return res

def print_object_list(level, key, ntype, value):
    res = "{}<".format('\t' * level) + ".idx __value = " + str(key) + " " + ntype + " = " + value + ">\n"
    return res

def print_list(level, llist, sstr, ast, fc):
    res = ""
    cnt = 0
    flag = -1
    val = []
    found = 0
    for key, item in enumerate(llist):
        ntype = str(type( llist[key])).split()[1][1:-2]
        if ntype == "bytes":
            res += print_object_list(level, key, "type", "blob")
            res += "{}".format('\t' * (level + 1))
            par = str(binascii.hexlify(llist[key])).split("'")[1].upper()
            for i, c in enumerate(par):
                if i % 2 == 0 and i != 0:
                    res += " "
                res += c
            res += "\n"
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key) + ">\n"
        elif ntype == "dict":
            res += print_object_list(level, key, "type", ntype)
            res += print_dict(level + 1, llist[key], sstr, ast, fc)
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key) + ">\n"
        elif ntype == "list":
            res += print_object_list(level, key, "type", ntype)
            ret = print_list(level + 1, llist[key], sstr, ast, fc)
            if ret == 1:
                found = 1
                val.append(cnt + len(val))
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key)  + ">\n"
        elif ntype == "set":
            res += print_object_list(level, key, "type", ntype)
            res += print_set(level + 1, llist[key])
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key)  + ">\n"
        elif len(ntype.split('.')) > 1 and ntype.split('.')[1] == "nodes":
            if ntype.split('.')[2].lower() == sstr and fc == 0:
                found = 1
                val.append(cnt + len(val))
            if ntype.split('.')[2] == "Func" and fc == 1:
                if llist[key].call_expr.value == sstr:
                    flag = 1
            res += print_object_list(level, key, "type", ntype)
            ret = llist[key].to_dxml(sstr, ast, fc, level + 1)
            if ret == 1:
                flag = cnt
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key)  + ">\n"
        else:
            if ntype == "NoneType":
                res += "{}<".format('\t' * level) + ".idx __value = "  + str(key) + "/>\n"
            elif ntype == "str":
                res += print_line_list(level, str(key), ntype, "'" + str(llist[key]) + "'")
            else:
                res += print_line_list(level, str(key), ntype, str(llist[key]))
        cnt += 1
    if found == 1:
        for item in val:
            llist.insert(item, ast)
    return flag

def print_line(level, key, ntype, value):
    res = "{}<".format('\t' * level) + str(key) + " " + ntype + " = " + value + "/>\n"
    return res

def print_object(level, key, ntype, value):
    res = "{}<".format('\t' * level) + str(key) + " " + ntype + " = " + value + ">\n"
    return res

@meta.add_method(nodes.BlockStmt)
def before(self, sstr, ast):
    print(ast)
    llist = ["if", "while", "switch", "for", "do", "return", "goto"]
    for item in llist:
        if sstr == item:
            self.to_dxml(sstr, ast, 0)
    #print(str(self.to_c()))
    
@meta.add_method(nodes.BlockStmt)
def before_func(self, sstr, ast):
    self.to_dxml(sstr, ast, 1)
    #print(str(self.to_c()))

@meta.add_method(parsing.node.Node)
def to_dxml(self, sstr, ast, fc, level = 0):
    res = ""
    ret = -1
    if level == 0:
        res += "<.root type = "+ str(type(ast))  + ">\n"
        ret += self.to_dxml(sstr, ast, fc, level + 1)
        res += "</.root>"
    else:
        for key in  sorted(self.__dict__.keys()):
            ntype = str(type(self.__dict__[key])).split()[1][1:-2]
            if ntype == "bytes":
                res += print_object(level, key, "type", "blob")
                res += "{}".format('\t' * (level + 1))
                par = str(binascii.hexlify(self.__dict__[key])).split("'")[1].upper()
                for i, c in enumerate(par):
                    if i % 2 == 0 and i != 0:
                        res += " "
                    res += c
                res += "\n"
                res += "{}</".format('\t' * level) + str(key)  + ">\n"
            elif ntype == "dict":
                res += print_object(level, key, "type", ntype)
                res += print_dict(level + 1, self.__dict__[key], sstr, ast, fc)
                res += "{}</".format('\t' * level) + key  + ">\n"
            elif ntype == "list":
                res += print_object(level, key, "type", ntype)
                ret = print_list(level + 1, self.__dict__[key], sstr, ast, fc)
                fattype = str(type(self)).split()[1][1:-2]
                if ret != -1 and fattype == "cnorm.nodes.BlockStmt":
                    self.__dict__[key].insert(ret, ast)
                    ret = -1
                res += "{}</".format('\t' * level) + key  + ">\n"
            elif ntype == "set":
                res += print_object(level, key, "type", ntype)
                res += print_set(level + 1, self.__dict__[key])
                res += "{}</".format('\t' * level) + key  + ">\n"
            elif len(ntype.split('.')) > 1 and ntype.split('.')[1] == "nodes":
                res += print_object(level, key, "type", ntype)
                ret = self.__dict__[key].to_dxml(sstr, ast, fc, level + 1)
                res += "{}</".format('\t' * level) + str(key)  + ">\n"
            else:
                if ntype == "str":
                    res += print_line(level, key, ntype, "'" + str(self.__dict__[key]) + "'")
                else:
                    res += print_line(level, key, ntype, str(self.__dict__[key]))
    return ret

from pyrser import meta
from pyrser import parsing
from pyrser.parsing import node
import binascii
from pyrser.grammar import Grammar

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

def print_dict(level, ddict):
    res = ""
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
            res += print_dict(level + 1, ddict[key])
            res += "{}</".format('\t' * level) + ".idx __key = '" + key  + "'>\n"
        elif ntype == "list":
            res += print_object_dict(level, key, "type", ntype)
            res += print_list(level + 1, ddict[key])
            res += "{}</".format('\t' * level)  + ".idx __key = '" + key  + "'>\n"
        elif ntype == "set":
            res += print_object_dict(level, key, "type", ntype)
            res += print_set(level + 1, ddict[key])
            res += "{}</".format('\t' * level)  + ".idx __key = '" + key  + "'>\n"
        elif ntype == "pyrser.parsing.node.Node":
            res += print_object_dict(level, key, "type", "object")
            res += ddict[key].to_dxml(level + 1)
            res += "{}</".format('\t' * level)  + ".idx __key = '" + key  + "'>\n"
        else:
            if ntype == "NoneType":
                res += "{}<".format('\t' * level) + ".idx __key = '"  + key + "'/>\n"
            elif ntype == "str":
                res += print_line_dict(level, str(key), ntype, "'" + str(ddict[key]) + "'")
            else:
                res += print_line_dict(level, str(key), ntype, str(ddict[key]))
    return res


def print_line_list(level, key, ntype, value):
    res = "{}<".format('\t' * level) + ".idx __value = "  + str(key) + " " + ntype + " = " + value + "/>\n"
    return res

def print_object_list(level, key, ntype, value):
    res = "{}<".format('\t' * level) + ".idx __value = " + str(key) + " " + ntype + " = " + value + ">\n"
    return res

def print_list(level, llist):
    res = ""
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
            res += print_dict(level + 1, llist[key])
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key) + ">\n"
        elif ntype == "list":
            res += print_object_list(level, key, "type", ntype)
            res += print_list(level + 1, llist[key])
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key)  + ">\n"
        elif ntype == "set":
            res += print_object_list(level, key, "type", ntype)
            res += print_set(level + 1, llist[key])
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key)  + ">\n"
        elif ntype == "pyrser.parsing.node.Node":
            res += print_object_list(level, key, "type", "object")
            res += llist[key].to_dxml(level + 1)
            res += "{}</".format('\t' * level)  + ".idx __value = " + str(key)  + ">\n"
        else:
            if ntype == "NoneType":
                res += "{}<".format('\t' * level) + ".idx __value = "  + str(key) + "/>\n"
            elif ntype == "str":
                res += print_line_list(level, str(key), ntype, "'" + str(llist[key]) + "'")
            else:
                res += print_line_list(level, str(key), ntype, str(llist[key]))
    return res

def print_line(level, key, ntype, value):
    res = "{}<".format('\t' * level) + str(key) + " " + ntype + " = " + value + "/>\n"
    return res

def print_object(level, key, ntype, value):
    res = "{}<".format('\t' * level) + str(key) + " " + ntype + " = " + value + ">\n"
    return res

@meta.add_method(parsing.node.Node)
def to_dxml(self, level = 0):
    res = ""
    if level == 0:
        res += "<.root type = object>\n"
        res += self.to_dxml(level + 1)
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
                res += print_dict(level + 1, self.__dict__[key])
                res += "{}</".format('\t' * level) + key  + ">\n"
            elif ntype == "list":
                res += print_object(level, key, "type", ntype)
                res += print_list(level + 1, self.__dict__[key])
                res += "{}</".format('\t' * level) + key  + ">\n"
            elif ntype == "set":
                res += print_object(level, key, "type", ntype)
                res += print_set(level + 1, self.__dict__[key])
                res += "{}</".format('\t' * level) + key  + ">\n"
            elif ntype == "pyrser.parsing.node.Node":
                res += print_object(level, key, "type", "object")
                res += self.__dict__[key].to_dxml(level + 1)
                res += "{}</".format('\t' * level) + str(key)  + ">\n"
            else:
                if ntype == "NoneType":
                    res += "{}<".format('\t' * level) + str(key) + "/>\n"
                elif ntype == "str":
                    res += print_line(level, key, ntype, "'" + str(self.__dict__[key]) + "'")
                else:
                    res += print_line(level, key, ntype, str(self.__dict__[key]))
    return res

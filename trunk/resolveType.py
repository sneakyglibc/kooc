import sys

def isChar(s):
    if len(s) != 3:
        return False
    if (s[0] == '\'') & (s[2] == '\''):
        return True
    return False

def isString(s):
    if (s[0] != "\"") & (s[-1] != "\""):
        return False
    return True

def comp(digit, p):
    i = 0
    while i < len(p):
        if digit == p[i]:
            return True
        i += 1
    return False

def isNumber(s):
    i = 0
    if s.count(".") > 1:
        return "ERROR"
    if s[0] == '-':
        i += 1
    for digit in s[i:len(s)]:
        if comp(digit, "0123456789.") == False:
            return "ERROR"
    if s.count(".") == 1:
        return "float"
    return "entier"

def entierType(s):
    nb = int(s)
    Type = list()
    if (nb >= -32768) & (nb <= 32767):
        Type.append("short")
    if (nb >= 0) & (nb <= 65535):
        Type.append("unsigned short")
    if (nb >= -2147483648) & (nb <= 2147483647):
        Type.append("0int")
    if (nb >= 0) & (nb <= 4294967295):
        Type.append("unsigned int")
    if (nb >= -9223372036854775808) & (nb <= 9223372036854775807):
        Type.append("long long")
    if (nb >= 0) & (nb <= 18446744073709551615):
        Type.append("unsigned long long")
    return Type

def floatType(s):
    nb = float(s)
    if nb < 0:
        nb *= -1
    Type = list()
    if (nb >= sys.float_info.min) & (nb <= sys.float_info.max):
        Type.append("float")
        Type.append("double")
    if (nb < sys.float_info.min) & (nb > sys.float_info.max):
        Type.append("double")
    return Type

def resolveType(s):
    ret = str()
    Type = []
    if (s == "true") | (s == "false"):
        Type.append("bool")
        return Type
    if isChar(s):
        Type.append("char")
        Type.append("unsigned char")
        return (Type)
    if isString(s):
        Type.append("const char *")
        return (Type)
    ret = isNumber(s)
    if ret == "float":
        return floatType(s)
    if ret == "entier":
        return entierType(s)
    return (Type)

# print(resolveType("\"Ceci est un test\""))
# print(resolveType("'a'"))
# print(resolveType("false"))
# print(resolveType("42"))
# print(resolveType("-42"))
# print(resolveType("0.5"))
# print(resolveType("-0.5"))
# print(resolveType("-0.r5"))

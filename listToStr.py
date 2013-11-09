#!/usr/bin/python3.3

def initPos(length, param):
    count = 0
    position = []
    for idx, List in enumerate(param):
        tmp = [idx, 0, len(List) - 1]
        position.append(tmp)
    return(position)

def check(position, nb_list):
    while nb_list >= 0:
        if position[nb_list][1] == position[nb_list][2]:
            nb_list -= 1
        else:
            return(True)
    return(False)

def updatePos(position, nb_list):
    while nb_list >= 0:
        if check(position, nb_list) == False:
            return (False)
        if position[nb_list][1] < position[nb_list][2]:
            position[nb_list][1] += 1
            return (True)
        elif position[nb_list][1] == position[nb_list][2]:
            position[nb_list][1] = 0
        nb_list -= 1

def listToListStr(param):
    nb_list = len(param) - 1
    idx = 0
    l_str = []
    position = initPos(nb_list, param)
    tmp = []
    while idx <= nb_list:
        tmp.append(param[position[idx][0]][position[idx][1]])
        idx += 1
        if idx > nb_list:
            l_str.append(tmp)
            idx = 0
            tmp = []
            if updatePos(position, nb_list) == False:
                break
    return(l_str)


#l=[["int", "char", "bool"], ["bool", "char", "long"], ["int", "int", "int", "long"]]
#l2=[["char", "int"], ["long", "bool"]]
#print(listToListStr(l))
#print(listToListStr(l2))

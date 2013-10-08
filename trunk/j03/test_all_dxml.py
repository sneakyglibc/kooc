#!/usr/bin/env python3.3

import dumbXml
from pyrser.parsing import node

## CREATE SAMPLE OF ALL SUPPORTED TYPE

x = node.Node()
x.txt = "cool"
x.flags = True
x.subnode = node.Node()
x.subnode.num = 12
x.sb2 = node.Node()
x.sb2.real = 3.4e+20

f = open("t1.dxml", "w+")
f.write(x.to_dxml())
f.close()

tree = node.Node()
tree.ls = [1, 2.0, "titi", True, [2, 3, 4, [3, [3, 4]], 5]]
tree.dct = {"g":1, "y":2, "koko":{'D', 'T', 'C'}}
tree.aset = {'Z', 'X', 'T', 'U'}
tree.ablob = b'\xFF\xaa\x06Th -}'

f = open("t2.dxml", "w+")
f.write(tree.to_dxml())
f.close()

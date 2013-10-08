import dumbXml
from pyrser.parsing import node

tree = node.Node()
tree.ls = [1, 2.0, "titi", b'\xFF\xaa\x06Th -}', [2, 3, 4, [3, [3, 4]], 5]]
tree.dct = {"g":b'\xFF\xaa\x06Th -}', "y":None, "koko":{'D', 'T', 'C'}}
tree.aset = {'Z', 'X', 'T', 'U'}
tree.ablob = b'\xFF\xaa\x06Th -}'
print(tree.to_dxml())

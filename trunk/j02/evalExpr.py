import sys
from pyrser.grammar import Grammar
from pyrser.error import ParseError
from pyrser import meta
from pyrser.parsing.node import Node
from pyrser.parsing.parserStream import Stream
import collections

class   Evalexpr(Grammar):
    grammar = """
                Calc ::= Expr:res Base.eof #result(res)
                ;
                Expr ::= Term:_ ['+' Term:sec #add(_, sec) | '-' Term:th #sub(_,th)]*
                ;
                Term ::= Factor:_ ['*' Factor:sec #mul(_, sec) | '/' Factor:th #div(_, th)]*
                ;
                Factor ::= ['-' #sign(_) | '+']* [Number:nb | '(' Expr:nb ')'] #msign(_,nb)
                ;
                Number ::= [Base.num+]:_ | Var:_ | Base.id:var #getVar(_, var)
                ;
                Var ::= [[Base.id]:var '=' [Expr]:val] #getVal(_, var, val)
                ;
                """
    entry = "Calc"
    var = {}
    def parse_file(self, filename: str, entry=None):
        """Parse filename using the grammar"""
        import os.path
        if os.path.exists(filename):
            f = open(filename, 'r')
            ss = f.readline()
            while (ss != ""):
                if ss[len(ss) - 1] == '\n':
                    ss[0:-1]
                self.parse(ss)
                ss = f.readline()

@meta.hook(Evalexpr)
def getVar(self, ret, key):
    if not key.value in self.var:
        return False
    ret.value = self.var[key.value]
    return True

@meta.hook(Evalexpr)
def getVal(self, ret, key, val):
    self.var[key.value] = val.value
    ret.value = val.value
    return True

@meta.hook(Evalexpr)
def result(self, ret):
    if int(ret.value) == float(ret.value):
        print(int(ret.value))
    else:
        print(ret.value)
    return True

@meta.hook(Evalexpr)
def sign(self, ret):
    if not hasattr(ret, "sign"):
        ret.sign = 1
    ret.sign *= -1
    return True

@meta.hook(Evalexpr)
def msign(self, ret, nb):
    ret.value = nb.value
    if hasattr(ret, "sign"):
        ret.value = float(ret.value) * float(ret.sign)
    return True

@meta.hook(Evalexpr)
def mul(self, ret, nb):
    ret.value = float(ret.value) * float(nb.value)
    return True

@meta.hook(Evalexpr)
def div(self, ret, nb):
    ret.value =  float(ret.value) / float(nb.value)
    return True

@meta.hook(Evalexpr)
def add(self, ret, nb):
    ret.value =  float(ret.value) + float(nb.value)
    return True

@meta.hook(Evalexpr)
def sub(self, ret, nb):
    ret.value =  float(ret.value) - float(nb.value)
    return True

p = Evalexpr()
p.parse_file(sys.argv[1])

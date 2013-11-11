from pyrser.grammar import Grammar
from pyrser import meta, directives

class   Import(Grammar):

    entry = "import"
    grammar =   """
                import ::= "@import" '"' [name_import]+:ret '"' #rule_import(_, ret);
                name_import ::= ['a'..'z' | 'A'..'Z' | '0'..'9' | '.' | '/' |  '_'] ;
                """

@meta.hook(Import)
def rule_import(self, ast, ret):
    from kooc import Kooc
    from kooc import ilist
    import os
    global ilist

    if not os.path.exists(ret.value):
        print("Error : file not found : " + ret.value)
        return False
    tmp = ret.value.split("/")[-1]
    if tmp in ilist:
        print("Warning : recursive inclusion ", tmp)
        ast.nimport = None
    else:
        ilist.append(tmp)
        parse = Kooc()
        ast.nimport = parse.parse_file(ret.value)
    return True

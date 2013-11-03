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
    tmp = ret.value.split("/")[-1]
    global ilist
    if tmp in ilist:
        print("Warning : recursive inclusion ", tmp)
        ast.nimportx = None
    else:
        ilist.append(tmp)
        parse = Kooc()
        ast.nimport = parse.parse_file(ret.value)
    return True

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
    if not hasattr(self, "lfile"):
        self.lfile = []
    tmp = ret.value.split("/")[-1]
    if tmp in self.lfile:
        print("Warning : recursive inclusion ", tmp)
        ast.nimport = None
    else:
        self.lfile.append(tmp)
        parse = Kooc()
        ast.nimport = parse.parse_file(ret.value).node
    return True

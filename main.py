from kooc import Kooc

cparse = Kooc()
ast = cparse.parse("int a;int b; @import \"module.kh\"")
print (ast.node.to_c())

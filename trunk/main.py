from kooc import Kooc

cparse = Kooc()
ast = cparse.parse_file("test.kc")
print (ast.node.to_c())

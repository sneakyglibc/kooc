from kooc import Kooc
import dumbXml

cparse = Kooc()
ast = cparse.parse_file("test.kc")
print (ast.node.to_c())


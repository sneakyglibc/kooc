from kooc import Kooc
import dumbXml
import sys

cparse = Kooc()
ast = cparse.parse_file(sys.argv[1])
print (ast.node.to_c())
#print (ast.node.to_dxml())


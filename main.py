from kooc import Kooc
import dumbXml
import sys
from pyrser.error import ParseError



def main():
    try:
        cparse = Kooc()
        ast = cparse.parse_file(sys.argv[1])
        res = "#include <stdlib.h>\n" + str(ast.node.to_c())
        #print (ast.node.to_dxml())
    except ParseError as e:                                                                                                                                
        print(str(e))
    else:
        dst = open(sys.argv[1].split(".")[0] + ".c", 'w')
        dst.write(res)
        print(res)
        


if __name__ == '__main__':
    main()

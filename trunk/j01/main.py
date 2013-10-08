import sys
from parserCSV import *
csv = parserCSV()
res = csv.parse(";;toto;;tata;\n;\n\npere")
for line in res.lines:
    for word in line:
        print(word)

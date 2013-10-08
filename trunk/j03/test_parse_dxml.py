#!/usr/bin/env python3.3

import dumbXml

## READ SAMPLE OF ALL SUPPORTED TYPE

dxml = dumbXml.dxmlParser()

xml0 = dxml.parse("""
        <.root type=object>
            <raw str='From scratch' />
        </.root>
    """)

if xml0.raw == "From scratch":
    print("OK")

xml1 = dxml.parse_file("t1.dxml")

if xml1.subnode.num == 12:
    print("OK")

xml2 = dxml.parse_file("t2.dxml")

if xml2.ls[4][3][1][1] == 4:
    print("OK")


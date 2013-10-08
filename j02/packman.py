import struct

def ushort_uint(bytes):
    return struct.unpack('>HI',bytes)

def buf2latin(bytes):
    size = struct.unpack_from('>H',bytes)
    ss = struct.unpack(">H" + str(size[0]) + "s", bytes)
    carac = struct.unpack(str(size[0]) + "B", ss[1])
    stri = ""
    for item in carac:
        stri += chr(item)
    return (size[0], stri)

def ascii2buf(*args):
    ss = struct.pack(">I", len(args))
    for item in args:
        ss += struct.pack(">H", len(item))
        ss += struct.pack(">" + str(len(item)) + "s", item.encode('utf-8'))
    ss = bytearray(ss)
    return ss

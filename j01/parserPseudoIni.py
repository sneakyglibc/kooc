from pyrser.grammar import Grammar
from pyrser.error import ParseError
from pyrser import meta
from pyrser.parsing.node import Node

class   parserPseudoIni(Grammar):
    grammar = """
                Ini ::= [Section:section #create_section_l(_, section)]+ Base.eof
                ;
                Section ::= '[' Base.id:section_n']' [ClefValeur:keyval #create_section_vals(_, keyval)]+ #create_section(_, section_n)
                ;
                ClefValeur ::= Base.id:key '=' valeur:value #create_kv(_, key, value)
                ;
                valeur ::= Base.id | Base.num | Base.string
                ;
                """
    entry = "Ini"

@meta.hook(parserPseudoIni)
def create_section_l(self, ret, case):
    if not hasattr(ret, "sections"):
        ret.sections = {}
    ret.sections[case.section_name] = case.section_values
    return True

@meta.hook(parserPseudoIni)
def create_section(self, ret, section_name):
    ret.section_name = section_name.value
    return True

@meta.hook(parserPseudoIni)
def create_section_vals(self, ret, kv):
    if not hasattr(ret, "section_values"):
        ret.section_values = {}
    ret.section_values[kv.key] = kv.value
    return True

@meta.hook(parserPseudoIni)
def create_kv(self, ret, key, value):
    ret.key = key.value
    ret.value = value.value
    return True


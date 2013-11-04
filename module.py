from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration

class   Module(Grammar, Declaration):

    entry = "module"
    grammar =   """
        module ::=
           "":module_block
           #new_root(_, module_block)
           "@module" Base.id:n #add_name(_, n) "{"
           [decl_mod]*
           "}" ;

        decl_mod ::=
            "":local_specifier
            #create_ctype(local_specifier)
            declaration_specifier+:dsp
            init_declarator:decl
            #not_empty(module_block, dsp, decl)
            #end_decl(module_block, decl)
            [
                ','
                #copy_ctype(local_specifier, decl)
                init_declarator:decl
                #end_decl(module_block, decl)
            ]*
            [
                ';'
                |
                Statement.compound_statement:b
                #add_body(decl, b)
            ]
        ;

        declaration_specifier ::=
            Base.id:i
            #new_decl_spec(local_specifier, i, module_block)
            [
                #is_composed(local_specifier)
                composed_type_specifier
                |
                #is_enum(local_specifier)
                enum_specifier
                |
                #is_typeof(i)
                typeof_expr
            ]?
            |
            attr_asm_decl:attr
            #add_attr_specifier(local_specifier, attr)
        ;
        composed_fields ::=
            '{'
                "":current_block
                #new_composed(_, module_block)
                decl_mod*
            '}'
        ;
               """
@meta.hook(Module)
def add_name(self, ast, name):
    ast.mname = name.value
    return True

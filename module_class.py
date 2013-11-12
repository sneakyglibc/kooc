from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration
from cnorm import nodes

class   Mclass(Grammar):

    entry = "class"
    grammar =   """
        class ::=
           "":module_block
           "":private_block
           #new_root(_, module_block)
           #new_private(_, private_block)
           "@class" Base.id:n #add_name(_, n) "{"
           [decl_mod
                | [ #begin_private "@member" [ ["{" [decl_mod | ";"]* "}"] | decl_mod | ";" ] #end_private ]
                | ";"]*
           "}"
        ;
        decl_mod ::=
            "":local_specifier
            #create_ctype(local_specifier)
            declaration_specifier+:dsp
            init_declarator:decl
            #not_empty(module_block, dsp, decl)
            #end_decl_class(module_block, private_block, decl)
            [
                ','
                #copy_ctype(local_specifier, decl)
                init_declarator:decl
                #end_decl_class(module_block, private_block, decl)
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
                #new_composed(_, current_block)
                decl_mod*
            '}'
        ;
               """

private = False

@meta.hook(Mclass)
def add_name(self, ast, name):
    ast.mname = name.value
    return True

@meta.hook(Mclass)
def begin_private(self):
    global private
    private = True
    return True

@meta.hook(Mclass)
def end_private(self):
    global private
    private = False
    return True

@meta.hook(Mclass)
def new_private(self, ast, current_block):
    ast.private = nodes.RootBlockStmt([])
    current_block.node = ast.private
    return True
 
@meta.hook(Mclass)
def end_decl_class(self, current_block, private_block, ast):
    global private

    if private == False:
        current_block.node.body.append(ast.node)
        if hasattr(ast.node, 'ctype') and ast.node._name != "" and \
                ast.node.ctype._storage == nodes.Storages.TYPEDEF:
            current_block.node.types[ast.node._name] = ref(ast.node)                           
    else:
        private_block.node.body.append(ast.node)
        if hasattr(ast.node, 'ctype') and ast.node._name != "" and \
                ast.node.ctype._storage == nodes.Storages.TYPEDEF:                          
            private_block.node.types[ast.node._name] = ref(ast.node)
    return True

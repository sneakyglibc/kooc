from pyrser.grammar import Grammar
from pyrser import meta, directives
from cnorm.parsing.declaration import Declaration

class   Call(Grammar, Declaration):

    entry = "expression"
    grammar =   """
        unary_expression ::=
            // CAST
            '(' type_name:t ')'
            [
                // simple cast
                unary_expression:_
                |
                // compound literal
                initializer_block:_
            ]
            #to_cast(_, t)
            | // SIZEOF
            Base.id:i #sizeof(i)
            [
                '(' type_name:n ')'
                | Expression.unary_expression:n
            ]:n
            #new_sizeof(_, i, n)
            | Expression.unary_expression:_
        ;

        // ({}) and __builtin_offsetof
        primary_expression ::=
            "({"
                "":current_block
                #new_blockexpr(_, current_block)
                [
                    line_of_code
                ]*
            "})"
            | // TODO: create special node for that
                "__builtin_offsetof"
                '(' [type_name ',' postfix_expression]:bof ')'
                #new_builtoffset(_, bof)
            |
            Expression.primary_expression:_
        ;
constant_expression ::=
            conditional_expression:_
        ;
                """

@meta.hook(Call)
def printv(self, ast):
    print(ast)
    return True

from cnorm.parsing.statement import Statement
from cnorm.passes import to_c
import aspectC

cparse = Statement()

ast = cparse.parse("""
{

while ("coucou")
{
for(koko;lolo;++jiji)
{
calcul = de + la + mort();
}
for(koko;lolo;++jiji)
{
calcul = de + la + dada();
calcul = de + la + mort();
calcul = de + la + mort();
}
calcul = de + la + mort();
}
f["toto"][2];
return i;
}
""", "compound_statement")

ast.before("for", cparse.parse("""
printf("c'est cool la ligne d'en dessous est une boucle for");
""", "single_statement"))

ast.before_func("mort", cparse.parse("""
printf("mort() est une fonction de la vie");
""", "single_statement"))

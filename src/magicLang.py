# -----------------------------------------------------------------------------
# MagicLang
#
"""
<programa> ::= { <lista_sentencias> }
<lista_sentencias> ::= <sentencia> | <sentencia> <lista_sentencias>
<sentencia> ::= λ | <asignacion>; | <funcion> | <invocacion>; | <repeticion> | <condicional> | <imprimir>;

<asignacion> ::= forjar <identificador> = <valor>

<identificador> ::= <minuscula> <caracteres>
<caracteres> ::= λ | <caracter><caracteres>
<caracter> ::= <minuscula> | <mayuscula> | <numero> | <simbolo>

<funcion> ::= hechizo <identificador>(<vacio_o_parametros>) <bloque>

<vacio_o_parametros> ::= λ | <parametros>
<parametros> ::= <identificador> | <identificador>, <parametros>
<bloque> ::= [<lista_sentencias>]

<invocacion> ::= invocar <identificador>(<vacio_o_argumento>) | invocar <bloque>
<vacio_o_argumento> ::= λ | <argumento>
<argumento> ::= <valor> | <valor>, <argumento>

<repeticion> ::= conjurar (<valor_numerico>) veces <bloque>

<condicional> ::= ritual(<valor_booleano>) <bloque> | ritual(<valor_booleano>) <bloque> fallido <bloque>

<imprimir> ::= encantar(<valor>)

<valor> ::= <valor_numerico> | <valor_booleano>

<valor_numerico> ::= <numero> | <operacion_numerica> | <identificador>
<operacion_numerica> ::= <valor_numerico> <operador_numerico> <valor_numerico> | (<valor_numerico>)

<valor_booleano> ::= <booleano> | <operacion_booleana> | <identificador>
<operacion_booleana> ::= no <valor_booleano> | <valor_booleano> <operador_booleano> <valor_booleano> | <valor_numerico> <comparador_numerico> <valor_numerico> | (<valor_booleano>)

<operador_numerico> ::= + | - | * | / | %
<comparador_numerico> ::= <comparacion> | < | > | <= | >=
<operador_booleano> ::= <comparacion> | y | o
<comparacion> ::= == | !=
<booleano> ::= Verdadero | Falso
<numero> ::= <digito> | <digito><numero>
<digito> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<minuscula> ::= a | b | c | d | e | f | g | h | i | j | k | l | m | n | ñ | o | p | q | r | s | t | u | v | w | x | y | z
<mayuscula> ::= A | B | C | D | E | F | G | H | I | J | K | L | M | N | Ñ | O | P | Q | R | S | T | U | V | W | X | Y | Z
<simbolo> ::= _ | - | # | $ | ?
"""
#
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

reservadas = {
    'y': 'Y',
    'o': 'O',
    'no': 'NO',
    'forjar': 'FORJAR',
    'hechizo': 'HECHIZO',
    'invocar': 'INVOCAR',
    'conjurar': 'CONJURAR',
    'veces': 'VECES',
    'ritual': 'RITUAL',
    'fallido': 'FALLIDO',
    'encantar': 'ENCANTAR'
}

# All tokens must be named in advance.
tokens = (  'MAS', 'MENOS', 'POR', 'DIVIDIDO', 'MODULO',
            'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL',
            'IGUAL', 'DISTINTO',
            'ASIGN', 'COMA', 'PUNTO_Y_COMA', 
            'IZQ_LLAVE', 'DER_LLAVE', 'IZQ_CORCHETE', 'DER_CORCHETE',
            'NUMERO', 'BOOLEANO', 'ID'
        ) + tuple(reservadas.values())

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_MODULO = r'%'
t_MAYOR = r'<'
t_MENOR = r'>'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUAL = r'=='
t_DISTINTO = r'!='
t_ASIGN = r'='
t_PUNTO_Y_COMA = r';'
t_COMA = r','
t_IZQ_LLAVE = r'\{'
t_DER_LLAVE = r'\}'
t_IZQ_CORCHETE = r'\['
t_DER_CORCHETE = r'\]'


# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLEANO(t):
    r'(Verdadero|Falso)'
    if t.value == 'Verdadero':
        t.value = True
    else:
        t.value = False
    return t

def t_ID(t):
    r'[a-zñ][a-zA-Z0-9_ñ\-#$?]*'
    if t.value in reservadas:
        t.type = reservadas[t.value]
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Parser
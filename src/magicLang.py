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

<repeticion> ::= conjurar (<valor>) veces <bloque>

<condicional> ::= ritual(<valor>) <bloque> | ritual(<valor>) <bloque> fallido <bloque>

<imprimir> ::= encantar(<valor>)

<valor> ::= <valor_numerico> | <valor_booleano> | <identificador>

<valor_numerico> ::= <numero> | <operacion_numerica>
<operacion_numerica> ::= <valor_numerico> <operador_numerico> <valor_numerico> | (<valor_numerico>)

<valor_booleano> ::= <booleano> | <operacion_booleana>
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
from magicLangSem import *

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
            'IZQ_LLAVE', 'DER_LLAVE', 'IZQ_CORCHETE', 'DER_CORCHETE', 'IZQ_PAREN', 'DER_PAREN',
            'NUMERO', 'BOOLEANO', 'ID'
        ) + tuple(set(reservadas.values()))

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
t_IZQ_PAREN = r'\('     
t_DER_PAREN = r'\)'


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
    print(f'Caracter incorrecto {t.value[0]!r} en línea {t.lexer.lineno}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()



##########################################
# --- Parser
##########################################

# Precedencia de operadores unificada
precedence = (
    ('left', 'O'),
    ('left', 'Y'),
    ('right', 'NO'),
    ('nonassoc', 'IGUAL', 'DISTINTO', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'MENOS_U'), # Para 'menos' unario (ej. -5)
)

entorno_g = Entorno()

# Símbolo inicial
start = 'programa'

def p_programa(p):
    '''programa : IZQ_LLAVE lista_sentencias DER_LLAVE'''
    # p[0] ahora almacena el AST completo (la lista de sentencias)
    p[0] = p[2]

def p_lista_sentencias(p):
    '''lista_sentencias : lista_sentencias sentencia
                        | empty'''
    if len(p) == 3:
        p[0] = p[1]
        if p[2]: # p[2] puede ser None si la sentencia es 'empty'
            p[0].append(p[2])
    else:
        p[0] = [] # Una lista vacía

def p_sentencia(p):
    '''sentencia : asignacion PUNTO_Y_COMA
                 | funcion
                 | invocacion PUNTO_Y_COMA
                 | repeticion
                 | condicional
                 | imprimir PUNTO_Y_COMA
                 | empty''' # Permitimos sentencias vacías (ej. ';;')
    p[0] = p[1]

def p_asignacion(p):
    '''asignacion : FORJAR ID ASIGN expresion'''
    # Retorna un nodo AST: ('asignacion', 'nombre_variable', nodo_expresion)
    p[0] = ('asignacion', p[2], p[4])

def p_funcion(p):
    '''funcion : HECHIZO ID IZQ_PAREN vacio_o_parametros DER_PAREN bloque'''
    # Retorna un nodo AST: ('hechizo', 'nombre_funcion', [lista_params], nodo_bloque)
    p[0] = ('hechizo', p[2], p[4], p[6])

def p_vacio_o_parametros(p):
    '''vacio_o_parametros : parametros
                          | empty'''
    p[0] = p[1] if len(p) == 2 else []

def p_parametros(p):
    '''parametros : ID COMA parametros'''
    # Retorna una lista de nombres: ['id1', 'id2', ...]
    p[0] = [p[1]] + p[3]
    
def p_parametros_simple(p):
    '''parametros : ID'''
    p[0] = [p[1]]

def p_bloque(p):
    '''bloque : IZQ_CORCHETE lista_sentencias DER_CORCHETE'''
    # Pasa la lista de sentencias del bloque
    p[0] = p[2]

def p_invocacion(p):
    '''invocacion : INVOCAR ID IZQ_PAREN vacio_o_argumento DER_PAREN'''
    # Nodo AST: ('invocar_funcion', 'nombre_funcion', [lista_argumentos])
    p[0] = ('invocar_funcion', p[2], p[4])

def p_invocacion_bloque(p):
    '''invocacion : INVOCAR bloque'''
    # Nodo AST: ('invocar_bloque', nodo_bloque)
    p[0] = ('invocar_bloque', p[2])

def p_vacio_o_argumento(p):
    '''vacio_o_argumento : argumento
                         | empty'''
    p[0] = p[1] if len(p) == 2 else []

def p_argumento(p):
    '''argumento : expresion COMA argumento'''
    # Retorna una lista de nodos de expresion
    p[0] = [p[1]] + p[3]

def p_argumento_simple(p):
    '''argumento : expresion'''
    p[0] = [p[1]]

def p_repeticion(p):
    '''repeticion : CONJURAR IZQ_PAREN expresion DER_PAREN VECES bloque'''
    # Nodo AST: ('conjurar', nodo_veces, nodo_bloque)
    p[0] = ('conjurar', p[3], p[6])
    

def p_condicional(p):
    '''condicional : RITUAL IZQ_PAREN expresion DER_PAREN bloque fallido_opcional'''
    # Nodo AST: ('ritual', nodo_condicion, nodo_bloque_if, nodo_bloque_else)
    p[0] = ('ritual', p[3], p[5], p[6])


def p_fallido_opcional(p):
    '''fallido_opcional : FALLIDO bloque
                        | empty'''
    p[0] = p[2] if len(p) == 3 else None # None si no hay bloque 'fallido'

def p_imprimir(p):
    '''imprimir : ENCANTAR IZQ_PAREN expresion DER_PAREN'''
    # Nodo AST: ('encantar', nodo_expresion)
    p[0] = ('encantar', p[3])
    

def p_expresion_binop(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MODULO expresion
                 | expresion Y expresion
                 | expresion O expresion
                 | expresion IGUAL expresion
                 | expresion DISTINTO expresion
                 | expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion MAYOR_IGUAL expresion'''
    p[0] = ('op_binaria', p[2], p[1], p[3])

def p_expresion_unop(p):
    '''expresion : NO expresion
                 | MENOS expresion %prec MENOS_U''' # Menos unario (ej. -10)
    p[0] = ('op_unaria', p[1], p[2])

def p_expresion_group(p):
    '''expresion : IZQ_PAREN expresion DER_PAREN'''
    p[0] = p[2]

def p_expresion_base(p):
    '''expresion : NUMERO
                 | BOOLEANO
                 | ID'''
    if p.slice[1].type == 'NUMERO':
        p[0] = ('numero', p[1])
    elif p.slice[1].type == 'BOOLEANO':
        p[0] = ('booleano', p[1])
    elif p.slice[1].type == 'ID':
        p[0] = ('id', p[1])

# Regla para producción vacía (λ)
def p_empty(p):
    '''empty :'''
    p[0] = None

# Manejador de errores de sintaxis
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}' (Tipo: {p.type}) en la línea {p.lineno}")
    else:
        print("Error de sintaxis: Fin de archivo inesperado (EOF).")

# Construir el parser
parser = yacc()

test_code = """
{   
    forjar x = 2-1;
    
    conjurar(4)veces [
        forjar x = x*2;
    ]

    forjar cond = x == 16;

    ritual(cond o x > 20)[
        encantar(x);
    ] fallido [
        encantar(no cond);
    ]
}
"""

test_code2 = """
{   
    hechizo repetirXvecesImprimirY(p1,p2) [
        conjurar (p1) veces [
            encantar(p2);
        ]
    ]

    invocar repetirXvecesImprimirY(2, 4);
    invocar repetirXvecesImprimirY(3, 1);
}
"""

print("--- Iniciando Parseo e Interpretación de MagicLang ---")

interprete = parser.parse(test_code2, lexer=lexer)

if interprete:
    interpretar(interprete, entorno_g)
    
print("--- Fin del Programa ---")
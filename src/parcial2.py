from ply.lex import lex
from ply.yacc import yacc

### SCANNER ###

# All tokens must be named in advance.
tokens = ('LLAVE_I', 'LLAVE_D', 'PUNTO_Y_COMA', 'IGUAL', 'MAS', 'MENOS', 'LETRA') 

# Token matching rules are written as regexs
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_PUNTO_Y_COMA = r';'
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'-'

def t_LETRA(t):
    r'[abc]'
    return t

# Ignored token with an action associated with it
t_ignore = ' \t\n'

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Error: Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()


### SCANNER ###

start = 'P'

# Regla P -> { L
def p_P(p):
    '''P : LLAVE_I L'''
    print("Parseo completo: Aceptado")

# Regla L -> } | S ; L
def p_L(p):
    '''L : LLAVE_D
         | S PUNTO_Y_COMA L'''

# Regla S -> V = E
def p_S(p):
    '''S : V IGUAL E'''

# Regla V -> a | b | c
def p_V(p):
    '''V : LETRA'''

# Regla E -> V O
def p_E(p):
    '''E : V O'''

# Regla O -> + V | - V | V
def p_O(p):
    '''O : MAS V
         | MENOS V
         | V'''

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}' (Tipo: {p.type}) en línea {p.lineno}")
    else:
        print("Error de sintaxis: Fin de entrada inesperado (EOF)")

# Build the parser object
parser = yacc()


### PRUEBA ###

print("--- Prueba con entrada VÁLIDA ---")
data_valida = """
{
    a = bc;
    b = a + b;
    c = c - a;
}
"""
parser.parse(data_valida)
print("\n")

print("--- Prueba con entrada INVÁLIDA (token 'x') ---")
data_invalida_lex = "{ a = bx; }"
parser.parse(data_invalida_lex, lexer=lexer.clone()) # Reiniciamos el lexer
print("\n")


print("--- Prueba con entrada INVÁLIDA (sintaxis ' falta el ; ') ---")
data_invalida_sintax = "{ a = b }"
parser.parse(data_invalida_sintax, lexer=lexer.clone())
print("\n")
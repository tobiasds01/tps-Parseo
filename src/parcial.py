# -----------------------------------------------------------------------------
# PARCIAL
# -----------------------------------------------------------------------------
"""
from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = (  'NOMBRE', 'DELIMITADOR', 'BLANCO')

# Token matching rules are written as regexs
t_DELIMITADOR = r'[.,;]'
t_BLANCO = r'[ \t]+'
t_NOMBRE = r'[a-zñ][a-zA-ZñÑ0-9]*'

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Error: Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()
    
# --- Prueba del Scanner ---

# Datos de entrada para probar
data = 1run test1 test2;build main;deploy

# Darle la entrada al lexer
lexer.input(data)

print("--- Iniciando Scanner ---")
# Tokenizar
while True:
    tok = lexer.token()
    if not tok:
        break  # No hay más tokens
    print(f"  Token -> {tok.type:12} Lexema -> {tok.value!r:10} (Línea {tok.lineno})")

print("--- Fin del Scanner ---")

"""
from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = () # 'LLAVE_I', 'LLAVE_D', 'PUNTO_Y_COMA', 'IGUAL', 'MAS', 'MENOS', 'LETRA')

# Token matching rules are written as regexs
"""
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_PUNTO_Y_COMA = r'\;'
t_IGUAL = r'\='
t_MAS = r'\+'
t_MENOS = r'\-'
t_LETRA = r'[a,b,c]'
"""
# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Error: Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

"""

# Definir el símbolo inicial (la regla "raíz" de la gramática)
start = 'P'

# Regla P -> { L
def p_P(p):
    '''P : LLAVE_I L'''
    print("-> Parseo completo: P -> { L")

# Regla L -> } | S ; L
def p_L(p):
    '''L : LLAVE_D
         | S PUNTO_Y_COMA L'''

# Regla S -> V = E
def p_S(p):
    '''S : V IGUAL E'''

# Regla V -> ID (para a, b, c)
def p_V(p):
    '''V : ID'''

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

# Construir el parser.
# debug=True es útil para ver qué hace, pero genera un archivo 'parser.out'
parser = yacc.yacc()


# --- 3. PRUEBA ---

print("--- Prueba con entrada VÁLIDA ---")
# E -> V O -> V V -> b c
# E -> V O -> V + V -> a + b
data_valida = 
{
    a = b c ;
    b = a + b ;
    c = a
}

parser.parse(data_valida)
print("Sintaxis OK.\n")


print("--- Prueba con entrada INVÁLIDA (token 'x') ---")
data_invalida_lex = "{ a = x }"
parser.parse(data_invalida_lex, lexer=lexer.clone()) # Reiniciamos el lexer
print("\n")


print("--- Prueba con entrada INVÁLIDA (sintaxis '; }') ---")
data_invalida_sintax = "{ a = b ; }" # Falta una S antes del '}'
parser.parse(data_invalida_sintax, lexer=lexer.clone())
print("\n")

"""






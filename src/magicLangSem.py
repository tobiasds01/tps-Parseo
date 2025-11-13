######################
# Clases auxiliares
######################

class Entorno:
    def __init__(self):
        self.variables = {}
        self.funciones = {}

    def get_variable(self, nombre):
        
        if nombre in self.variables:
            return self.variables[nombre]
        else:
            raise NameError(f"Error: Variable {nombre} no forjada.")

    def set_variable(self, nombre, valor):
        self.variables[nombre] = valor

    def get_funcion(self, nombre):
        if nombre in self.funciones:
            return self.funciones[nombre]
        else:
            raise NameError(f"Error: Hechizo {nombre} no definido.")

    def set_funcion(self, nombre, funcion):
        self.funciones[nombre] = funcion

class Hechizo:
    def __init__(self, parametros, nodo_bloque):
        self.parametros = parametros
        self.bloque = nodo_bloque

    def get_args(self):
        return self.parametros
    
    def get_bloque(self):
        return self.bloque

####################
# Semántica
####################

def interp_asignacion(id, nodo, entorno):
    entorno.set_variable(id, interpretar(nodo, entorno))

def interp_crear_funcion(id, params, bloque, entorno):
    hechizo = Hechizo(params, bloque)
    entorno.set_funcion(id, hechizo)

def ejecutar_bloque(nodo_bloque, entorno):
    for elem in nodo_bloque:
        interpretar(elem, entorno)

def interp_imprimir(nodo_valor, entorno):
    if nodo_valor[0] == 'id':
        print(str(nodo_valor[1]) + " = " + str(entorno.get_variable(nodo_valor[1])))
    else:
        print(str(interpretar(nodo_valor, entorno)))

def interp_repeticion(nodo_numero, nodo_bloque, entorno):
    num_repeticion = interpretar(nodo_numero, entorno)

    for i in range(num_repeticion):
        ejecutar_bloque(nodo_bloque, entorno)

def interp_condicional(nodo_condicion, nodo_bloque_if, nodo_bloque_else, entorno):
    condicion = interpretar(nodo_condicion, entorno)

    if(condicion):
        ejecutar_bloque(nodo_bloque_if, entorno)
    elif nodo_bloque_else is not None:
        ejecutar_bloque(nodo_bloque_else, entorno)

def interp_invocar_hechizo(nombre, argumento, entorno):
    hechizo = entorno.get_funcion(nombre)
    parametros = hechizo.get_args()
    cant_parametros = len(parametros)

    if len(argumento) != cant_parametros:
        raise NameError(f"Error: Debes pasarle {cant_parametros} al hechizo {nombre}.")
    
    for i in range(cant_parametros):
        entorno.set_variable(parametros[i], argumento[i][1])

    ejecutar_bloque(hechizo.get_bloque(), entorno)
    

## Función principal ##

def interpretar(nodo, entorno):

    if nodo is None:
        return None

    if isinstance(nodo, list):
        resultado = None
        for sentencia in nodo:
            resultado = interpretar(sentencia, entorno)
        return resultado

    tipo_nodo = nodo[0]
    ## Funciones ##
    if tipo_nodo == 'encantar':
        interp_imprimir(nodo[1], entorno)

    if tipo_nodo == 'asignacion':
        interp_asignacion(nodo[1], nodo[2], entorno)
    
    if tipo_nodo == 'conjurar':
        interp_repeticion(nodo[1], nodo[2], entorno)

    if tipo_nodo == 'ritual':
        interp_condicional(nodo[1], nodo[2], nodo[3], entorno)
    
    if tipo_nodo == 'hechizo':
        interp_crear_funcion(nodo[1], nodo[2], nodo[3], entorno)

    if tipo_nodo == 'invocar_funcion':
        interp_invocar_hechizo(nodo[1], nodo[2], entorno)


    ## Valores ##
    if tipo_nodo == 'numero':
        return nodo[1]
    
    if tipo_nodo == 'booleano':
        return nodo[1]

    if tipo_nodo == 'id':
        return entorno.get_variable(nodo[1])
    
    if tipo_nodo == 'op_unaria':
        op = nodo[1]
        val = interpretar(nodo[2], entorno)
        if op == 'no': return not val

    if tipo_nodo == 'op_binaria':
        op = nodo[1]
        val_izq = interpretar(nodo[2], entorno)
        val_der = interpretar(nodo[3], entorno)

        # Operadores numéricos
        if op == '+': return val_izq + val_der
        if op == '-': return val_izq - val_der
        if op == '*': return val_izq * val_der
        if op == '/': return val_izq / val_der
        if op == '%': return val_izq % val_der
        # Operadores de comparación
        if op == '==': return val_izq == val_der
        if op == '!=': return val_izq != val_der
        if op == '<':  return val_izq < val_der
        if op == '>':  return val_izq > val_der
        if op == '<=': return val_izq <= val_der
        if op == '>=': return val_izq >= val_der
        # Operadores lógicos
        if op == 'y': return val_izq and val_der
        if op == 'o': return val_izq or val_der
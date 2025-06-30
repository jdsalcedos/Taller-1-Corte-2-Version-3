#Evalua el tipo de expresión
def evaluate_expression(expr, symbol_table):
    """
    Evalúa recursivamente el tipo de una expresión:
      - Literales numéricos (int o float)
      - Variables (busca en symbol_table)
      - Operaciones binarias (tupla (op, left, right))
    Retorna el tipo ('int' o 'float') o lanza SyntaxError si hay un problema.
    """
   # Literal numérico entero o flotante
    if isinstance(expr, bool):
        return 'bool'
    if isinstance(expr, int):
        return 'int'
    elif isinstance(expr, float):
        return 'float'

    # Literal string o char (simulado)
    if isinstance(expr, str):
        if expr.startswith('"') and expr.endswith('"'):
            return 'string'
        elif expr.startswith("'") and expr.endswith("'") and len(expr) == 3:
            return 'char'
        elif expr == 'true' or expr == 'false':
            return 'bool'
        else:
            # Buscar la variable en los ámbitos
            try:
                var_info = lookup_variable(expr)
                return var_info['type']
            except SyntaxError:
                raise SyntaxError(f"Variable '{expr}' no declarada antes de usarse")


     # Operación binaria: ('+', left, right), etc.
    if isinstance(expr, tuple) and len(expr) == 3 and expr[0] == 'CAST':
        _, cast_type, inner_expr = expr
        inner_type = evaluate_expression(inner_expr, symbol_table)

        # Verifica si el cast es válido
        if cast_type == 'int' and inner_type in ('string', 'float', 'char'):
            return 'int'
        elif cast_type == 'float' and inner_type in ('string', 'int', 'char'):
            return 'float'
        elif cast_type == 'string' and inner_type in ('int', 'float', 'char'):
            return 'string'
        elif cast_type == 'bool' and inner_type in ('int', 'float', 'string'):
            return 'bool'
        else:
            raise SyntaxError(f"Conversión inválida: no se puede convertir {inner_type} a {cast_type}")
        
    # Operador unario: negación lógica
    if isinstance(expr, tuple) and len(expr) == 2 and expr[0] == 'NOT':
        _, sub_expr = expr
        sub_type = evaluate_expression(sub_expr, symbol_table)

        if sub_type != 'bool':
            raise SyntaxError(f"Uso inválido del operador '!': se esperaba 'bool' pero se obtuvo '{sub_type}'")
        return 'bool'
    
    if isinstance(expr, tuple) and len(expr) == 2 and expr[0] == 'NOT':
        _, sub_expr = expr
        sub_type = evaluate_expression(sub_expr, symbol_table)

        if sub_type != 'bool':
            raise SyntaxError(f"Uso inválido del operador '!': se esperaba 'bool' pero se obtuvo '{sub_type}'")
        return 'bool'

    # Llamada a función como expresión: ('FUNC_CALL', nombre, [args])
    if isinstance(expr, tuple) and len(expr) == 3 and expr[0] == 'FUNC_CALL':
        _, name, arg_exprs = expr

        if 'functions' not in symbol_table or name not in symbol_table['functions']:
            raise SyntaxError(f"Función '{name}' no declarada")

        expected_params = symbol_table['functions'][name]['params']
        if len(arg_exprs) != len(expected_params):
            raise SyntaxError(f"Número incorrecto de argumentos para función '{name}'")

        for i, (arg_expr, expected_type) in enumerate(zip(arg_exprs, expected_params)):
            actual_type = evaluate_expression(arg_expr, symbol_table)
            if actual_type != expected_type:
                raise SyntaxError(
                    f"Tipo erróneo en argumento {i+1} de '{name}': se esperaba '{expected_type}' pero se obtuvo '{actual_type}'"
                )

        return symbol_table['functions'][name]['return']


        # Compatibilidad de tipos para operaciones comunes
    if isinstance(expr, tuple) and len(expr) == 3:
        op, left, right = expr
        left_type  = evaluate_expression(left, symbol_table)
        right_type = evaluate_expression(right, symbol_table)

        if op == '+':
            # Permitir suma numérica y concatenación string-string
            if left_type == right_type:
                if left_type in ('int', 'float', 'string'):
                    return left_type
                else:
                    raise SyntaxError(f"Operación '+' no soportada para tipo '{left_type}'")
            else:
                # Detectar concatenación inválida entre string y numérico
                if ('string' in (left_type, right_type)) and ('int' in (left_type, right_type) or 'float' in (left_type, right_type)):
                    raise SyntaxError(
                        f"Error semántico: concatenación inválida entre {left_type} y {right_type}"
                    )
                else:
                    raise SyntaxError(
                        f"Tipos incompatibles en operación '+': {left_type} vs {right_type}"
                    )
        elif op in ('-', '*', '/'):
            if left_type == right_type and left_type in ('int', 'float'):
                return left_type
            else:
                raise SyntaxError(
                    f"Tipos incompatibles en operación '{op}': {left_type} vs {right_type}"
                )
            
        # comparaciones relacionales
        elif op in ('==', '!='):
            if left_type != right_type:
                raise SyntaxError(f"Comparación inválida con '{op}': tipos incompatibles {left_type} y {right_type}")
            return 'bool'

        elif op in ('<', '<=', '>', '>='):
            if left_type in ('int', 'float') and right_type in ('int', 'float'):
                return 'bool'
            else:
                raise SyntaxError(f"Comparación inválida con '{op}': se esperaba 'int' o 'float', pero se obtuvo {left_type} y {right_type}")
    
        else:
            raise SyntaxError(f"Operador '{op}' no soportado")

    # Cualquier otro formato no es válido
    raise SyntaxError(f"Expresión semánticamente inválida: {expr}")

def is_valid_identifier(name):
    # Debe ser identificador válido y no comenzar con número
    return name.isidentifier() and not name[0].isdigit()
class SemanticError(Exception):
    pass

#Declaración de funciones
def declare_function(name, param_types, return_type, symbol_table):
    if name in symbol_table["functions"]:
        raise SemanticError(f"Función '{name}' ya declarada")
    symbol_table["functions"][name] = {
        "params": param_types,
        "return": return_type
    }

#Verificación de llamadas a funciones
def check_function_call(name, arg_types, symbol_table):
    funcs = symbol_table["functions"]
    if name not in funcs:
        raise SemanticError(f"Función '{name}' no declarada")
    sig = funcs[name]
    if len(arg_types) != len(sig["params"]):
        raise SemanticError(f"Aridad incorrecta en '{name}'")
    for i, (a, p) in enumerate(zip(arg_types, sig["params"])):
        if a != p:
            raise SemanticError(
                f"Tipo erróneo en arg {i+1} de '{name}': {a} ≠ {p}"
            )
    return sig["return"]

# Estructuras globales para gestión de ámbitos
scope_stack = []  # Pila para rastrear los ámbitos activos
symbol_table = {}  # Tabla de símbolos por ámbito y funciones

# Funciones para manejar ámbitos
def enter_scope(name):
    """Entra en un nuevo ámbito: push y crea entrada en symbol_table."""
    scope_stack.append(name)
    if name not in symbol_table:
        symbol_table[name] = {}

def exit_scope():
    """Sale del ámbito actual."""
    scope_stack.pop()

def current_scope():
    """Devuelve el nombre del ámbito actual."""
    return scope_stack[-1]

def lookup_variable(name):
    """Busca una variable remontando ámbitos desde el más interno al global."""
    for scope in reversed(scope_stack):
        if name in symbol_table.get(scope, {}):
            return symbol_table[scope][name]
    raise SyntaxError(f"Variable '{name}' no declarada en ningún ámbito accesible")

# Declaración de funciones (permanentes en symbol_table['functions'])
def declare_function(name, param_types, return_type):
    funcs = symbol_table['functions']
    if name in funcs:
        raise SemanticError(f"Función '{name}' ya declarada")
    funcs[name] = {'params': param_types, 'return': return_type}

# Declaración de variables en ámbito actual
def declare_variable(name, vtype, is_const=False):
    scope = current_scope()
    table = symbol_table[scope]
    if name in table:
        print(f"Warning: '{name}' shadows a variable en ámbito '{scope}'")
    table[name] = {'type': vtype, 'const': is_const, 'initialized': False, 'used': False}

#Función principal del analizador sintáctico 
def semantic(ast):
    print(ast)
    """
    Realiza el análisis semántico del AST:
      1. Mantiene una tabla de símbolos (name -> tipo).
      2. Verifica que las variables se declaren antes de usarse.
      3. Verifica compatibilidad de tipos en declaraciones y asignaciones.
      4. Verifica identificadores válidos.
      5. Advierte si hay variables no utilizadas.
    Retorna la tabla de símbolos final o lanza SyntaxError si detecta errores.
    """

    # Inicialización global
    # Inicialización global
    symbol_table.clear()
    symbol_table["functions"] = {}
    scope_stack.clear()
    enter_scope("global")

    def mark_used(var_name):
        # Busca la variable en los ámbitos y la marca como usada
        for scope in reversed(scope_stack):
            if scope in symbol_table and var_name in symbol_table[scope]:
                symbol_table[scope][var_name]['used'] = True
                return
    
    def mark_initialized(var_name):
        # Busca la variable en los ámbitos y la marca como inicializada
        for scope in reversed(scope_stack):
            if scope in symbol_table and var_name in symbol_table[scope]:
                symbol_table[scope][var_name]['initialized'] = True
                return

    def evaluate_expression_with_usage(expr, symbol_table):
        # Literales (int, float, string, etc.) — no hacen nada
        if isinstance(expr, (int, float, bool)):
            return

        # Identificadores (variables)
        if isinstance(expr, str):
            # intento resolver en ámbitos
            try:
                var_info = lookup_variable(expr)
            except SyntaxError:
                # si no es variable, lo dejamos pasar si es literal string/char/bool
                if (expr.startswith('"') and expr.endswith('"')) or \
                (expr.startswith("'") and expr.endswith("'") and len(expr) == 3) or \
                expr in ('true', 'false'):
                    return
                else:
                    raise SyntaxError(f"Variable '{expr}' no declarada")
            # si llegó aquí, es variable: marco uso y chequeo inicialización
            mark_used(expr)
            if not var_info.get('initialized', False):
                raise SyntaxError(f"Variable '{expr}' usada antes de ser inicializada")
            return

    # Tuplas (expresiones compuestas)
        elif isinstance(expr, tuple):
            if len(expr) == 3 and expr[0] == 'FUNC_CALL':
                _, name, args = expr

                if 'functions' not in symbol_table or name not in symbol_table['functions']:
                    raise SyntaxError(f"Función '{name}' no declarada")

                expected_params = symbol_table['functions'][name]['params']
                if len(args) != len(expected_params):
                    raise SyntaxError(f"Número incorrecto de argumentos para función '{name}'")

                for arg_expr in args:
                    evaluate_expression_with_usage(arg_expr, symbol_table)

        elif len(expr) == 3 and expr[0] == 'CAST':
            _, _, subexpr = expr
            evaluate_expression_with_usage(subexpr, symbol_table)

        elif len(expr) == 2 and expr[0] == 'NOT':
            _, subexpr = expr
            evaluate_expression_with_usage(subexpr, symbol_table)

        else:
            # Operaciones binarias (op, left, right)
            for subexpr in expr[1:]:
                evaluate_expression_with_usage(subexpr, symbol_table)

    def process_block(block):
        for node in block:
            node_type = node[0]

            if node_type == 'DECLARATION':
                if node[1] == 'const':
                    _, _, var_type, var_name, *rest = node
                    is_const = True
                else:
                    _, var_type, var_name, *rest = node
                    is_const = False

                if not is_valid_identifier(var_name):
                    raise SyntaxError(f"Nombre de variable inválido: '{var_name}'")

                # Verifica que no esté ya en el ámbito actual
                current = current_scope()
                if var_name in symbol_table[current]:
                    raise SyntaxError(f"Variable '{var_name}' ya declarada en ámbito '{current}'")
                symbol_table[current][var_name] = {
                    'type': var_type,
                    'const': is_const,
                    'used': False,
                    'initialized': False
                }

                if rest:
                    expr = rest[0]
                    expr_type = evaluate_expression(expr, symbol_table)
                    if expr_type != var_type:
                        raise SyntaxError(
                            f"Asignación incompatible para '{var_name}': "
                            f"esperado {var_type}, obtenido {expr_type}"
                        )
                    #MARCA en el ámbito correcto ANTES de evaluar usage:
                    symbol_table[current][var_name]['used'] = True
                    symbol_table[current][var_name]['initialized'] = True
                    evaluate_expression_with_usage(expr, symbol_table)
                        
            elif node_type == 'ASSIGNMENT':
                _, var_name, expr = node

                # **AQUÍ**: busca en ámbitos
                var_info = lookup_variable(var_name)

                if var_info['const']:
                    raise SyntaxError(f"No se puede modificar la constante '{var_name}'")

                # **MARCAR** como inicializada ANTES de evaluar la expresión:
                for scope in reversed(scope_stack):
                    if var_name in symbol_table[scope]:
                        symbol_table[scope][var_name]['initialized'] = True
                        symbol_table[scope][var_name]['used'] = True
                        break

                expr_type = evaluate_expression(expr, symbol_table)
                if expr_type != var_info['type']:
                    raise SyntaxError(
                        f"Asignación incompatible para '{var_name}': "
                        f"esperado {var_info['type']}, obtenido {expr_type}"
                    )

                evaluate_expression_with_usage(expr, symbol_table)

            elif node_type == 'IF':
                _, cond_expr, then_block, *else_block = node
                cond_type = evaluate_expression(cond_expr, symbol_table)
                evaluate_expression_with_usage(cond_expr, symbol_table)
                if cond_type != 'bool':
                    raise SyntaxError(
                        f"Condición inválida en 'if': se esperaba 'bool' pero se obtuvo '{cond_type}'"
                    )
                process_block(then_block)
                if else_block:
                    process_block(else_block[0])

            elif node_type == 'WHILE':
                _, cond_expr, body = node
                cond_type = evaluate_expression(cond_expr, symbol_table)
                evaluate_expression_with_usage(cond_expr, symbol_table)
                if cond_type != 'bool':
                    raise SyntaxError(
                        f"Condición inválida en 'while': se esperaba 'bool' pero se obtuvo '{cond_type}'"
                    )
                process_block(body)
            elif node_type == 'FUNC_DECL':
                _, name, param_types, return_type = node
                declare_function(name, param_types, return_type, symbol_table)

            elif node_type == 'FUNC_CALL':
                _, name, arg_exprs = node
                arg_types = [evaluate_expression(expr, {k: v['type'] for k, v in symbol_table.items() if k != 'functions'})
                             for expr in arg_exprs]
                check_function_call(name, arg_types, symbol_table)

            #Control de stack
            elif node_type == 'BLOCK_ENTER':
                enter_scope(f"block_{len(scope_stack)}")
            elif node_type == 'BLOCK_EXIT':
                exit_scope()
            else:

                continue

    process_block(ast)

    # h) Advertencia de variables no usadas
    unused = []
    for scope_name, tbl in symbol_table.items():
        if scope_name == "functions":
            continue
        for name, info in tbl.items():
            if not info['used']:
                unused.append(name)

    if unused:
        print(f"Advertencia: variables no utilizadas: {', '.join(unused)}")

    # i) Error si alguna variable usada no fue inicializada
    for scope_name, tbl in symbol_table.items():
        if scope_name == "functions": continue
        for name, info in tbl.items():
            if info['used'] and not info['initialized']:
                raise SyntaxError(f"Variable '{name}' usada antes de ser inicializada")

    return symbol_table
"""
ast = [
    ("FUNC_DECL", "sumar", ["int", "int"], "int"),
    ("FUNC_CALL", "sumar", [1, 2]),              # OK
    ("FUNC_CALL", "sumar", [1]),                 # Error: aridad incorrecta
    ("FUNC_CALL", "sumar", [1, '"hola"']),         # Error: tipo incorrecto
]
"""
#Para probar funcionamiento correcto de ámbitos (Código válido)
"""
ast = [
    ("BLOCK_ENTER",),
    ("DECLARATION", "int", "x", 1),          # int x = 1
    ("ASSIGNMENT", "x", 1),                  # x = 1 → uso

    ("BLOCK_ENTER",),
    ("DECLARATION", "string", "x", '"hola"'),# string x = "hola" (oculta la anterior)
    ("ASSIGNMENT", "x", '"hola"'),           # x = "hola" → uso local
    ("BLOCK_EXIT",),

    ("ASSIGNMENT", "x", 2),                  # uso de x (global)
    ("BLOCK_EXIT",)
]
"""
#Para probar funcionamiento correcto de ámbitos (Código inválido)
"""
ast = [
    ("BLOCK_ENTER",),

    ("ASSIGNMENT", "x", 5),                #  ERROR: 'x' no ha sido declarada

    ("DECLARATION", "int", "x", 0),

    ("BLOCK_EXIT",)
]

try:
    semantic(ast)
except (SyntaxError, SemanticError) as e:
    print("Error:", e)
"""


def semantic_analyze(ast):
    """
    Función puente que llama a semantic() para mantener compatibilidad con las pruebas
    """
    try:
        semantic(ast)
        return True
    except (SyntaxError, SemanticError) as e:
        if isinstance(e, SemanticError):
            raise e
        else:
            raise SemanticError(str(e))
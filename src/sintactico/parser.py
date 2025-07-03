# -------------------------------------------------------------
# Analizador Sintáctico para Lenguajes de Programación
# Versión 4.0 - Febrero 1, 2025
# Desarrollado por: Ing. Jonathan Torres, Ph.D.
# -------------------------------------------------------------


# Variable global para la última línea procesada
last_token_line = None

# Función principal que maneja el análisis sintáctico
def parser(tokens):
    global last_token_line

    tokens = tokens.copy()
    ast = []

    last_token = tokens[-1]
    last_token_line = last_token[2]

    while tokens:
        # Salta tokens de espacios o saltos de línea si los hubiera (opcional)
        if tokens[0][0] in ('WHITESPACE', 'NEWLINE'):
            tokens.pop(0)
            continue
        try:
            ast.append(parse_statement(tokens))
        except SyntaxError as e:
            raise SyntaxError(str(e))
    return ast # Retorna el árbol de sintaxis abstracta (AST)

# Función para procesar una sentencia del código
def parse_statement(tokens):
    # Sentencia return
    if match_keyword(tokens, 'return'):
        tokens.pop(0)  # Consume 'return'
        expr = parse_expression(tokens)  # Puede ser una constante, una variable, etc.
        parse_semi(tokens)  # Asegura que haya punto y coma
        return ('RETURN', expr)
    
    # Acepta declaraciones con o sin 'const'
    if match_keyword(tokens, 'const') or \
       match_keyword(tokens, 'int') or \
       match_keyword(tokens, 'float') or \
       match_keyword(tokens, 'string') or \
       match_keyword(tokens, 'bool') or \
       match_keyword(tokens, 'char'):
        return parse_declaration(tokens)

    # Si el primer token es 'if', procesamos una estructura condicional
    elif match_keyword(tokens, 'if'):
        return parse_if(tokens)

    # Si el primer token es un identificador, procesamos una asignación
    elif match(tokens, 'IDENTIFIER'):
        return parse_assignment(tokens)

    # Si no es ninguno de los anteriores, es un error de sintaxis
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: sentencia inválida, token inesperado '{val}'")

# Función para procesar una declaración (ejemplo: int a = 5;)
def parse_declaration(tokens):
    # Soporta declaraciones con 'const <tipo> <ident> = <expr>;'
    if match_keyword(tokens, 'const'):
        tokens.pop(0)  # Consume 'const'
        # Ahora debe venir el tipo
        tipo = parse_type(tokens)
        # Ahora debe venir el identificador
        ident = parse_id(tokens)
        # Solo se permite declaración de constante con inicialización obligatoria
        if match(tokens, 'SEMICOLON'):
            tokens.pop(0)
            raise SyntaxError("Una constante debe ser inicializada al declararse")
        parse_equals(tokens)
        expr = parse_expression(tokens)
        parse_semi(tokens)
        return ('DECLARATION', 'const', tipo, ident, expr)
    else:
        tipo = parse_type(tokens)
        ident = parse_id(tokens)
        if match(tokens, 'LPAREN'):
            return parse_function_declaration(tipo, ident, tokens)

        if match(tokens, 'SEMICOLON'):
            tokens.pop(0)
            return ('DECLARATION', tipo, ident)
        
        parse_equals(tokens)
        expr = parse_expression(tokens)
        parse_semi(tokens)
        return ('DECLARATION', tipo, ident, expr)
    
# Función para procesar una asignación, por ejemplo: 'a = 5'
def parse_assignment(tokens):
    # Procesar el identificador (ej. 'a')
    ident = parse_id(tokens)
    
    # Procesar el operador de asignación ('=')
    parse_equals(tokens)
    
    # Procesar la expresión del lado derecho de la asignación (ej. '5')
    expr = parse_expression(tokens)
    
    # Procesar el punto y coma al final
    parse_semi(tokens)
    
    # Retornar la estructura de la asignación
    return ('ASSIGNMENT', ident, expr)

# Función para procesar una estructura condicional 'if' con soporte para 'else'
def parse_if(tokens):
    # Verificamos si el primer token es la palabra clave 'if'
    expect_keyword(tokens, 'if')

    # Guardamos la información de la línea y columna del 'if' para mostrarla en caso de error
    if_line, if_col = tokens[0][2], tokens[0][3]

    # Espera el paréntesis de apertura '('
    expect(tokens, 'LPAREN')

    # Procesa la expresión dentro de los paréntesis
    cond = parse_expression(tokens)

    # Espera el paréntesis de cierre ')'
    expect(tokens, 'RPAREN')
    
    # Espera la llave de apertura '{'
    expect(tokens, 'LBRACE')

    then_block = [('BLOCK_ENTER',)]  # Marcar entrada al bloque then
    # Procesar sentencias dentro del bloque if
    while tokens and not match(tokens, 'RBRACE'):
        then_block.append(parse_statement(tokens))
    then_block.append(('BLOCK_EXIT',))  # Marcar salida del bloque then

    # Si no hemos encontrado la llave de cierre 'RBRACE' y ya no quedan tokens, lanzar error
    if not match(tokens, 'RBRACE'):
        raise SyntaxError(f"Error en línea {if_line}, columna {if_col}: falta '}}' de cierre en el bloque 'if'")

    # Consumir la llave de cierre 'RBRACE'
    tokens.pop(0)

    # Verificar si hay un 'else'
    else_block = None
    if tokens and match_keyword(tokens, 'else'):
        tokens.pop(0)  # Consume 'else'
        
        # Espera la llave de apertura '{'
        expect(tokens, 'LBRACE')
        
        else_block = [('BLOCK_ENTER',)]  # Marcar entrada al bloque else
        # Procesar sentencias dentro del bloque else
        while tokens and not match(tokens, 'RBRACE'):
            else_block.append(parse_statement(tokens))
        else_block.append(('BLOCK_EXIT',))  # Marcar salida del bloque else
        
        # Si no hemos encontrado la llave de cierre 'RBRACE' y ya no quedan tokens, lanzar error
        if not match(tokens, 'RBRACE'):
            raise SyntaxError(f"Error en línea {if_line}, columna {if_col}: falta '}}' de cierre en el bloque 'else'")
        
        # Consumir la llave de cierre 'RBRACE'
        tokens.pop(0)

    # Retorna la estructura del bloque 'if' con su condición, bloque then y bloque else (si existe)
    if else_block is not None:
        return ('IF_ELSE', cond, then_block, else_block)
    else:
        return ('IF', cond, then_block)

# Función para procesar expresiones, que son comparaciones o operaciones
def parse_expression(tokens):
    return parse_comparison(tokens)

# Función para procesar expresiones de comparación (ejemplo: 'x > 5', 'y == 3')
def parse_comparison(tokens):
    # Primero procesamos las operaciones de adición y sustracción
    left = parse_add_sub(tokens)

    # Mientras encontremos un operador de comparación ('>', '<', '==', '>=', '<=')
    while match(tokens, 'GREATER') or match(tokens, 'LESS') or match(tokens, 'EQUALS') or match(tokens, 'GREATEREQUAL') or match(tokens, 'LESSEQUAL'):
        _, op, _, _ = tokens.pop(0)  # Consumimos el operador de comparación
        # Procesamos la expresión de la derecha de la comparación
        right = parse_add_sub(tokens)
        # Retornamos la comparación estructurada
        left = (op, left, right)

    return left

# Función para procesar operaciones de adición y sustracción
def parse_add_sub(tokens):
    # Primero procesamos las multiplicaciones y divisiones
    left = parse_mul_div(tokens)
    # Mientras encontremos un operador de adición o sustracción
    while match(tokens, 'OPERATOR', '+') or match(tokens, 'OPERATOR', '-'):
        _, op, _, _ = tokens.pop(0)  # Consumimos el operador
        # Procesamos la expresión de la derecha
        right = parse_mul_div(tokens)
        # Retornamos la expresión con el operador aplicado
        left = (op, left, right)
    return left

# Función para procesar operaciones de multiplicación y división
def parse_mul_div(tokens):
    # Procesamos el primer operando
    left = parse_unary(tokens)
    # Mientras encontremos un operador de multiplicación o división
    while match(tokens, 'OPERATOR', '*') or match(tokens, 'OPERATOR', '/'):
        _, op, _, _ = tokens.pop(0)  # Consumimos el operador
        # Procesamos el operando de la derecha
        right = parse_unary(tokens)
        # Retornamos la expresión con el operador aplicado
        left = (op, left, right)

    return left

# Función para procesar los operandos primarios (números, identificadores o paréntesis)
def parse_primary(tokens):
    # Si encontramos un paréntesis de apertura, procesamos la expresión entre paréntesis
    if match(tokens, 'LPAREN'):
        tokens.pop(0)
        expr = parse_expression(tokens)
        # Verificamos que haya un paréntesis de cierre correspondiente
        if not match(tokens, 'RPAREN'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba RPAREN ')' pero se encontró '{val}'")
        tokens.pop(0)  # Consumimos 'RPAREN'
        return expr

    # Si encontramos un número, lo procesamos
    elif match(tokens, 'NUMBER'):
        return parse_num(tokens)
    
        # Si encontramos una cadena, la procesamos
    elif match(tokens, 'STRING'):
        return parse_string(tokens)

    # Si encontramos un carácter, lo procesamos
    elif match(tokens, 'CHAR'):
        return parse_char(tokens)

        # Soporte para cast explícito como int("5") o float("3.14")
    elif match_keyword(tokens, 'int') or match_keyword(tokens, 'float') or match_keyword(tokens, 'string'):
        cast_type = tokens.pop(0)[1]  # Extrae 'int', 'float' o 'string'

        # Verifica que lo siguiente sea un paréntesis de apertura
        if not match(tokens, 'LPAREN'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba '(' después de cast a {cast_type}")
        
        tokens.pop(0)  # Consumimos '('
        expr = parse_expression(tokens)  # Parseamos la expresión interna

        if not match(tokens, 'RPAREN'):
            tipo, val, line, col = tokens[0]
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ')' al cerrar cast a {cast_type}")
        
        tokens.pop(0)  # Consumimos ')'

        return ('CAST', cast_type, expr)

    # Si encontramos un identificador, lo procesamos
    elif match(tokens, 'IDENTIFIER'):
        name = parse_id(tokens)
        if match(tokens, 'LPAREN'):
            tokens.pop(0)  # Consumir '('
            args = []
            if not match(tokens, 'RPAREN'):
                while True:
                    arg = parse_expression(tokens)
                    args.append(arg)
                    if match(tokens, 'COMMA'):
                        tokens.pop(0)
                    else:
                        break
            if not match(tokens, 'RPAREN'):
                tipo, val, line, col = tokens[0]
                raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ')' al final de llamada a función")
            tokens.pop(0)  # Consumir ')'
            return ('FUNC_CALL', name, args)
        else:
            return name

    # Si encontramos un operador de comparación '==', lanzamos un error
    elif match(tokens, 'OPERATOR') and tokens[0][1] == '==':
        _, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: expresión no puede comenzar con '=='")
    
    elif match_keyword(tokens, 'false'):
        tokens.pop(0)
        return False  # O ('bool', False) si quieres mantener consistencia
    
    elif match_keyword(tokens, 'true'):
        tokens.pop(0)
        return True

    # Si no encontramos un token esperado, lanzamos un error
    else:
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: token inesperado '{val}' en expresión")


# === FUNCIONES AUXILIARES ===

# Variable global para almacenar la última línea procesada en el analizador.
last_token_line = None

# Función para procesar un tipo de dato (int, float)
def parse_type(tokens):
    global last_token_line  # Accede a la variable global para la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba tipo, pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens.pop(0)  # Extrae el primer token de la lista.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica si el tipo de token es válido en este contexto.
    if tipo == 'KEYWORD' and val in ('int', 'float', 'string', 'bool', 'char'):
        return val
    
    # Si no es un tipo válido, lanza un error especificando la línea y columna.
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un tipo válido, pero se encontró '{val}'")

# Función para procesar un identificador (como variables o nombres de funciones)
def parse_id(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay tokens disponibles, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba identificador, pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens.pop(0)  # Extrae el primer token de la lista.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica si el token es un identificador válido.
    if tipo == 'IDENTIFIER':
        return val
    
    # Si el token no es un identificador válido, lanza un error con la línea y columna.
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba identificador, pero se encontró '{val}'")

# Función para procesar números (entero o decimal)
def parse_num(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba número, pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens.pop(0)  # Extrae el primer token de la lista.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Si el token es un número, lo procesa como entero o decimal según corresponda.
    if tipo == 'NUMBER':
        return float(val) if '.' in val else int(val)
    
    # Si el token no es un número válido, lanza un error con la línea y columna.
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un número válido, pero se encontró '{val}'")

# Función para procesar el operador de asignación '='
def parse_equals(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba '=', pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica que el token sea un operador '='.
    if tipo != 'OPERATOR' or val != '=':
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba '=', pero se encontró '{val}'.")
    
    tokens.pop(0)  # Consume el operador '='.

# Función para procesar el punto y coma ';' al final de las instrucciones
def parse_semi(tokens):
    global last_token_line  # Accede a la variable global de la última línea procesada.

    # Si no hay más tokens, lanza un error especificando la última línea conocida.
    if not tokens:
        raise SyntaxError(f"Error en línea {last_token_line}: se esperaba ';', pero no se encontró más tokens.")
    
    tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token.
    last_token_line = line  # Actualiza la última línea procesada con la línea actual.

    # Verifica que el token sea un punto y coma ';'.
    if tipo != 'SEMICOLON':
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ';', pero se encontró '{val}'.")
    
    tokens.pop(0)  # Consume el punto y coma ';'.


# Función para procesar cadenas de texto
def parse_string(tokens):
    tipo, val, line, col = tokens.pop(0)
    # Asegurarse que la cadena esté entre comillas dobles
    if tipo == 'STRING':
        return val  # Retorna el valor de la cadena
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba una cadena pero se encontró '{val}'")

# Función para procesar caracteres
def parse_char(tokens):
    tipo, val, line, col = tokens.pop(0)
    # Asegurarse que el carácter esté entre comillas simples
    if tipo == 'CHAR':
        return val  # Retorna el valor del carácter
    raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba un carácter pero se encontró '{val}'")

# Función para hacer coincidir un tipo de token y valor específico
def match(tokens, type_, value=None):
    if not tokens:
        return False
    tk_type, tk_val, *_ = tokens[0]  # Obtiene el tipo y valor del primer token
    return tk_type == type_ and (value is None or tk_val == value)

# Función para verificar si el token actual es una palabra clave
def match_keyword(tokens, keyword):
    if not tokens:
        return False
    tk_type, tk_val, *_ = tokens[0]  # Obtiene el tipo y valor del primer token
    return tk_type == 'KEYWORD' and tk_val == keyword

# Función para esperar un token específico
def expect(tokens, type_, value=None):
    if not match(tokens, type_, value):
        if tokens:
            tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba {type_} '{value}' pero se encontró '{val}'")
        else:
            raise SyntaxError(f"Error: se esperaba {type_} '{value}' pero se encontró EOF")
    tokens.pop(0)  # Consume el token esperado

# Función para esperar una palabra clave específica
def expect_keyword(tokens, keyword):
    if not match_keyword(tokens, keyword):
        if tokens:
            tipo, val, line, col = tokens[0]  # Obtiene el tipo y valor del primer token
            raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba palabra clave '{keyword}' pero se encontró '{val}'")
        else:
            raise SyntaxError(f"Error: se esperaba palabra clave '{keyword}' pero se encontró EOF")
    tokens.pop(0)  # Consume la palabra clave esperada

def parse_unary(tokens):
    if match(tokens, 'OPERATOR') and tokens[0][1] == '!':
        _, val, line, col = tokens.pop(0)  # consumimos '!'
        operand = parse_unary(tokens)  # recursivo por si hay múltiples '!'
        return ('NOT', operand)
    else:
        return parse_primary(tokens)
    
def parse_function_definition(tokens):
    tipo = parse_type(tokens)              # int
    name = parse_id(tokens)                # sumar
    expect(tokens, 'LPAREN')               # (
    params = []

    while not match(tokens, 'RPAREN'):     # mientras no llegue el ')'
        param_type = parse_type(tokens)    # int
        param_name = parse_id(tokens)      # a
        params.append((param_type, param_name))
        if match(tokens, 'COMMA'):
            tokens.pop(0)

    expect(tokens, 'RPAREN')               # )
    expect(tokens, 'LBRACE')               # {
    body = []

    while not match(tokens, 'RBRACE'):
        stmt = parse_statement(tokens)     # cuerpo
        body.append(stmt)
    
    expect(tokens, 'RBRACE')               # }

    return ('FUNCTION_DEF', tipo, name, params, body)

def parse_function_declaration(return_type, name, tokens):
    tokens.pop(0)  # Consumir '('
    param_types = []

    if not match(tokens, 'RPAREN'):
        while True:
            param_type = parse_type(tokens)
            param_name = parse_id(tokens)
            param_types.append(param_type)
            if match(tokens, 'COMMA'):
                tokens.pop(0)
            else:
                break

    if not match(tokens, 'RPAREN'):
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba ')' en la declaración de la función")
    tokens.pop(0)  # Consumir ')'

    # Consumir el bloque de la función, aunque no lo procesemos
    if not match(tokens, 'LBRACE'):
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba '{{' en la declaración de la función")
    
    brace_count = 1
    tokens.pop(0)  # Consumir '{'
    while brace_count > 0:
        if not tokens:
            raise SyntaxError("Se esperaba '}' al final del cuerpo de la función")
        tok_type, tok_val, *_ = tokens.pop(0)
        if tok_type == 'LBRACE':
            brace_count += 1
        elif tok_type == 'RBRACE':
            brace_count -= 1

    return ('FUNC_DECL', name, param_types, return_type)


def parse_block(tokens):
    if not match(tokens, 'LBRACE'):
        tipo, val, line, col = tokens[0]
        raise SyntaxError(f"Error en línea {line}, columna {col}: se esperaba '{{' para iniciar el bloque de función")
    
    tokens.pop(0)  # Consumimos '{'
    statements = []

    # Repetimos hasta encontrar '}'
    while not match(tokens, 'RBRACE'):
        stmt = parse_statement(tokens)
        statements.append(stmt)

    tokens.pop(0)  # Consumimos '}'
    return ('BLOCK', statements)



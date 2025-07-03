#!/usr/bin/env python3
"""
Generador de Código Intermedio para Lenguajes de Programación
Versión 1.0 - Febrero 1, 2025

Este módulo recorre el AST y genera código intermedio en formato de cuádruplas.
El código intermedio es una representación más cercana al código máquina pero
aún independiente de la arquitectura del procesador.
"""

class CodeGenerator:
    """
    Generador de código intermedio que convierte un AST en cuádruplas.
    Las cuádruplas tienen el formato: (resultado, operador, operando1, operando2)
    """
    
    def __init__(self):
        self.temp_counter = 0  # Contador para variables temporales
        self.label_counter = 0  # Contador para etiquetas
        self.code = []  # Lista de cuádruplas generadas
        
    def new_temp(self):
        """Genera una nueva variable temporal (t1, t2, t3, ...)"""
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self):
        """Genera una nueva etiqueta (L1, L2, L3, ...)"""
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, result, op, arg1=None, arg2=None):
        """
        Emite una cuádrupla al código intermedio.
        
        Args:
            result: Variable donde se almacena el resultado
            op: Operador o instrucción
            arg1: Primer operando (opcional)
            arg2: Segundo operando (opcional)
        """
        quad = (result, op, arg1, arg2)
        self.code.append(quad)
        return result
    
    def generate_expression(self, expr):
        """
        Genera código intermedio para una expresión.
        Retorna la variable temporal que contiene el resultado.
        
        Args:
            expr: Expresión del AST (número, string, variable, o tupla de operación)
            
        Returns:
            str: Variable temporal con el resultado
        """
        # Casos base: literales
        if isinstance(expr, (int, float)):
            temp = self.new_temp()
            self.emit(temp, '=', expr, None)
            return temp
            
        elif isinstance(expr, str):
            # Verificar si es un literal string o una variable
            if expr.startswith('"') and expr.endswith('"'):
                # Es un literal string
                temp = self.new_temp()
                self.emit(temp, '=', expr, None)
                return temp
            elif expr.startswith("'") and expr.endswith("'"):
                # Es un literal char
                temp = self.new_temp()
                self.emit(temp, '=', expr, None)
                return temp
            elif expr in ('true', 'false'):
                # Es un literal booleano
                temp = self.new_temp()
                self.emit(temp, '=', expr, None)
                return temp
            else:
                # Es una variable, la devolvemos directamente
                return expr
                
        elif isinstance(expr, bool):
            # Literal booleano en Python
            temp = self.new_temp()
            value = 'true' if expr else 'false'
            self.emit(temp, '=', value, None)
            return temp
            
        # Casos complejos: operaciones
        elif isinstance(expr, tuple):
            if len(expr) == 2 and expr[0] == 'NOT':
                # Operador unario NOT
                _, operand = expr
                operand_temp = self.generate_expression(operand)
                result_temp = self.new_temp()
                self.emit(result_temp, '!', operand_temp, None)
                return result_temp
                
            elif len(expr) == 3 and expr[0] == 'CAST':
                # Conversión de tipo (cast)
                _, cast_type, inner_expr = expr
                operand_temp = self.generate_expression(inner_expr)
                result_temp = self.new_temp()
                self.emit(result_temp, f'cast_{cast_type}', operand_temp, None)
                return result_temp
                
            elif len(expr) == 3 and expr[0] == 'FUNC_CALL':
                # Llamada a función
                _, func_name, args = expr
                
                # Generar código para argumentos
                arg_temps = []
                for arg in args:
                    arg_temp = self.generate_expression(arg)
                    arg_temps.append(arg_temp)
                
                # Emitir llamadas param para cada argumento
                for arg_temp in arg_temps:
                    self.emit(None, 'param', arg_temp, None)
                
                # Emitir llamada a función
                result_temp = self.new_temp()
                self.emit(result_temp, 'call', func_name, len(args))
                return result_temp
                
            elif len(expr) == 3:
                # Operación binaria: (op, left, right)
                op, left, right = expr
                
                # Generar código para operandos
                left_temp = self.generate_expression(left)
                right_temp = self.generate_expression(right)
                
                # Generar código para la operación
                result_temp = self.new_temp()
                self.emit(result_temp, op, left_temp, right_temp)
                return result_temp
        
        # Caso no manejado
        raise ValueError(f"Expresión no reconocida en generación de código: {expr}")
    
    def generate_statement(self, stmt):
        """
        Genera código intermedio para una sentencia.
        
        Args:
            stmt: Sentencia del AST
        """
        if not isinstance(stmt, tuple):
            raise ValueError(f"Sentencia inválida: {stmt}")
            
        stmt_type = stmt[0]
        
        if stmt_type == 'DECLARATION':
            if len(stmt) == 4:
                # Declaración con inicialización: ('DECLARATION', tipo, nombre, expr)
                _, var_type, var_name, init_expr = stmt
                expr_temp = self.generate_expression(init_expr)
                self.emit(var_name, '=', expr_temp, None)
                
            elif len(stmt) == 5 and stmt[1] == 'const':
                # Declaración de constante: ('DECLARATION', 'const', tipo, nombre, expr)
                _, _, var_type, var_name, init_expr = stmt
                expr_temp = self.generate_expression(init_expr)
                self.emit(var_name, '=', expr_temp, None)
                
            elif len(stmt) == 3:
                # Declaración sin inicialización: ('DECLARATION', tipo, nombre)
                _, var_type, var_name = stmt
                # No generamos código para declaraciones sin inicialización
                pass
            
        elif stmt_type == 'ASSIGNMENT':
            # Asignación: ('ASSIGNMENT', variable, expr)
            _, var_name, expr = stmt
            expr_temp = self.generate_expression(expr)
            self.emit(var_name, '=', expr_temp, None)
            
        elif stmt_type == 'IF':
            # Estructura condicional: ('IF', condición, bloque)
            _, condition, then_block = stmt
            
            # Generar código para la condición
            cond_temp = self.generate_expression(condition)
            
            # Generar etiquetas
            else_label = self.new_label()
            end_label = self.new_label()
            
            # Salto condicional
            self.emit(None, 'if_false', cond_temp, else_label)
            
            # Generar código del bloque then
            for stmt in then_block:
                self.generate_statement(stmt)
            
            # Salto al final
            self.emit(None, 'goto', end_label, None)
            
            # Etiqueta else (aunque no haya else)
            self.emit(else_label, 'label', None, None)
            
            # Etiqueta de fin
            self.emit(end_label, 'label', None, None)
            
        elif stmt_type == 'IF_ELSE':
            # Estructura condicional: ('IF_ELSE', condición, bloque_then, bloque_else)
            _, condition, then_block, else_block = stmt
            
            # Generar código para la condición
            cond_temp = self.generate_expression(condition)
            
            # Generar etiquetas
            else_label = self.new_label()
            end_label = self.new_label()
            
            # Salto condicional al else
            self.emit(None, 'if_false', cond_temp, else_label)
            
            # Generar código del bloque then
            for stmt in then_block:
                self.generate_statement(stmt)
            
            # Salto al final (saltando el else)
            self.emit(None, 'goto', end_label, None)
            
            # Etiqueta del else
            self.emit(else_label, 'label', None, None)
            
            # Generar código del bloque else
            for stmt in else_block:
                self.generate_statement(stmt)
            
            # Etiqueta de fin
            self.emit(end_label, 'label', None, None)
            
        elif stmt_type == 'WHILE':
            # Bucle while: ('WHILE', condición, bloque)
            _, condition, body_block = stmt
            
            # Generar etiquetas
            start_label = self.new_label()
            end_label = self.new_label()
            
            # Etiqueta de inicio del bucle
            self.emit(start_label, 'label', None, None)
            
            # Generar código para la condición
            cond_temp = self.generate_expression(condition)
            
            # Salto condicional de salida
            self.emit(None, 'if_false', cond_temp, end_label)
            
            # Generar código del cuerpo
            for stmt in body_block:
                self.generate_statement(stmt)
            
            # Salto de vuelta al inicio
            self.emit(None, 'goto', start_label, None)
            
            # Etiqueta de fin
            self.emit(end_label, 'label', None, None)
            
        elif stmt_type == 'RETURN':
            # Sentencia return: ('RETURN', expr)
            _, expr = stmt
            if expr is not None:
                expr_temp = self.generate_expression(expr)
                self.emit(None, 'return', expr_temp, None)
            else:
                self.emit(None, 'return', None, None)
                
        elif stmt_type == 'FUNC_CALL':
            # Llamada a función como sentencia
            self.generate_expression(stmt)
            
        elif stmt_type == 'BLOCK_ENTER':
            # Marca de entrada de bloque - ignorar en generación de código
            pass
            
        elif stmt_type == 'BLOCK_EXIT':
            # Marca de salida de bloque - ignorar en generación de código
            pass
            
        else:
            raise ValueError(f"Tipo de sentencia no reconocido: {stmt_type}")
    
    def generate(self, ast):
        """
        Genera código intermedio para todo el AST.
        
        Args:
            ast: Lista de sentencias del AST
            
        Returns:
            list: Lista de cuádruplas del código intermedio
        """
        self.code = []  # Reiniciar el código
        self.temp_counter = 0
        self.label_counter = 0
        
        for stmt in ast:
            self.generate_statement(stmt)
        
        return self.code
    
    def print_code(self):
        """Imprime el código intermedio de forma legible."""
        print("=== CÓDIGO INTERMEDIO ===")
        for i, quad in enumerate(self.code):
            result, op, arg1, arg2 = quad
            
            if op == 'label':
                print(f"{i:3d}: {result}:")
            elif op == 'goto':
                print(f"{i:3d}: goto {arg1}")
            elif op == 'if_false':
                print(f"{i:3d}: if_false {arg1} goto {arg2}")
            elif op == 'return':
                if arg1:
                    print(f"{i:3d}: return {arg1}")
                else:
                    print(f"{i:3d}: return")
            elif op == 'param':
                print(f"{i:3d}: param {arg1}")
            elif op == 'call':
                print(f"{i:3d}: {result} = call {arg1}, {arg2}")
            elif arg2 is None:
                if arg1 is None:
                    print(f"{i:3d}: {result} {op}")
                else:
                    print(f"{i:3d}: {result} = {op} {arg1}")
            else:
                print(f"{i:3d}: {result} = {arg1} {op} {arg2}")


def generate_intermediate_code(ast):
    """
    Función principal para generar código intermedio desde un AST.
    
    Args:
        ast: AST generado por el parser
        
    Returns:
        list: Lista de cuádruplas del código intermedio
    """
    generator = CodeGenerator()
    return generator.generate(ast)


def print_intermediate_code(code):
    """
    Imprime código intermedio de forma legible.
    
    Args:
        code: Lista de cuádruplas
    """
    print("=== CÓDIGO INTERMEDIO ===")
    for i, quad in enumerate(code):
        result, op, arg1, arg2 = quad
        print(f"{i:3d}: ({result}, {op}, {arg1}, {arg2})")


# Función de ejemplo/prueba
if __name__ == "__main__":
    # Ejemplo de uso
    print("🔧 GENERADOR DE CÓDIGO INTERMEDIO")
    print("=" * 50)
    
    # AST de ejemplo: int a = 5 + 2;
    ast_ejemplo = [
        ('DECLARATION', 'int', 'a', ('+', 5, 2))
    ]
    
    print("AST de entrada:")
    print(ast_ejemplo)
    
    # Generar código intermedio
    generator = CodeGenerator()
    codigo_intermedio = generator.generate(ast_ejemplo)
    
    print("\nCódigo intermedio generado:")
    generator.print_code()
    
    print(f"\nCuádruplas generadas: {len(codigo_intermedio)}")

#!/usr/bin/env python3
"""
Configuración y utilidades del compilador
"""

import sys
import os

# Configuración de paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
TESTS_PATH = os.path.join(PROJECT_ROOT, 'tests')

# Agregar paths al sistema
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def setup_paths():
    """Configura los paths necesarios para el proyecto"""
    paths = [PROJECT_ROOT, SRC_PATH, TESTS_PATH]
    for path in paths:
        if path not in sys.path:
            sys.path.insert(0, path)

def get_compiler_modules():
    """
    Importa y retorna todos los módulos del compilador
    
    Returns:
        tuple: (lexer, parser, semantic, CodeGenerator)
    """
    setup_paths()
    
    from src.lexico.lexer import lexer
    from src.sintactico.parser import parser
    from src.semantico.semantic import semantic
    from src.generador.code_generator import CodeGenerator
    
    return lexer, parser, semantic, CodeGenerator

def compile_code(source_code):
    """
    Función de conveniencia para compilar código
    
    Args:
        source_code (str): Código fuente a compilar
        
    Returns:
        list: Lista de cuádruplas generadas
    """
    lexer, parser, semantic, CodeGenerator = get_compiler_modules()
    
    tokens = lexer(source_code)
    ast = parser(tokens)
    semantic(ast)
    generator = CodeGenerator()
    return generator.generate(ast)

# Configurar paths al importar este módulo
setup_paths()

#!/usr/bin/env python3
"""
Archivo principal del compilador
Demuestra el uso del pipeline completo de compilación
"""

import sys
import os

# Agregar el directorio actual al path para los imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.lexico.lexer import lexer
from src.sintactico.parser import parser
from src.semantico.semantic import semantic
from src.generador.code_generator import CodeGenerator

def compilar(codigo):
    """
    Función principal que ejecuta todo el pipeline de compilación
    
    Args:
        codigo (str): Código fuente a compilar
        
    Returns:
        list: Lista de cuádruplas generadas
        
    Raises:
        Exception: Si hay errores en cualquier fase
    """
    print("🚀 INICIANDO COMPILACIÓN")
    print("=" * 50)
    print(f"📝 Código fuente: {codigo}")
    print()
    
    try:
        # Fase 1: Análisis Léxico
        print("🔍 FASE 1: Análisis Léxico")
        tokens = lexer(codigo)
        print(f"   ✅ {len(tokens)} tokens generados")
        print(f"   📝 Tokens: {tokens}")
        print()
        
        # Fase 2: Análisis Sintáctico
        print("🌳 FASE 2: Análisis Sintáctico")
        ast = parser(tokens)
        print(f"   ✅ AST generado correctamente")
        print(f"   📝 AST: {ast}")
        print()
        
        # Fase 3: Análisis Semántico
        print("🧠 FASE 3: Análisis Semántico")
        symbol_table = semantic(ast)
        print(f"   ✅ Análisis semántico exitoso")
        print()
        
        # Fase 4: Generación de Código Intermedio
        print("⚙️  FASE 4: Generación de Código Intermedio")
        generator = CodeGenerator()
        cuadruplas = generator.generate(ast)
        print(f"   ✅ {len(cuadruplas)} cuádruplas generadas")
        print()
        
        print("📊 CUÁDRUPLAS RESULTANTES:")
        print("-" * 50)
        for i, cuadrupla in enumerate(cuadruplas, 1):
            print(f"   {i:2d}: {cuadrupla}")
        
        print(f"\n✅ COMPILACIÓN EXITOSA")
        return cuadruplas
        
    except Exception as e:
        print(f"❌ ERROR EN COMPILACIÓN: {e}")
        raise

def main():
    """
    Función principal con ejemplos de uso
    """
    print("🔥 COMPILADOR SIMPLE - DEMO")
    print("=" * 60)
    
    # Ejemplos de código a compilar
    ejemplos = [
        "int a = 5 + 2;",
        "int x = 10; int y = 20; int suma = x + y;",
        "bool activo = !false;",
        "float pi = 3.14; float radio = 2.5; float area = pi * radio;",
        "int x = 15; if (x > 10) { int mayor = x + 1; }"
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{'='*60}")
        print(f"EJEMPLO {i}")
        print(f"{'='*60}")
        
        try:
            cuadruplas = compilar(ejemplo)
            print(f"✅ Ejemplo {i} compilado exitosamente")
        except Exception as e:
            print(f"❌ Error en ejemplo {i}: {e}")
        
        print()

if __name__ == "__main__":
    # Verificar si se pasó código como argumento
    if len(sys.argv) > 1:
        codigo_usuario = " ".join(sys.argv[1:])
        print("🎯 COMPILANDO CÓDIGO DEL USUARIO")
        print("=" * 60)
        try:
            compilar(codigo_usuario)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        main()

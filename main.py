#!/usr/bin/env python3
"""
Archivo principal del compilador
Demuestra el uso del pipeline completo de compilación con menú de depuración
"""

import sys
import os
from pprint import pprint
from tests import tests_compiler

# Agregar el directorio actual al path para los imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.lexico.lexer import lexer
from src.sintactico.parser import parser
from src.semantico.semantic import semantic
from src.generador.code_generator import CodeGenerator
from src.CodigoObjeto.codigob import CodeGeneratorob
from src.VM.virtualmachine import VirtualMachine

def prompt_menu():
    """
    Muestra el menú de opciones y devuelve el set de fases seleccionadas.
      1) Tokens
      2) AST
      3) Semántico (tabla de símbolos)
      4) Código intermedio
      5) Código objeto
      6) Ejecutar en VM
    """
    print("Selecciona las fases que quieres mostrar (separadas por comas):")
    print(" 1) Tokens")
    print(" 2) AST")
    print(" 3) Semántico (tabla de símbolos)")
    print(" 4) Código intermedio (cuádruplas)")
    print(" 5) Código objeto")
    print(" 6) Ejecutar en VM")
    raw = input("Tu selección [ej. 1,2,4]: ")
    opts = set()
    for part in raw.split(','):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= 6:
            opts.add(int(part))
    return opts

#En esta función compilar se da la integración de todas las fases
def compilar(codigo, options):
    """
    Ejecuta todo el pipeline y muestra únicamente las fases seleccionadas.
    
    Args:
        codigo (str): Código fuente a compilar
        options (set[int]): Conjunto de fases a imprimir
    """
    # 1) Léxico
    tokens = lexer(codigo) # ← llamada al lexer
    if 1 in options:
        print("\n--- FASE 1: ANÁLISIS LÉXICO ---")
        print(f"Tokens ({len(tokens)}):")
        for t in tokens:
            print(f"  {t}")

    # 2) Sintáctico
    ast = parser(tokens) # ← llamada al parser
    if 2 in options:
        print("\n--- FASE 2: ANÁLISIS SINTÁCTICO ---")
        print("AST:")
        for node in ast:
            print(f"  {node}")

    # 3) Semántico
    try:
        symbol_table = semantic(ast) # ← llamada al analizador semántico
        if 3 in options:
            print("\n--- FASE 3: ANÁLISIS SEMÁNTICO ---")
            print("Tabla de símbolos resultante:")
            pprint(symbol_table)
    except Exception as e:
        print(f"\n[ERROR SEMÁNTICO] {e}")
        raise

    # 4) Código intermedio
    icg = CodeGenerator()
    quads = icg.generate(ast) # ← generación de cuádruplas
    if 4 in options:
        print("\n--- FASE 4: CÓDIGO INTERMEDIO (CUÁDRUPLAS) ---")
        for i, q in enumerate(quads, 1):
            print(f"  {i:2d}: {q}")

    # 5) Objeto (ensamblador)
    ocg = CodeGeneratorob()
    ocg.generate_code(quads)  # ← conversión a código objeto (ensamblador)
    asm = ocg.get_code()
    if 5 in options:
        print("\n--- FASE 5: CÓDIGO OBJETO---")
        print(asm)

    # 6) Ejecutar en VM
    if 6 in options:
        print("\n--- FASE 6: EJECUCIÓN EN VM ---")
        vm = VirtualMachine()
        vm.load_program(asm)  # ← carga y ejecución en la máquina virtual
        vm.run()
        print(f">> Pila (cima): {vm.get_final_stack_top()}")
        print(f">> Memoria: {vm.get_memory_state()}")

def main():
    print("COMPILADOR SIMPLE - MENÚ DE DEPURACIÓN")
    print("=" * 60)
    
    # 1) Selección de fases
    options = prompt_menu()
    if not options:
        print("No seleccionaste ninguna fase. Saliendo.")
        return

    # 2) Correr los tests definidos en tests_simple.TEST_CASES
    for idx, caso in enumerate(tests_compiler.TEST_CASES, start=1):
        print(f"\n{'='*60}")
        print(f"TEST {idx}: {caso['name']} — {caso['description']}")
        print(f"Esperado: {'ÉXITO' if caso['expect_success'] else 'FALLO'}")
        print("-" * 60)
        print(caso["code"])
        try:
            compilar(caso["code"], options)
            resultado = True
        except Exception:
            resultado = False

        correcto = (resultado == caso["expect_success"])
        estado = "✅ OK" if correcto else "❌ ERROR"
        print(f"\nResultado obtenido: {'ÉXITO' if resultado else 'FALLO'} — {estado}")

    print("\n" + "="*60)
    print("FIN DE EJECUCIÓN DE TESTS")

if __name__ == "__main__":
    main()

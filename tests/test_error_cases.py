#!/usr/bin/env python3
"""
Pruebas específicas para casos de error y manejo de excepciones
Este archivo se enfoca exclusivamente en casos que DEBEN fallar
"""

import sys
import os

# Agregar el directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexico.lexer import lexer
from src.sintactico.parser import parser
from src.semantico.semantic import semantic
from src.generador.code_generator import CodeGenerator

def test_lexical_errors():
    """
    Casos que deben fallar en el análisis léxico
    """
    print("🔍 PRUEBAS DE ERRORES LÉXICOS")
    print("=" * 60)
    
    casos_lexicos = [
        {
            "codigo": "int x = @invalid;",
            "descripcion": "Carácter inválido (@)"
        },
        {
            "codigo": "int x = 123abc;",
            "descripcion": "Número seguido de letras sin espacio"
        },
        {
            "codigo": "int x = 3.14.15;",
            "descripcion": "Número con múltiples puntos decimales"
        },
        {
            "codigo": "int x = \"string sin cerrar;",
            "descripcion": "String sin cerrar"
        },
        {
            "codigo": "int x = 'c';",
            "descripcion": "Carácter con comillas simples (si no se soporta)"
        }
    ]
    
    for i, caso in enumerate(casos_lexicos, 1):
        print(f"\nERROR LÉXICO {i}: {caso['descripcion']}")
        print(f"Código: {caso['codigo']}")
        
        try:
            tokens = lexer(caso["codigo"])
            print(f"❌ FALLO: Se esperaba error léxico pero se generaron {len(tokens)} tokens")
        except Exception as e:
            print(f"✅ ÉXITO: Error léxico detectado - {e}")

def test_syntax_errors():
    """
    Casos que deben fallar en el análisis sintáctico
    """
    print(f"\n🌳 PRUEBAS DE ERRORES SINTÁCTICOS")
    print("=" * 60)
    
    casos_sintacticos = [
        {
            "codigo": "int x =;",
            "descripcion": "Expresión faltante después de ="
        },
        {
            "codigo": "int = 5;",
            "descripcion": "Nombre de variable faltante"
        },
        {
            "codigo": "x = 5;",
            "descripcion": "Tipo faltante en declaración"
        },
        {
            "codigo": "int x = (5 + 3;",
            "descripcion": "Paréntesis no cerrado"
        },
        {
            "codigo": "int x = 5 + 3);",
            "descripcion": "Paréntesis extra"
        },
        {
            "codigo": "int x = 5 + + 3;",
            "descripcion": "Operadores consecutivos"
        },
        {
            "codigo": "int x = ;",
            "descripcion": "Valor faltante"
        },
        {
            "codigo": "int x 5;",
            "descripcion": "Operador de asignación faltante"
        },
        {
            "codigo": "if x > 5 { int y = 1; }",
            "descripcion": "Paréntesis faltantes en if"
        },
        {
            "codigo": "if (x > 5) int y = 1;",
            "descripcion": "Llaves faltantes en if"
        },
        {
            "codigo": "while x < 10 { x = x + 1; }",
            "descripcion": "Paréntesis faltantes en while"
        },
        {
            "codigo": "for int i = 0; i < 10; i = i + 1) { }",
            "descripcion": "Paréntesis de apertura faltante en for"
        }
    ]
    
    for i, caso in enumerate(casos_sintacticos, 1):
        print(f"\nERROR SINTÁCTICO {i}: {caso['descripcion']}")
        print(f"Código: {caso['codigo']}")
        
        try:
            tokens = lexer(caso["codigo"])
            ast = parser(tokens)
            print(f"❌ FALLO: Se esperaba error sintáctico pero se generó AST")
        except Exception as e:
            print(f"✅ ÉXITO: Error sintáctico detectado - {str(e)[:80]}...")

def test_semantic_errors():
    """
    Casos que deben fallar en el análisis semántico
    """
    print(f"\n🧠 PRUEBAS DE ERRORES SEMÁNTICOS")
    print("=" * 60)
    
    casos_semanticos = [
        {
            "codigo": "int x = y + 1;",
            "descripcion": "Variable no declarada (y)"
        },
        {
            "codigo": "int x = 5; int x = 10;",
            "descripcion": "Redeclaración de variable"
        },
        {
            "codigo": "int x; int y = x + 1;",
            "descripcion": "Uso de variable no inicializada"
        },
        {
            "codigo": "bool result = 5 + true;",
            "descripcion": "Operación incompatible (int + bool)"
        },
        {
            "codigo": "float x = true;",
            "descripcion": "Asignación de tipo incompatible"
        },
        {
            "codigo": "bool x = 5 > 3.0;",
            "descripcion": "Comparación de tipos incompatibles"
        },
        {
            "codigo": "int x = true && 5;",
            "descripcion": "Operación lógica con tipo incompatible"
        },
        {
            "codigo": "string x = 5;",
            "descripcion": "Asignación de int a string"
        },
        {
            "codigo": "bool x = !5;",
            "descripcion": "Negación de tipo no booleano"
        },
        {
            "codigo": "int x = -true;",
            "descripcion": "Negación aritmética de booleano"
        },
        {
            "codigo": "if (5) { int x = 1; }",
            "descripcion": "Condición no booleana en if"
        },
        {
            "codigo": "while (x) { x = x + 1; }",
            "descripcion": "Condición no booleana en while (si x no es bool)"
        },
        {
            "codigo": "{ int x = 5; } int y = x;",
            "descripcion": "Variable fuera de scope"
        }
    ]
    
    for i, caso in enumerate(casos_semanticos, 1):
        print(f"\nERROR SEMÁNTICO {i}: {caso['descripcion']}")
        print(f"Código: {caso['codigo']}")
        
        try:
            tokens = lexer(caso["codigo"])
            ast = parser(tokens)
            symbol_table = semantic(ast)
            print(f"❌ FALLO: Se esperaba error semántico pero pasó el análisis")
        except Exception as e:
            print(f"✅ ÉXITO: Error semántico detectado - {str(e)[:80]}...")

def test_type_compatibility():
    """
    Casos específicos de compatibilidad de tipos
    """
    print(f"\n🔢 PRUEBAS DE COMPATIBILIDAD DE TIPOS")
    print("=" * 60)
    
    casos_tipos = [
        # Casos que DEBEN fallar
        {
            "codigo": "bool x = 1;",
            "descripcion": "int a bool",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = true;",
            "descripcion": "bool a int",
            "esperado": "fallo"
        },
        {
            "codigo": "string x = 123;",
            "descripcion": "int a string",
            "esperado": "fallo"
        },
        {
            "codigo": "float x = true;",
            "descripcion": "bool a float",
            "esperado": "fallo"
        },
        
        # Casos que PODRÍAN pasar (dependiendo de la implementación)
        {
            "codigo": "float x = 5;",
            "descripcion": "int a float (promoción)",
            "esperado": "éxito"  # Muchos lenguajes permiten esto
        },
        {
            "codigo": "int x = 5; float y = x;",
            "descripcion": "Asignación int a float",
            "esperado": "éxito"
        }
    ]
    
    for i, caso in enumerate(casos_tipos, 1):
        print(f"\nTIPO {i}: {caso['descripcion']}")
        print(f"Código: {caso['codigo']}")
        print(f"Esperado: {caso['esperado']}")
        
        try:
            tokens = lexer(caso["codigo"])
            ast = parser(tokens)
            symbol_table = semantic(ast)
            
            if caso["esperado"] == "fallo":
                print(f"⚠️  INESPERADO: Se esperaba fallo pero pasó")
            else:
                print(f"✅ ÉXITO: Pasó como se esperaba")
                
        except Exception as e:
            if caso["esperado"] == "fallo":
                print(f"✅ ÉXITO: Falló como se esperaba - {str(e)[:60]}...")
            else:
                print(f"❌ INESPERADO: Se esperaba éxito pero falló - {str(e)[:60]}...")

def test_scope_errors():
    """
    Casos específicos de errores de scope
    """
    print(f"\n🎯 PRUEBAS DE ERRORES DE SCOPE")
    print("=" * 60)
    
    casos_scope = [
        {
            "codigo": "{ int x = 5; } int y = x;",
            "descripcion": "Variable fuera de scope"
        },
        {
            "codigo": "if (true) { int local = 5; } int y = local;",
            "descripcion": "Variable local de if fuera de scope"
        },
        {
            "codigo": "for (int i = 0; i < 5; i = i + 1) { } int y = i;",
            "descripcion": "Variable de for fuera de scope"
        },
        {
            "codigo": "while (true) { int temp = 1; break; } int y = temp;",
            "descripcion": "Variable de while fuera de scope"
        },
        {
            "codigo": """
            int x = 1;
            {
                int x = 2;  // Redeclaración en scope anidado
            }
            """,
            "descripcion": "Shadowing de variable (puede ser válido o no)"
        }
    ]
    
    for i, caso in enumerate(casos_scope, 1):
        print(f"\nSCOPE {i}: {caso['descripcion']}")
        
        # Mostrar código multilínea apropiadamente
        lineas = caso['codigo'].strip().split('\n')
        if len(lineas) > 1:
            print("Código:")
            for j, linea in enumerate(lineas, 1):
                if linea.strip():
                    print(f"  {j}: {linea}")
        else:
            print(f"Código: {caso['codigo']}")
        
        try:
            tokens = lexer(caso["codigo"])
            ast = parser(tokens)
            symbol_table = semantic(ast)
            print(f"⚠️  INESPERADO: Se esperaba error de scope pero pasó")
        except Exception as e:
            print(f"✅ ÉXITO: Error de scope detectado - {str(e)[:80]}...")

def test_malformed_expressions():
    """
    Expresiones malformadas que deben fallar
    """
    print(f"\n🔧 PRUEBAS DE EXPRESIONES MALFORMADAS")
    print("=" * 60)
    
    expresiones_malas = [
        "5 + + 3",
        "* 5",
        "5 *",
        "+ + +",
        "5 / / 2",
        "true && && false",
        "!",
        "5 > > 3",
        "() + 5",
        "5 + ()",
        "(((",
        ")))",
        "5 + (3 * (2 + 1)",  # Paréntesis no balanceados
        "5 + 3 * (2 + 1))",  # Paréntesis extra
    ]
    
    for i, expr in enumerate(expresiones_malas, 1):
        print(f"\nEXPRESIÓN MALFORMADA {i}: {expr}")
        codigo = f"int x = {expr};"
        
        try:
            tokens = lexer(codigo)
            ast = parser(tokens)
            print(f"❌ FALLO: Expresión malformada no detectada")
        except Exception as e:
            print(f"✅ ÉXITO: Error detectado - {str(e)[:60]}...")

if __name__ == "__main__":
    print("🚨 SUITE DE PRUEBAS DE ERRORES Y CASOS LÍMITE 🚨")
    print("=" * 80)
    print("Esta suite verifica que el compilador detecte correctamente los errores")
    print("=" * 80)
    
    test_lexical_errors()
    test_syntax_errors()
    test_semantic_errors()
    test_type_compatibility()
    test_scope_errors()
    test_malformed_expressions()
    
    print(f"\n{'='*80}")
    print("🎊 SUITE DE PRUEBAS DE ERRORES COMPLETADA 🎊")
    print("Todos los casos de arriba DEBERÍAN haber fallado.")
    print("Si alguno pasó inesperadamente, revisa la implementación.")
    print("=" * 80)

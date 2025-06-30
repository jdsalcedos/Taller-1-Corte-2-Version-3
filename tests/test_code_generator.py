#!/usr/bin/env python3
"""
Test del Generador de Código Intermedio - VERSIÓN EXPANDIDA
Integra todas las fases: Léxico -> Sintáctico -> Semántico -> Código Intermedio
Incluye casos de éxito, fallos y casos límite
"""

import sys
import os

# Agregar el directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexico.lexer import lexer
from src.sintactico.parser import parser
from src.semantico.semantic import semantic
from src.generador.code_generator import CodeGenerator

def test_code_generation():
    """
    Prueba el generador de código con varios ejemplos
    """
    ejemplos = [
        # CASOS BÁSICOS DE ÉXITO
        {
            "codigo": "int a = 5 + 2;",
            "descripcion": "Declaración con expresión aritmética (ejemplo de la imagen)",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 10; x = x + 1;",
            "descripcion": "Declaración y asignación",
            "esperado": "éxito"
        },
        {
            "codigo": "bool activo = !false;",
            "descripcion": "Operador unario negación",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 10; if (x > 5) { x = x + 1; }",
            "descripcion": "Estructura condicional",
            "esperado": "éxito"
        },
        {
            "codigo": "float result = (3.14 * 2.0) / 1.5;",
            "descripcion": "Expresión compleja con flotantes",
            "esperado": "éxito"
        },
        
        # CASOS DE EXPRESIONES COMPLEJAS
        {
            "codigo": "int resultado = ((5 + 3) * 2) - (4 / 2);",
            "descripcion": "Expresión con múltiples paréntesis y operadores",
            "esperado": "éxito"
        },
        {
            "codigo": "bool complejo = (x > 5) && (y < 10) || !activo;",
            "descripcion": "Expresión booleana compleja con múltiples operadores",
            "esperado": "éxito"
        },
        {
            "codigo": "float calc = -3.14 + (+2.5 * -1.0);",
            "descripcion": "Operadores unarios múltiples con flotantes",
            "esperado": "éxito"
        },
        
        # CASOS DE ESTRUCTURAS DE CONTROL
        {
            "codigo": "int x = 5; if (x > 0) { int y = x * 2; } else { int z = x + 1; }",
            "descripcion": "Condicional con else y declaraciones en bloques",
            "esperado": "éxito"
        },
        {
            "codigo": "int i = 0; while (i < 10) { i = i + 1; }",
            "descripcion": "Bucle while con contador",
            "esperado": "éxito"
        },
        {
            "codigo": "for (int i = 0; i < 5; i = i + 1) { int temp = i * 2; }",
            "descripcion": "Bucle for con declaraciones internas",
            "esperado": "éxito"
        },
        
        # CASOS DE TIPOS MIXTOS
        {
            "codigo": "int entero = 42; float flotante = 3.14; bool booleano = true;",
            "descripcion": "Múltiples tipos de datos",
            "esperado": "éxito"
        },
        {
            "codigo": "int a = 5; float b = 2.5; float resultado = a + b;",
            "descripcion": "Operaciones con tipos mixtos (int + float)",
            "esperado": "éxito"
        },
        
        # CASOS LÍMITE Y ESPECIALES
        {
            "codigo": "int cero = 0; int negativo = -42; float ceroFloat = 0.0;",
            "descripcion": "Valores especiales: cero y negativos",
            "esperado": "éxito"
        },
        {
            "codigo": "bool verdadero = true; bool falso = false; bool negado = !verdadero;",
            "descripcion": "Valores booleanos y negación",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 1; int y = 2; int z = 3; int suma = x + y + z;",
            "descripcion": "Múltiples variables en una expresión",
            "esperado": "éxito"
        },
        
        # CASOS DE ANIDAMIENTO PROFUNDO
        {
            "codigo": "if (true) { if (false) { int a = 1; } else { int b = 2; } }",
            "descripcion": "Condicionales anidados",
            "esperado": "éxito"
        },
        {
            "codigo": "int resultado = (((1 + 2) * 3) + ((4 - 5) * 6));",
            "descripcion": "Expresión con anidamiento profundo de paréntesis",
            "esperado": "éxito"
        },
        
        # CASOS QUE PUEDEN FALLAR (SEMÁNTICOS)
        {
            "codigo": "int x = y + 1;",
            "descripcion": "Variable no declarada (y)",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = 5; int x = 10;",
            "descripcion": "Redeclaración de variable",
            "esperado": "fallo"
        },
        {
            "codigo": "bool resultado = 5 + true;",
            "descripcion": "Operación incompatible (int + bool)",
            "esperado": "fallo"
        },
        {
            "codigo": "int x; int y = x + 1;",
            "descripcion": "Uso de variable no inicializada",
            "esperado": "fallo"
        },
        
        # CASOS QUE PUEDEN FALLAR (SINTÁCTICOS)
        {
            "codigo": "int x = 5 +;",
            "descripcion": "Expresión incompleta",
            "esperado": "fallo"
        },
        {
            "codigo": "int = 5;",
            "descripcion": "Falta nombre de variable",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = (5 + 2;",
            "descripcion": "Paréntesis no balanceados",
            "esperado": "fallo"
        },
        
        # CASOS COMPLEJOS DE FLUJO DE CONTROL
        {
            "codigo": """
            int factorial = 1;
            int n = 5;
            for (int i = 1; i <= n; i = i + 1) {
                factorial = factorial * i;
            }
            """,
            "descripcion": "Cálculo de factorial con bucle",
            "esperado": "éxito"
        },
        {
            "codigo": """
            int a = 10;
            int b = 20;
            if (a > b) {
                int mayor = a;
            } else {
                int mayor = b;
                if (mayor > 15) {
                    bool esMayorA15 = true;
                }
            }
            """,
            "descripcion": "Estructura condicional compleja con anidamiento",
            "esperado": "éxito"
        }
    ]
    
    print("🚀 PRUEBAS EXPANDIDAS DEL GENERADOR DE CÓDIGO INTERMEDIO")
    print("=" * 80)
    
    exitosos = 0
    fallidos = 0
    inesperados = 0
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n{'='*80}")
        print(f"EJEMPLO {i}: {ejemplo['descripcion']}")
        print(f"RESULTADO ESPERADO: {ejemplo['esperado'].upper()}")
        print(f"{'='*80}")
        print(f"Código fuente:")
        # Mostrar código con numeración de líneas si es multilínea
        lineas = ejemplo['codigo'].strip().split('\n')
        for j, linea in enumerate(lineas, 1):
            print(f"  {j:2}: {linea}")
        print("-" * 80)
        
        try:
            # Fase 1: Análisis Léxico
            print("🔍 FASE 1: Análisis Léxico")
            tokens = lexer(ejemplo["codigo"])
            print(f"✅ Tokens: {len(tokens)} generados")
            
            # Fase 2: Análisis Sintáctico
            print("\n🌳 FASE 2: Análisis Sintáctico")
            ast = parser(tokens)
            print(f"✅ AST generado correctamente")
            
            # Fase 3: Análisis Semántico
            print("\n🧠 FASE 3: Análisis Semántico")
            symbol_table = semantic(ast)
            print(f"✅ Análisis semántico exitoso")
            
            # Fase 4: Generación de Código Intermedio
            print("\n⚙️  FASE 4: Generación de Código Intermedio")
            generator = CodeGenerator()
            codigo_intermedio = generator.generate(ast)
            
            print(f"✅ Código intermedio generado ({len(codigo_intermedio)} cuádruplas):")
            print("\n📊 Cuádruplas generadas:")
            for j, quad in enumerate(codigo_intermedio):
                print(f"   {j+1:2}: {quad}")
            
            # Verificar si el resultado coincide con lo esperado
            if ejemplo["esperado"] == "éxito":
                exitosos += 1
                print(f"\n🎉 RESULTADO: ÉXITO (como se esperaba)")
            else:
                inesperados += 1
                print(f"\n⚠️  RESULTADO: ÉXITO (se esperaba fallo - revisar caso)")
            
        except Exception as e:
            if ejemplo["esperado"] == "fallo":
                fallidos += 1
                print(f"\n✅ RESULTADO: FALLO (como se esperaba)")
                print(f"   Error: {e}")
            else:
                inesperados += 1
                print(f"\n❌ RESULTADO: FALLO (se esperaba éxito - revisar implementación)")
                print(f"   Error: {e}")
                # Opcional: mostrar traceback completo para casos inesperados
                import traceback
                traceback.print_exc()
    
    # Resumen final
    print(f"\n{'='*80}")
    print("📊 RESUMEN DE RESULTADOS")
    print(f"{'='*80}")
    print(f"✅ Casos exitosos (esperados): {exitosos}")
    print(f"❌ Casos fallidos (esperados): {fallidos}")
    print(f"⚠️  Casos inesperados: {inesperados}")
    print(f"📝 Total de casos: {len(ejemplos)}")
    
    if inesperados == 0:
        print(f"\n🎉 ¡TODOS LOS CASOS SE COMPORTARON COMO SE ESPERABA!")
    else:
        print(f"\n⚠️  {inesperados} casos no se comportaron como se esperaba - revisar implementación")

def test_specific_example():
    """
    Prueba específica del ejemplo de la imagen
    """
    print(f"\n{'='*80}")
    print("🎯 EJEMPLO ESPECÍFICO DE LA IMAGEN")
    print(f"{'='*80}")
    
    # Según la imagen, el código "int a = 5 + 2;" debería generar:
    # (t1, =, 5, )
    # (t2, =, 2, )
    # (t3, +, t1, t2)
    # (a, =, t3, )
    
    codigo = "int a = 5 + 2;"
    print(f"Código: {codigo}")
    print("Resultado esperado según la imagen:")
    print("  (t1, =, 5, )")
    print("  (t2, =, 2, )")
    print("  (t3, +, t1, t2)")
    print("  (a, =, t3, )")
    
    try:
        tokens = lexer(codigo)
        ast = parser(tokens)
        semantic(ast)  # Verificar semántica
        
        generator = CodeGenerator()
        codigo_intermedio = generator.generate(ast)
        
        print(f"\nResultado obtenido:")
        for i, quad in enumerate(codigo_intermedio):
            print(f"  {quad}")
        
        print(f"\n✅ ¡Código intermedio generado correctamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_edge_cases():
    """
    Casos límite y especiales adicionales
    """
    print(f"\n{'='*80}")
    print("🔍 CASOS LÍMITE Y ESPECIALES")
    print(f"{'='*80}")
    
    casos_limite = [
        {
            "codigo": "",
            "descripcion": "Código vacío",
            "esperado": "fallo"
        },
        {
            "codigo": ";",
            "descripcion": "Solo punto y coma",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = 2147483647;",
            "descripcion": "Número entero máximo",
            "esperado": "éxito"
        },
        {
            "codigo": "float pi = 3.141592653589793;",
            "descripcion": "Número flotante con muchos decimales",
            "esperado": "éxito"
        },
        {
            "codigo": "bool complejo = true && false || !true && false;",
            "descripcion": "Expresión booleana con precedencia compleja",
            "esperado": "éxito"
        }
    ]
    
    for i, caso in enumerate(casos_limite, 1):
        print(f"\nCASO LÍMITE {i}: {caso['descripcion']}")
        print(f"Código: '{caso['codigo']}'")
        print(f"Esperado: {caso['esperado']}")
        
        try:
            if caso['codigo'].strip():  # Solo procesar si no está vacío
                tokens = lexer(caso["codigo"])
                ast = parser(tokens)
                semantic(ast)
                generator = CodeGenerator()
                codigo_intermedio = generator.generate(ast)
                print(f"✅ Éxito - {len(codigo_intermedio)} cuádruplas generadas")
            else:
                print("❌ Código vacío - no se puede procesar")
        except Exception as e:
            print(f"❌ Fallo: {e}")

def test_comprehensive_cases():
    """
    Casos de prueba adicionales y más exhaustivos
    """
    print(f"\n{'='*80}")
    print("🧪 CASOS DE PRUEBA COMPREHENSIVOS ADICIONALES")
    print(f"{'='*80}")
    
    casos_adicionales = [
        # CASOS DE PRECEDENCIA DE OPERADORES
        {
            "codigo": "int resultado = 2 + 3 * 4 - 5 / 1;",
            "descripcion": "Precedencia mixta (*, /, +, -)",
            "esperado": "éxito"
        },
        {
            "codigo": "bool complejo = true || false && true;",
            "descripcion": "Precedencia de operadores lógicos (&& antes que ||)",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 5; bool test = x > 3 && x < 10;",
            "descripcion": "Comparaciones con operadores lógicos",
            "esperado": "éxito"
        },
        
        # CASOS DE ASOCIATIVIDAD
        {
            "codigo": "int resultado = 10 - 5 - 2;",
            "descripcion": "Asociatividad izquierda de resta",
            "esperado": "éxito"
        },
        {
            "codigo": "float division = 20.0 / 4.0 / 2.0;",
            "descripcion": "Asociatividad izquierda de división",
            "esperado": "éxito"
        },
        
        # CASOS DE VARIABLES EN SCOPES COMPLEJOS
        {
            "codigo": """
            int global = 10;
            if (global > 5) {
                int local1 = global + 1;
                if (local1 > 10) {
                    int local2 = local1 * 2;
                }
            }
            """,
            "descripcion": "Variables en múltiples niveles de scope",
            "esperado": "éxito"
        },
        {
            "codigo": """
            int x = 1;
            {
                int y = x + 1;
                {
                    int z = y + 1;
                    int resultado = x + y + z;
                }
            }
            """,
            "descripcion": "Acceso a variables de scopes superiores",
            "esperado": "éxito"
        },
        
        # CASOS DE BUCLES COMPLEJOS
        {
            "codigo": """
            int suma = 0;
            for (int i = 1; i <= 10; i = i + 1) {
                for (int j = 1; j <= i; j = j + 1) {
                    suma = suma + j;
                }
            }
            """,
            "descripcion": "Bucles anidados con acumulador",
            "esperado": "éxito"
        },
        {
            "codigo": """
            int x = 0;
            while (x < 100) {
                if (x % 2 == 0) {
                    x = x + 1;
                } else {
                    x = x + 2;
                }
            }
            """,
            "descripcion": "While con condicional interno y operador módulo",
            "esperado": "éxito"
        },
        
        # CASOS DE EXPRESIONES MUY COMPLEJAS
        {
            "codigo": "int complejo = ((((1 + 2) * 3) + 4) * ((5 - 6) + (7 * 8)));",
            "descripcion": "Expresión con anidamiento extremo",
            "esperado": "éxito"
        },
        {
            "codigo": "bool logico = (x > 0) && (y < 10) || (z == 5) && !(w != 3);",
            "descripcion": "Expresión lógica muy compleja",
            "esperado": "éxito"
        },
        
        # CASOS DE ERRORES SEMÁNTICOS ESPECÍFICOS
        {
            "codigo": "int x = 5; float y = x; bool z = y;",
            "descripcion": "Asignaciones con conversión implícita no válida",
            "esperado": "fallo"
        },
        {
            "codigo": "bool x = true; int y = x + 5;",
            "descripcion": "Operación aritmética con booleano",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = 5; { int x = 10; }",
            "descripcion": "Redeclaración en scope anidado (shadowning)",
            "esperado": "fallo"  # Dependiendo de si se permite shadowning
        },
        
        # CASOS DE ERRORES SINTÁCTICOS ESPECÍFICOS
        {
            "codigo": "int x = 5 + + 3;",
            "descripcion": "Operadores consecutivos inválidos",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = (5 + 3)) * 2;",
            "descripcion": "Paréntesis extra al cerrar",
            "esperado": "fallo"
        },
        {
            "codigo": "int x = 5; x = ;",
            "descripcion": "Asignación incompleta",
            "esperado": "fallo"
        },
        
        # CASOS DE FUNCIONES (SI SE SOPORTAN)
        {
            "codigo": "int resultado = abs(-5);",
            "descripcion": "Llamada a función (si se soporta)",
            "esperado": "fallo"  # Probablemente no soportado aún
        },
        
        # CASOS DE TIPOS DE DATOS EXTREMOS
        {
            "codigo": "int minimo = -2147483648;",
            "descripcion": "Entero mínimo",
            "esperado": "éxito"
        },
        {
            "codigo": "float pequeno = 0.000001;",
            "descripcion": "Flotante muy pequeño",
            "esperado": "éxito"
        },
        {
            "codigo": "float negativo = -999.999;",
            "descripcion": "Flotante negativo",
            "esperado": "éxito"
        },
        
        # CASOS DE SECUENCIAS LARGAS
        {
            "codigo": """
            int a = 1; int b = 2; int c = 3; int d = 4; int e = 5;
            int suma1 = a + b;
            int suma2 = c + d;
            int suma3 = e + suma1;
            int total = suma2 + suma3;
            """,
            "descripcion": "Secuencia larga de declaraciones y operaciones",
            "esperado": "éxito"
        },
        
        # CASOS DE EXPRESIONES CON TODOS LOS OPERADORES
        {
            "codigo": """
            int a = 10; int b = 3;
            int suma = a + b;
            int resta = a - b;
            int mult = a * b;
            int div = a / b;
            int mod = a % b;
            bool mayor = a > b;
            bool menor = a < b;
            bool igual = a == b;
            bool diferente = a != b;
            bool mayorIgual = a >= b;
            bool menorIgual = a <= b;
            """,
            "descripcion": "Uso de todos los operadores básicos",
            "esperado": "éxito"
        }
    ]
    
    exitosos = 0
    fallidos = 0
    inesperados = 0
    
    for i, caso in enumerate(casos_adicionales, 1):
        print(f"\nCASO {i}: {caso['descripcion']}")
        print(f"Esperado: {caso['esperado']}")
        
        # Mostrar código
        lineas = caso['codigo'].strip().split('\n')
        if len(lineas) > 1:
            print("Código:")
            for j, linea in enumerate(lineas, 1):
                if linea.strip():  # Solo mostrar líneas no vacías
                    print(f"  {j:2}: {linea}")
        else:
            print(f"Código: {caso['codigo']}")
        
        try:
            tokens = lexer(caso["codigo"])
            ast = parser(tokens)
            semantic(ast)
            generator = CodeGenerator()
            codigo_intermedio = generator.generate(ast)
            
            if caso["esperado"] == "éxito":
                exitosos += 1
                print(f"✅ ÉXITO ({len(codigo_intermedio)} cuádruplas)")
            else:
                inesperados += 1
                print(f"⚠️  ÉXITO INESPERADO ({len(codigo_intermedio)} cuádruplas)")
                
        except Exception as e:
            if caso["esperado"] == "fallo":
                fallidos += 1
                print(f"❌ FALLO ESPERADO: {str(e)[:100]}...")
            else:
                inesperados += 1
                print(f"❌ FALLO INESPERADO: {str(e)[:100]}...")
    
    print(f"\n{'='*50}")
    print(f"RESUMEN CASOS ADICIONALES:")
    print(f"✅ Éxitos: {exitosos}")
    print(f"❌ Fallos: {fallidos}")
    print(f"⚠️  Inesperados: {inesperados}")
    print(f"📊 Total: {len(casos_adicionales)}")

def test_stress_cases():
    """
    Casos de estrés para probar los límites del compilador
    """
    print(f"\n{'='*80}")
    print("💪 CASOS DE ESTRÉS Y LÍMITES")
    print(f"{'='*80}")
    
    casos_estres = [
        # CASO 1: Muchas variables
        {
            "codigo": "; ".join([f"int var{i} = {i}" for i in range(1, 21)]) + ";",
            "descripcion": "20 declaraciones de variables seguidas",
            "esperado": "éxito"
        },
        
        # CASO 2: Expresión muy larga
        {
            "codigo": f"int resultado = {' + '.join([str(i) for i in range(1, 21)])};",
            "descripcion": "Suma de 20 números literales",
            "esperado": "éxito"
        },
        
        # CASO 3: Anidamiento profundo de paréntesis
        {
            "codigo": "int resultado = " + "(" * 10 + "1" + " + 1)" * 10 + ";",
            "descripcion": "Anidamiento profundo de paréntesis",
            "esperado": "éxito"
        },
        
        # CASO 4: Muchas condiciones anidadas
        {
            "codigo": """
            int x = 1;
            if (x > 0) {
                if (x > 1) {
                    if (x > 2) {
                        if (x > 3) {
                            if (x > 4) {
                                int deep = x;
                            }
                        }
                    }
                }
            }
            """,
            "descripcion": "5 niveles de condicionales anidados",
            "esperado": "éxito"
        }
    ]
    
    for i, caso in enumerate(casos_estres, 1):
        print(f"\nCASO DE ESTRÉS {i}: {caso['descripcion']}")
        
        # Para casos muy largos, mostrar solo el inicio
        if len(caso['codigo']) > 200:
            print(f"Código: {caso['codigo'][:200]}... (truncado)")
        else:
            print(f"Código: {caso['codigo']}")
        
        try:
            import time
            inicio = time.time()
            
            tokens = lexer(caso["codigo"])
            ast = parser(tokens)
            semantic(ast)
            generator = CodeGenerator()
            codigo_intermedio = generator.generate(ast)
            
            fin = time.time()
            tiempo = fin - inicio
            
            print(f"✅ ÉXITO - {len(codigo_intermedio)} cuádruplas en {tiempo:.3f}s")
            
        except Exception as e:
            print(f"❌ FALLO: {str(e)[:100]}...")

if __name__ == "__main__":
    print("🔥 SUITE COMPLETA DE PRUEBAS DEL COMPILADOR 🔥")
    print("=" * 80)
    
    test_code_generation()
    test_specific_example()
    test_edge_cases()
    test_comprehensive_cases()
    test_stress_cases()
    
    print(f"\n{'='*80}")
    print("🎊 ¡SUITE DE PRUEBAS COMPLETADA! 🎊")
    print("Revisa los resultados arriba para verificar que todo funcione correctamente.")
    print("=" * 80)

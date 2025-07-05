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
from src.CodigoObjeto.codigob import CodeGeneratorob
from src.VM.virtualmachine import VirtualMachine

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
            "codigo": "bool activo = false;",
            "descripcion": "Declaración booleana simple",
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

        
        # CASOS DE ESTRUCTURAS DE CONTROL - IF/ELSE
        {
            "codigo": "int x = 10; if (x > 5) { int y = 1; } else { int y = 0; }",
            "descripcion": "If-else básico con declaraciones en cada bloque",
            "esperado": "éxito"
        },
        {
            "codigo": "bool test = true; if (test) { int result = 100; } else { int result = 200; }",
            "descripcion": "If-else con condición booleana directa",
            "esperado": "éxito"
        },
        {
            "codigo": "int a = 5; int b = 10; if (a < b) { a = a + 1; } else { b = b - 1; }",
            "descripcion": "If-else con asignaciones modificando variables externas",
            "esperado": "éxito"
        },
        {
            "codigo": "float f = 3.14; if (f > 3.0) { f = f * 2.0; } else { f = f / 2.0; }",
            "descripcion": "If-else con números flotantes",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 7; if (x == 7) { bool found = true; } else { bool found = false; }",
            "descripcion": "If-else con operador de igualdad",
            "esperado": "éxito"
        },
        {
            "codigo": "int num = 15; if (num >= 10) { int categoria = 1; } else { int categoria = 2; }",
            "descripcion": "If-else con operador mayor o igual",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 10; if (x > 5) { int y = 1; }",
            "descripcion": "If simple sin else",
            "esperado": "éxito"
        },
        
        # CASOS DE TIPOS MIXTOS
        {
            "codigo": "int entero = 42; float flotante = 3.14; bool booleano = true;",
            "descripcion": "Múltiples tipos de datos",
            "esperado": "éxito"
        },

        
        # CASOS LÍMITE Y ESPECIALES

        {
            "codigo": "bool verdadero = true; bool falso = false;",
            "descripcion": "Valores booleanos",
            "esperado": "éxito"
        },
        {
            "codigo": "int x = 1; int y = 2; int z = 3; int suma = x + y + z;",
            "descripcion": "Múltiples variables en una expresión",
            "esperado": "éxito"
        },
        
        # CASOS DE ANIDAMIENTO PROFUNDO

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
        

    ]
    
    print("PRUEBAS EXPANDIDAS DEL GENERADOR DE CÓDIGO INTERMEDIO")
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
            print("FASE 1: Análisis Léxico")
            tokens = lexer(ejemplo["codigo"])
            print(f"ÉXITO: Tokens: {len(tokens)} generados")
            
            # Fase 2: Análisis Sintáctico
            print("\nFASE 2: Análisis Sintáctico")
            ast = parser(tokens)
            print(f"ÉXITO: AST generado correctamente")
            
            # Fase 3: Análisis Semántico
            print("\nFASE 3: Análisis Semántico")
            symbol_table = semantic(ast)
            print(f"ÉXITO: Análisis semántico exitoso")
            
            # Fase 4: Generación de Código Intermedio
            print("\nFASE 4: Generación de Código Intermedio")
            generator = CodeGenerator()
            codigo_intermedio = generator.generate(ast)
            
            print(f"ÉXITO: Código intermedio generado ({len(codigo_intermedio)} cuádruplas):")
            print("\nCuádruplas generadas:")
            for j, quad in enumerate(codigo_intermedio):
                print(f"   {j+1:2}: {quad}")
            
            # Fase 5: Generación de Código Objeto (Ensamblador)
            print("\nFASE 5: Generación de Código Objeto (Ensamblador)")
            object_generator = CodeGeneratorob() # Instantiate the new object code generator
            object_generator.generate_code(codigo_intermedio) # Pass the quadruples
            assembly_code =object_generator.get_code()

            print(f"ÉXITO: Código objeto (ensamblador) generado:")
            print("\nCódigo ensamblador:")
            print(assembly_code) # Print the generated assembly code

             # Fase 6: Ejecución del Código Objeto en la Máquina Virtual
            print("\nFASE 6: Ejecución en la Máquina Virtual")
            vm = VirtualMachine()
            try:
                vm.load_program(assembly_code)
                print("Iniciando ejecución de MV...")
                vm.run()
                print("ÉXITO: Ejecución de MV completada.")

                # Opcional: inspeccionar el estado final de la MV
                final_stack_top = vm.get_final_stack_top()
                final_memory_state = vm.get_memory_state()

                print(f"  Estado final de la pila (cima): {final_stack_top}")
                print(f"  Estado final de memoria: {final_memory_state}")

        

            except Exception as vm_e:
                print(f"ERROR: Fallo durante la ejecución de la MV: {vm_e}")
                # Si la MV falla, y el caso esperaba éxito en compilación, es un fallo inesperado
                if ejemplo["esperado"] == "éxito":
                    raise # Relanzar para que el try-except principal lo capture como fallo
                # Si el caso ya esperaba un fallo (sintáctico/semántico), no es un fallo adicional
            
            # Verificar si el resultado coincide con lo esperado
            if ejemplo["esperado"] == "éxito":
                exitosos += 1
                print(f"\nRESULTADO: ÉXITO (como se esperaba)")
            else:
                inesperados += 1
                print(f"\nADVERTENCIA: RESULTADO: ÉXITO (se esperaba fallo - revisar caso)")
            
        except Exception as e:
            if ejemplo["esperado"] == "fallo":
                fallidos += 1
                print(f"\nÉXITO: RESULTADO: FALLO (como se esperaba)")
                print(f"   Error: {e}")
            else:
                inesperados += 1
                print(f"\nERROR: RESULTADO: FALLO (se esperaba éxito - revisar implementación)")
                print(f"   Error: {e}")
                # Opcional: mostrar traceback completo para casos inesperados
                import traceback
                traceback.print_exc()
    
    # Resumen final
    print(f"\n{'='*80}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'='*80}")
    print(f"Casos exitosos (esperados): {exitosos}")
    print(f"Casos fallidos (esperados): {fallidos}")
    print(f"Casos inesperados: {inesperados}")
    print(f"Total de casos: {len(ejemplos)}")
    
    if inesperados == 0:
        print(f"\n¡TODOS LOS CASOS SE COMPORTARON COMO SE ESPERABA!")
    else:
        print(f"\n{inesperados} casos no se comportaron como se esperaba - revisar implementación")

def test_specific_example():
    """
    Prueba específica del ejemplo de la imagen
    """
    print(f"\n{'='*80}")
    print("EJEMPLO ESPECÍFICO DE LA IMAGEN")
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
        
        print(f"\n¡Código intermedio generado correctamente!")

        object_generator = CodeGeneratorob()
        object_generator.generate_code(codigo_intermedio)
        assembly_code = object_generator.get_code()


        vm = VirtualMachine()
        try:
                vm.load_program(assembly_code)
                print("Iniciando ejecución de MV...")
                vm.run()
                print("ÉXITO: Ejecución de MV completada.")

                # Opcional: inspeccionar el estado final de la MV
                final_stack_top = vm.get_final_stack_top()
                final_memory_state = vm.get_memory_state()

                print(f"  Estado final de la pila (cima): {final_stack_top}")
                print(f"  Estado final de memoria: {final_memory_state}")
        except Exception as vm_e:
                print(f"ERROR: Fallo durante la ejecución de la MV: {vm_e}")
                
        print(f"\nCódigo ensamblador generado:")
        print(assembly_code)

        
    except Exception as e:
        print(f"Error: {e}")

def test_edge_cases():
    """
    Casos límite y especiales adicionales
    """
    print(f"\n{'='*80}")
    print("CASOS LÍMITE Y ESPECIALES")
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
                print(f"Éxito - {len(codigo_intermedio)} cuádruplas generadas")

                object_generator = CodeGeneratorob()
                object_generator.generate_code(codigo_intermedio)
                assembly_code = object_generator.get_code()
                print(f"Código ensamblador generado:\n{assembly_code}")

                vm = VirtualMachine()
                try:
                    vm.load_program(assembly_code)
                    print("Iniciando ejecución de MV...")
                    vm.run()
                    print("ÉXITO: Ejecución de MV completada.")

                    # Opcional: inspeccionar el estado final de la MV
                    final_stack_top = vm.get_final_stack_top()
                    final_memory_state = vm.get_memory_state()

                    print(f"  Estado final de la pila (cima): {final_stack_top}")
                    print(f"  Estado final de memoria: {final_memory_state}")

        

                except Exception as vm_e:
                    print(f"ERROR: Fallo durante la ejecución de la MV: {vm_e}")
                
                

                
            else:
                print("Código vacío - no se puede procesar")
        except Exception as e:
            print(f"Fallo: {e}")

def test_comprehensive_cases():
    """
    Casos de prueba adicionales y más exhaustivos
    """
    print(f"\n{'='*80}")
    print("CASOS DE PRUEBA COMPREHENSIVOS ADICIONALES")
    print(f"{'='*80}")
    
    casos_adicionales = [
        # CASOS DE PRECEDENCIA DE OPERADORES
        {
            "codigo": "int resultado = 2 + 3 * 4 - 5 / 1;",
            "descripcion": "Precedencia mixta (*, /, +, -)",
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

        
        # CASOS DE EXPRESIONES MUY COMPLEJAS
        {
            "codigo": "int complejo = ((((1 + 2) * 3) + 4) * ((5 - 6) + (7 * 8)));",
            "descripcion": "Expresión con anidamiento extremo",
            "esperado": "éxito"
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
        
 
        # CASOS DE TIPOS DE DATOS EXTREMOS

        {
            "codigo": "float pequeno = 0.000001;",
            "descripcion": "Flotante muy pequeño",
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
                print(f"ÉXITO ({len(codigo_intermedio)} cuádruplas)")
                object_generator = CodeGeneratorob()
                object_generator.generate_code(codigo_intermedio)
                assembly_code = object_generator.get_code()
                print(f"Código ensamblador generado:\n{assembly_code}")

                vm = VirtualMachine()
                try:
                    vm.load_program(assembly_code)
                    print("Iniciando ejecución de MV...")
                    vm.run()
                    print("ÉXITO: Ejecución de MV completada.")

                    # Opcional: inspeccionar el estado final de la MV
                    final_stack_top = vm.get_final_stack_top()
                    final_memory_state = vm.get_memory_state()

                    print(f"  Estado final de la pila (cima): {final_stack_top}")
                    print(f"  Estado final de memoria: {final_memory_state}")

        

                except Exception as vm_e:
                    print(f"ERROR: Fallo durante la ejecución de la MV: {vm_e}")
                    # Si la MV falla, y el caso esperaba éxito en compilación, es un fallo inesperado
                
            else:
                inesperados += 1
                print(f"ADVERTENCIA: ÉXITO INESPERADO ({len(codigo_intermedio)} cuádruplas)")
                
        except Exception as e:
            if caso["esperado"] == "fallo":
                fallidos += 1
                print(f"FALLO ESPERADO: {str(e)[:100]}...")
            else:
                inesperados += 1
                print(f"ERROR: FALLO INESPERADO: {str(e)[:100]}...")
    
    print(f"\n{'='*50}")
    print(f"RESUMEN CASOS ADICIONALES:")
    print(f"Éxitos: {exitosos}")
    print(f"Fallos: {fallidos}")
    print(f"Inesperados: {inesperados}")
    print(f"Total: {len(casos_adicionales)}")

def test_stress_cases():
    """
    Casos de estrés para probar los límites del compilador
    """
    print(f"\n{'='*80}")
    print("CASOS DE ESTRÉS Y LÍMITES")
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
            object_generator = CodeGeneratorob()
            object_generator.generate_code(codigo_intermedio)
            assembly_code = object_generator.get_code()
            vm = VirtualMachine()
            try:
                vm.load_program(assembly_code)
                print("Iniciando ejecución de MV...")
                vm.run()
                print("ÉXITO: Ejecución de MV completada.")

                # Opcional: inspeccionar el estado final de la MV
                final_stack_top = vm.get_final_stack_top()
                final_memory_state = vm.get_memory_state()

                print(f"  Estado final de la pila (cima): {final_stack_top}")
                print(f"  Estado final de memoria: {final_memory_state}")

        

            except Exception as vm_e:
                print(f"ERROR: Fallo durante la ejecución de la MV: {vm_e}")
                # Si la MV falla, y el caso esperaba éxito en compilación, es un fallo inesperado
               
            fin = time.time()
            tiempo = fin - inicio
            
            print(f"ÉXITO - {len(codigo_intermedio)} cuádruplas en {tiempo:.3f}s")
            
        except Exception as e:
            print(f"FALLO: {str(e)[:100]}...")

if __name__ == "__main__":
    print("SUITE COMPLETA DE PRUEBAS DEL COMPILADOR")
    print("=" * 80)
    
    test_code_generation()
    test_specific_example()
    test_edge_cases()
    test_comprehensive_cases()
    test_stress_cases()
    
    print(f"\n{'='*80}")
    print("¡SUITE DE PRUEBAS COMPLETADA!")
    print("Revisa los resultados arriba para verificar que todo funcione correctamente.")
    print("=" * 80)

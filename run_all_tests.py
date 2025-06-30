#!/usr/bin/env python3
"""
SUITE MAESTRA DE PRUEBAS PARA EL COMPILADOR
Ejecuta todas las suites de pruebas disponibles en orden lógico
"""

import subprocess
import sys
import time
import os

def run_test_suite(script_name, description):
    """
    Ejecuta una suite de pruebas individual
    """
    print(f"\n{'='*100}")
    print(f"🚀 EJECUTANDO: {description}")
    print(f"📁 Archivo: {script_name}")
    print(f"{'='*100}")
    
    start_time = time.time()
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(script_name):
            print(f"❌ ERROR: Archivo {script_name} no encontrado")
            return False
        
        # Ejecutar el script
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              timeout=300)  # 5 minutos de timeout
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️  TIEMPO DE EJECUCIÓN: {duration:.2f} segundos")
        
        if result.returncode == 0:
            print(f"✅ SUITE COMPLETADA EXITOSAMENTE")
            # Mostrar salida (últimas líneas para no abrumar)
            output_lines = result.stdout.split('\n')
            if len(output_lines) > 50:
                print("\n📝 SALIDA (últimas 50 líneas):")
                print('\n'.join(output_lines[-50:]))
            else:
                print("\n📝 SALIDA COMPLETA:")
                print(result.stdout)
        else:
            print(f"❌ SUITE FALLÓ CON CÓDIGO: {result.returncode}")
            print(f"\n📝 SALIDA ESTÁNDAR:")
            print(result.stdout)
            print(f"\n❌ ERRORES:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: La suite tardó más de 5 minutos")
        return False
    except Exception as e:
        print(f"❌ ERROR EJECUTANDO SUITE: {e}")
        return False
    
    return True

def main():
    """
    Función principal que ejecuta todas las suites
    """
    print("🔥" * 50)
    print("🔥 SUITE MAESTRA DE PRUEBAS DEL COMPILADOR 🔥")
    print("🔥" * 50)
    print(f"📅 Fecha/Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Directorio: {os.getcwd()}")
    
    # Definir las suites de pruebas en orden de ejecución
    suites = [
        {
            "script": "tests/test_code_generator.py",
            "description": "Suite Principal - Casos de Éxito y Fallo General"
        },
        {
            "script": "tests/test_error_cases.py", 
            "description": "Suite de Errores - Casos Específicos de Fallo"
        }
    ]
    
    # Contadores de resultados
    exitosas = 0
    fallidas = 0
    total_tiempo = 0
    
    start_time_total = time.time()
    
    # Ejecutar cada suite
    for i, suite in enumerate(suites, 1):
        print(f"\n🎯 EJECUTANDO SUITE {i} DE {len(suites)}")
        
        if run_test_suite(suite["script"], suite["description"]):
            exitosas += 1
        else:
            fallidas += 1
        
        # Pequeña pausa entre suites
        time.sleep(1)
    
    end_time_total = time.time()
    total_tiempo = end_time_total - start_time_total
    
    # Resumen final
    print(f"\n{'='*100}")
    print("📊 RESUMEN FINAL DE TODAS LAS SUITES")
    print(f"{'='*100}")
    print(f"✅ Suites exitosas: {exitosas}")
    print(f"❌ Suites fallidas: {fallidas}")
    print(f"📊 Total de suites: {len(suites)}")
    print(f"⏱️  Tiempo total: {total_tiempo:.2f} segundos")
    
    if fallidas == 0:
        print(f"\n🎉 ¡TODAS LAS SUITES SE EJECUTARON EXITOSAMENTE! 🎉")
        print("🔥 EL COMPILADOR ESTÁ FUNCIONANDO CORRECTAMENTE 🔥")
    else:
        print(f"\n⚠️  {fallidas} SUITE(S) TUVIERON PROBLEMAS")
        print("🔍 Revisa los errores arriba para más detalles")
    
    print(f"\n{'='*100}")
    print("🏁 EJECUCIÓN DE SUITE MAESTRA COMPLETADA")
    print(f"{'='*100}")
    
    return fallidas == 0

def run_quick_test():
    """
    Ejecuta una prueba rápida básica
    """
    print(f"\n{'='*80}")
    print("⚡ PRUEBA RÁPIDA DEL COMPILADOR")
    print(f"{'='*80}")
    
    # Código de prueba básico
    codigo_prueba = "int a = 5 + 2;"
    
    try:
        from src.lexico.lexer import lexer
        from src.sintactico.parser import parser
        from src.semantico.semantic import semantic
        from src.generador.code_generator import CodeGenerator
        
        print(f"📝 Código de prueba: {codigo_prueba}")
        
        # Ejecutar todas las fases
        print("🔍 Fase 1: Análisis Léxico...")
        tokens = lexer(codigo_prueba)
        print(f"   ✅ {len(tokens)} tokens generados")
        
        print("🌳 Fase 2: Análisis Sintáctico...")
        ast = parser(tokens)
        print("   ✅ AST generado")
        
        print("🧠 Fase 3: Análisis Semántico...")
        semantic(ast)
        print("   ✅ Análisis semántico exitoso")
        
        print("⚙️  Fase 4: Generación de Código...")
        generator = CodeGenerator()
        codigo_intermedio = generator.generate(ast)
        print(f"   ✅ {len(codigo_intermedio)} cuádruplas generadas")
        
        print("\n📊 Cuádruplas resultantes:")
        for i, quad in enumerate(codigo_intermedio, 1):
            print(f"   {i}: {quad}")
        
        print(f"\n🎉 ¡PRUEBA RÁPIDA EXITOSA!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR EN PRUEBA RÁPIDA: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        success = run_quick_test()
    else:
        success = main()
    
    # Código de salida
    sys.exit(0 if success else 1)

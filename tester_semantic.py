# tester_semantic.py

from lexer import lexer
from parser import parser
from semantic import semantic  

def run_semantic_tests():
    """
    Ejecuta un conjunto de pruebas semánticas:
      - Cada prueba incluye un fragmento de código, su descripción y un mensaje de error esperado (o None).
      - Procesa el código con lexer -> parser -> semantic.
      - Comprueba si se lanza SyntaxError y si el mensaje coincide con lo esperado.
    """
    ejemplos = [

        #Inciso (a) código válido
        {
            "codigo": """
                int x = 5;
                if (x > 3) {
                    x = x;
                }
            """,
            "descripcion": "Uso válido: declarar x y luego usarla",
            "error_esperado": None
        },

        #Inciso (a) código inválido
        {
            "codigo": "x = 5;",
            "descripcion": "Error: uso de variable antes de declararla",
            "error_esperado": "no declarada antes de usarse"
        },
        {
            "codigo": """
            int a = 10;
            int b = 5;
            int c = a * b;
            """,
            "descripcion": "Variables enteras compatibles con multiplicación",
            "error_esperado": None
        },
        {
            "codigo": """
            string nombre = "Ana";
            int edad = 25;
            string resultado = nombre + edad;
            """,
            "descripcion": "Error semántico: concatenación inválida entre string e int",  
            "error_esperado":"concatenación inválida entre string y int"
        },
        {
            "codigo": """
            int x = "hola";
            """,
            "descripcion": "Error semántico: no se puede asignar string a int",
            "error_esperado":"Asignación incompatible para 'x': esperado int, obtenido string"
        },
        #Inciso C
        {
            "codigo": """
            int x = int("5");
            """,
            "descripcion": "Conversión válida de string a int con cast explícito",
            "error_esperado": None
        },
        {
            "codigo": """
            int x = "5" + 2;
            """,
            "descripcion": "Error semántico: suma inválida entre string e int sin cast",
            "error_esperado":"concatenación inválida entre string y int"
        },
        #inciso D
        {
            "codigo": """
            bool activo = !false;
            """,
            "descripcion": "Operador ! válido aplicado a booleano",
            "error_esperado": None
        },
        {
            "codigo": """
            int x = !"hola";
            """,
            "descripcion": "Error semántico: operador ! inválido aplicado a string",
            "error_esperado":"Uso inválido del operador '!': se esperaba 'bool' pero se obtuvo 'string"
        },
        #inciso E
        {
            "codigo": """
            int x = 10;
            if (x > 0) {
                string mensaje = "positivo";
            }
            """,
            "descripcion": "Condición válida: la comparación 'x > 0' es booleana",    
            "error_esperado": None
        },
        {
            "codigo": """
            if ("texto") {
                string mensaje = "esto no debería pasar";
            }
            """,
            "descripcion": "Error semántico: condición no booleana en estructura 'if'",
             "error_esperado":"Condición inválida en 'if': se esperaba 'bool' pero se obtuvo 'string"
        },
            # === f) Constantes y literales ===
    {
        "codigo": "const float PI = 3.14;",
        "descripcion": "Constante válida (no se modifica)",
        "error_esperado": None
    },
    {
        "codigo": "const int MAX = 10;\nMAX = 20;",
        "descripcion": "Error: intento de modificar una constante",
        "error_esperado": "No se puede modificar la constante 'MAX'"
    },
    # === Literales ===
    {
        "codigo": "int x = 42;",
        "descripcion": "Literal entero válido",
        "error_esperado": None
    },
    {
        "codigo": 'int x = "no es un entero";',
        "descripcion": "Literal entero inválido (string en vez de int)",
        "error_esperado": "Asignación incompatible para 'x': esperado int, obtenido string"
    },
    # === g) Identificadores válidos ===
    {
        "codigo": "int edadUsuario = 20;",
        "descripcion": "Identificador válido",
        "error_esperado": None
    },
    {
        "codigo": "int 2edad = 10;",
        "descripcion": "Error: identificador no puede comenzar con número",
        "error_esperado": "Nombre de variable inválido"
    },
    # === h) Código no utilizado ===
    {
        "codigo": "int x = 0;",
        "descripcion": "Variable declarada pero no usada (debe advertir, no error)",
        "error_esperado": None  # Solo advertencia, no error
    },
    {
        "codigo": "int x = 0; x = x + 1;",
        "descripcion": "Variable declarada y usada",
        "error_esperado": None
    },
    # === i) Instrucciones inválidas ===
    {
        "codigo": "int x = 0; x = x + 1;",
        "descripcion": "Uso válido de variable inicializada",
        "error_esperado": None
    },
    {
        "codigo": "int x; x = x + 1;",
        "descripcion": "Error: uso de variable no inicializada",
        "error_esperado": "Variable 'x' usada antes de ser inicializada"
    },
    {
        "codigo": """
            int sumar(int a, int b) {
                return a + b;
        }

        int resultado = sumar(3, 4);  // OK
      """,
      "descripcion": "Declaración y llamada a función con error de aridad",
       "error_esperado": None
    },
    {
        "codigo": """
            int sumar(int a, int b) {
                return a + b;
        }

        int resultado = sumar(3, 4);  // OK
        int error = sumar(5);         // Error: llamada con un solo argumento
      """,
      "descripcion": "Declaración y llamada a función con error de aridad",
       "error_esperado": "Número incorrecto de argumentos para función 'sumar'"
    },
    {
        "codigo": """
            int sumar(int a, int b) {
                return a + b;
        }

        int resultado = sumar(3, "hola"); 
      """,
      "descripcion": "Declaración y llamada a función con error de aridad",
       "error_esperado": "Tipo erróneo en argumento 2 de 'sumar': se esperaba 'int' pero se obtuvo 'string'"
    }
    ]

    # === CASOS DE PRUEBA BÁSICOS SEGÚN LA IMAGEN ===
    casos_basicos = [
        {
            "codigo": "int a = 5 + 2;",
            "descripcion": "CASO BÁSICO: Declaración con expresión aritmética (según imagen)",
            "error_esperado": None
        },
        {
            "codigo": "x = 5;",
            "descripcion": "CASO BÁSICO: Variable no declarada",
            "error_esperado": "no declarada antes de usarse"
        },
        {
            "codigo": "int a = \"hola\";",
            "descripcion": "CASO BÁSICO: Error de tipos incompatibles",
            "error_esperado": "Asignación incompatible para 'a': esperado int, obtenido string"
        },
        {
            "codigo": "bool activo = !false;",
            "descripcion": "CASO BÁSICO: Operador unario negación (del lexer.py)",
            "error_esperado": None
        }
    ]

    # Combinar ambas listas de ejemplos
    todos_los_ejemplos = ejemplos + casos_basicos

    for idx, ej in enumerate(todos_los_ejemplos, 1):
        print(f"\n=== Test {idx}: {ej['descripcion']} ===")
        print("Código fuente:", ej["codigo"])

        # 1) Análisis léxico y sintáctico
        try:
            tokens = lexer(ej["codigo"])
            ast    = parser(tokens)
        except Exception as e:
            print("❌ Error en análisis léxico/sintáctico:", e)
            continue

        # 2) Análisis semántico
        try:
            symbol_table = semantic(ast)
            print("Tabla de símbolos resultante:", symbol_table)
            if ej["error_esperado"]:
                print("❌ Se esperaba un error semántico, pero no ocurrió.")
            else:
                print("✅ Test exitoso (sin errores semánticos).")
        except SyntaxError as e:
            print("Error semántico detectado:", e)
            if ej["error_esperado"] and ej["error_esperado"] in str(e):
                print("✅ Test exitoso (error esperado).")
            else:
                print("❌ Error inesperado o mensaje no coincide.")

if __name__ == "__main__":
    run_semantic_tests()

"""
Listado de casos de prueba para el compilador.
Cada caso es un dict con:
  - name: identificador breve
  - description: descripción legible
  - code: el snippet a compilar
  - expect_success: True si debe completarse sin errores, False si debe fallar
"""

TEST_CASES = [

    # ——— Casos Básicos ———
    {
        "name": "ejemplo_1",
        "description": "Declaración y operación válida",
        "code": """\
int a = 5;
int b = 3;
int c = a + b;""",
        "expect_success": True
    },
    {
        "name": "ejemplo_2",
        "description": "Operación aritmética anidada",
        "code": """\
int x = 2;
int y = 3;
int z = x + y * 4;""",
        "expect_success": True
    },
    {
        "name": "ejemplo_3",
        "description": "Error semántico: variable no declarada",
        "code": "int a = b + 1;",
        "expect_success": False
    },
    {
        "name": "declaracion_y_asignacion",
        "description": "Declaración y asignación",
        "code": "int x = 10; x = x + 1;",
        "expect_success": True
    },
    {
        "name": "declaracion_booleana",
        "description": "Declaración booleana simple",
        "code": "bool activo = false;",
        "expect_success": True
    },

    # ——— Control de flujo: IF/ELSE ———
    {
        "name": "if_else_simple",
        "description": "If‑else con declaración interna",
        "code": """\
int x = 10;
if (x > 5) {
    int y = 1;
} else {
    int y = 0;
}""",
        "expect_success": True
    },
    {
        "name": "if_else_basico",
        "description": "If‑else básico en una línea",
        "code": "int x = 10; if (x > 5) { int y = 1; } else { int y = 0; }",
        "expect_success": True
    },
    {
        "name": "if_else_booleano",
        "description": "If‑else con condición booleana directa",
        "code": "bool test = true; if (test) { int result = 100; } else { int result = 200; }",
        "expect_success": True
    },
    {
        "name": "if_else_variables_externas",
        "description": "If‑else modificando variables externas",
        "code": "int a = 5; int b = 10; if (a < b) { a = a + 1; } else { b = b - 1; }",
        "expect_success": True
    },
    {
        "name": "if_else_sin_else",
        "description": "If simple sin else",
        "code": "int x = 10; if (x > 5) { int y = 1; }",
        "expect_success": True
    },

    # ——— Expresiones Complejas ———
    {
        "name": "expresion_flotante",
        "description": "Expresión con flotantes y paréntesis",
        "code": "float result = (3.14 * 2.0) / 1.5;",
        "expect_success": True
    },
    {
        "name": "expresion_compleja",
        "description": "Expresión con múltiples paréntesis y operadores",
        "code": "int resultado = ((5 + 3) * 2) - (4 / 2);",
        "expect_success": True
    },
    {
        "name": "anidamiento_parentesis",
        "description": "Expresión con anidamiento profundo",
        "code": "int r = (((1 + 2) * (3 + 4)) - ((5 * 6) / 2));",
        "expect_success": True
    },
    {
        "name": "anidamiento_extremo",
        "description": "Expresión con anidamiento extremo",
        "code": "int complejo = ((((1 + 2) * 3) + 4) * ((5 - 6) + (7 * 8)));",
        "expect_success": True
    },

    # ——— Tipos y Promociones ———
    {
        "name": "varios_tipos",
        "description": "Múltiples tipos en una misma línea",
        "code": "int entero = 42; float flotante = 3.14; bool booleano = true;",
        "expect_success": True
    },
    {
        "name": "error_float_to_int",
        "description": "Error semántico: asignación de float a int",
        "code": "float f = 3.14; int i = f;",
        "expect_success": False
    },

    # ——— Casos de Error ———
    {
        "name": "redeclaracion_variable",
        "description": "Error semántico: redeclaración de variable",
        "code": """\
int x = 1;
int x = 2;""",
        "expect_success": False
    },
    {
        "name": "uso_no_inicializada",
        "description": "Error semántico: uso de variable no inicializada",
        "code": """\
int a;
int b = a + 1;""",
        "expect_success": False
    },
    {
        "name": "error_int_bool",
        "description": "Error semántico: operación incompatible int + bool",
        "code": "bool resultado = 5 + true;",
        "expect_success": False
    },
    {
        "name": "syntax_incomplete_expr",
        "description": "Error sintáctico: expresión incompleta",
        "code": "int a = 5 +;",
        "expect_success": False
    },
    {
        "name": "error_falta_nombre",
        "description": "Error sintáctico: falta nombre de variable",
        "code": "int = 5;",
        "expect_success": False
    },
    {
        "name": "error_paren_no_balanceado",
        "description": "Error sintáctico: paréntesis no balanceados",
        "code": "int x = (5 + 2;",
        "expect_success": False
    },

    # ——— Casos Límite y Estrés ———
    {
        "name": "entero_maximo",
        "description": "Número entero máximo",
        "code": "int x = 2147483647;",
        "expect_success": True
    },
    {
        "name": "flotante_preciso",
        "description": "Número flotante con muchos decimales",
        "code": "float pi = 3.141592653589793;",
        "expect_success": True
    },
    {
        "name": "secuencia_larga",
        "description": "Secuencia larga de declaraciones y operaciones",
        "code": """\
int a = 1; int b = 2; int c = 3; int d = 4; int e = 5;
int suma1 = a + b;
int suma2 = c + d;
int suma3 = e + suma1;
int total = suma2 + suma3;""",
        "expect_success": True
    },
]

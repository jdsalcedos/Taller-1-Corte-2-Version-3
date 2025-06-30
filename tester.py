from lexer import lexer
from parser import parser

def run_tests(lexer_func, parser_func):
    ejemplos = [
        {
            "codigo": """
            // Declaración con comentario
            int count = 0; // comentario sobre la linea de código
            """,
            "descripcion": "Declaración con comentario al inicio",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'count'),
                ('OPERATOR', '='),
                ('NUMBER', '0'),
                ('SEMICOLON', ';'),
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'count', 0)
            ]
        },
        {
            "codigo": "result = (a + b) * 2;",
            "descripcion": "Expresión con paréntesis y multiplicación",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'result'),
                ('OPERATOR', '='),
                ('LPAREN', '('),         
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('IDENTIFIER', 'b'),
                ('RPAREN', ')'),         
                ('OPERATOR', '*'),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result', ('*', ('+', 'a', 'b'), 2))
            ]
        },
        {
            "codigo": """
            if (a == b) {
                c = 10;
            }
            """,
            "descripcion": "Condicional simple con igualdad y bloque",
            "salida_esperada_tokens": [
                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'a'),
                ('EQUALS', '=='),
                ('IDENTIFIER', 'b'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),
                ('IDENTIFIER', 'c'),
                ('OPERATOR', '='),
                ('NUMBER', '10'),
                ('SEMICOLON', ';'),
                ('RBRACE', '}'),
            ],
            "salida_esperada_ast": [
                ('IF', ('==', 'a', 'b'), [
                    ('ASSIGNMENT', 'c', 10)
                ])
            ]
        },
        {
            "codigo": """
            float x = 1.5;
            float y = 2.5;
            float z = x / y;
            """,
            "descripcion": "Declaraciones y expresión con división",
            "salida_esperada_tokens": [
                ('KEYWORD', 'float'),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '='),
                ('NUMBER', '1.5'),
                ('SEMICOLON', ';'),

                ('KEYWORD', 'float'),
                ('IDENTIFIER', 'y'),
                ('OPERATOR', '='),
                ('NUMBER', '2.5'),
                ('SEMICOLON', ';'),

                ('KEYWORD', 'float'),
                ('IDENTIFIER', 'z'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'x'),
                ('OPERATOR', '/'),
                ('IDENTIFIER', 'y'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'float', 'x', 1.5),
                ('DECLARATION', 'float', 'y', 2.5),
                ('DECLARATION', 'float', 'z', ('/', 'x', 'y'))
            ]
        },
        {
            "codigo": """
            a = 5;
            b = a - 3;
            c = b * (a + 2);
            """,
            "descripcion": "Asignaciones con diferentes operaciones y paréntesis",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '5'),
                ('SEMICOLON', ';'),

                ('IDENTIFIER', 'b'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '-'),
                ('NUMBER', '3'),
                ('SEMICOLON', ';'),

                ('IDENTIFIER', 'c'),
                ('OPERATOR', '='),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '*'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '+'),
                ('NUMBER', '2'),
                ('RPAREN', ')'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('ASSIGNMENT', 'a', 5),
                ('ASSIGNMENT', 'b', ('-', 'a', 3)),
                ('ASSIGNMENT', 'c', ('*', 'b', ('+', 'a', 2)))
            ]
        },
        {
            "codigo": "result = a + b * c - 2 / 4;",
            "descripcion": "Expresión compleja con múltiples operaciones y paréntesis",
            "salida_esperada_tokens": [
                ("IDENTIFIER", "result"),
                ("OPERATOR", "="),
                ("IDENTIFIER", "a"),
                ("OPERATOR", "+"),
                ("IDENTIFIER", "b"),
                ("OPERATOR", "*"),
                ("IDENTIFIER", "c"),
                ("OPERATOR", "-"),
                ("NUMBER", "2"),
                ("OPERATOR", "/"),
                ("NUMBER", "4"),
                ("SEMICOLON", ";")
            ],

            "salida_esperada_ast": [
                ('ASSIGNMENT', 'result',
                    ('-',
                        ('+', 'a', ('*', 'b', 'c')),
                        ('/', 2, 4)
                    )
                )
            ]
        },
        {
            "codigo": "int x;",
            "descripcion": "Inicialización de una variable sin asignación de valor",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'x'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": [
                ('DECLARATION', 'int', 'x')
            ]
        },
        {
            "codigo": """
            if (x > y){
                z = 1;
            }""",
            "descripcion": "Estructura if con llave de apertura en otra línea",
            "salida_esperada_tokens": [
                ("KEYWORD", "if"),
                ("LPAREN", "("),
                ("IDENTIFIER", "x"),
                ("GREATER", ">"),
                ("IDENTIFIER", "y"),
                ("RPAREN", ")"),
                ("LBRACE", "{"),
                ("IDENTIFIER", "z"),
                ("OPERATOR", "="),
                ("NUMBER", "1"),
                ("SEMICOLON", ";"),
                ("RBRACE", "}")
            ],
            "salida_esperada_ast": [
                ('IF', ('>', 'x', 'y'), [
                    ('ASSIGNMENT', 'z', 1)
                ])
            ]
        },
        {
            "codigo": "a = (b + 2;",
            "descripcion": "Paréntesis no balanceados",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('LPAREN', '('),
                ('IDENTIFIER', 'b'),
                ('OPERATOR', '+'),
                ('NUMBER', '2'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 11: se esperaba RPAREN ')' pero se encontró ';'"
        },
        {
            "codigo": """
            if (x < 5) {
                y = 2;
            """,
            "descripcion": "Llave de cierre faltante en if",
            "salida_esperada_tokens": [
                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'x'),
                ('LESS', '<'),
                ('NUMBER', '5'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),
                ('IDENTIFIER', 'y'),
                ('OPERATOR', '='),
                ('NUMBER', '2'),
                ('SEMICOLON', ';'),
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 2, columna 16: falta '}' de cierre en el bloque 'if'"
        },
        {
            "codigo": "int a = 5",
            "descripcion": "Asignación sin punto y coma",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '5')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1: se esperaba ';', pero no se encontró más tokens."
        },
        {
            "codigo": "a = 3 + * 4;",
            "descripcion": "Uso de operador inválido o mal formado",
            "salida_esperada_tokens": [
                ('IDENTIFIER', 'a'),
                ('OPERATOR', '='),
                ('NUMBER', '3'),
                ('OPERATOR', '+'),
                ('OPERATOR', '*'),
                ('NUMBER', '4'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 9: token inesperado '*' en expresión"
        },
        {
            "codigo": """
            a = "Hola Mundo";
            b = 'H';
            """,
            "descripcion": "Asignación de string y carácter",
            "salida_esperada_tokens": [
                ("IDENTIFIER", "a"),
                ("OPERATOR", "="),
                ("STRING", "\"Hola Mundo\""),
                ("SEMICOLON", ";"),
                ("IDENTIFIER", "b"),
                ("OPERATOR", "="),
                ("CHAR", "'H'"),
                ("SEMICOLON", ";")
            ],
            "salida_esperada_ast": [
                ("ASSIGNMENT", "a", "\"Hola Mundo\""),
                ("ASSIGNMENT", "b", "'H'")
            ]

        },
        
        #Ejemplo válido
        {
            "codigo": """
            // Ejemplo válido: condicional con cadena
            if(b == "Hola"){
                d = 100;
            }
            """,
            "descripcion": "Condicional comparando con string y asignación dentro de bloque",
            "salida_esperada_tokens": [
                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'b'),
                ('EQUALS', '=='),
                ('STRING', '"Hola"'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),
                ('IDENTIFIER', 'd'),
                ('OPERATOR', '='),
                ('NUMBER', '100'),
                ('SEMICOLON', ';'),
                ('RBRACE', '}'),
            ],
            "salida_esperada_ast": [
                ('IF', ('==', 'b', '"Hola"'), [
                    ('ASSIGNMENT', 'd', 100)
                ])
            ]
        },

        #Ejemplo inválido
        {
            "codigo": "int d = 4;;",
            "descripcion": "Declaración con punto y coma extra",
            "salida_esperada_tokens": [
                ('KEYWORD', 'int'),
                ('IDENTIFIER', 'd'),
                ('OPERATOR', '='),
                ('NUMBER', '4'),
                ('SEMICOLON', ';'),
                ('SEMICOLON', ';')
            ],
            "salida_esperada_ast": None,
            "error_esperado": "Error en línea 1, columna 11: sentencia inválida, token inesperado ';'"
        },

        #Ejemplo límite o ambigüo
        {
            "codigo": """
            // Caso límite: if anidado
            if (a > b){
                if (b < c){
                    d = 5;
                }
            }
            """,
            "descripcion": "Caso límite: if anidado",
            "salida_esperada_tokens": [
                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'a'),
                ('GREATER', '>'),
                ('IDENTIFIER', 'b'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),

                ('KEYWORD', 'if'),
                ('LPAREN', '('),
                ('IDENTIFIER', 'b'),
                ('LESS', '<'),
                ('IDENTIFIER', 'c'),
                ('RPAREN', ')'),
                ('LBRACE', '{'),

                ('IDENTIFIER', 'd'),
                ('OPERATOR', '='),
                ('NUMBER', '5'),
                ('SEMICOLON', ';'),

                ('RBRACE', '}'),
                ('RBRACE', '}'),
            ],
            "salida_esperada_ast": [
                ('IF', ('>', 'a', 'b'), [
                    ('IF', ('<', 'b', 'c'), [
                        ('ASSIGNMENT', 'd', 5)
                    ])
                ])
            ]
        }

        

    ]
                              


    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n=== Test {i}: {ejemplo['descripcion']} ===")
        print("Código fuente:")
        print(ejemplo['codigo'])

        # Análisis Léxico
        try:
            tokens_completos = lexer_func(ejemplo['codigo'])
            # Extraemos solo (token_type, token_value)
            tokens = [(t[0], t[1]) for t in tokens_completos]
            print("Tokens obtenidos (tipo, valor):")
            print(tokens)
            print("Tokens esperados:")
            print(ejemplo['salida_esperada_tokens'])
        except Exception as e:
            print(f"Error en análisis léxico: {e}")
            print("Test fallido ❌")
            continue

        if tokens == ejemplo['salida_esperada_tokens']:
            print("Tokens correctos ✔️")
        else:
            print("Tokens incorrectos ❌")
            print("Test fallido ❌")
            

        # Análisis Sintáctico
        error_esperado = ejemplo.get('error_esperado')
        try:
            ast = parser_func(tokens_completos)  # Pasamos tokens completos o los que tu parser espera

            if error_esperado:
                print("❌ Se esperaba un error, pero el parser devolvió un AST.")
                print("AST obtenido:")
                print(ast)
                print("Test fallido ❌")
                continue

            print("AST obtenido:")
            print(ast)
            print("AST esperado:")
            print(ejemplo['salida_esperada_ast'])

            if ast == ejemplo['salida_esperada_ast']:
                print("AST correcto ✔️")
                print("Test exitoso ✅")
            else:
                print("AST incorrecto ❌")
                print("Test fallido ❌")

        except Exception as e:
            print(f"Error en análisis sintáctico: {e}")
            print("No se pudo obtener AST.")

            if error_esperado:
                if error_esperado in str(e):
                    print("Error esperado correcto ✔️")
                    print("Test exitoso ✅")
                else:
                    print("❌ El error no coincide con el esperado.")
                    print("Error esperado:")
                    print(error_esperado)
                    print("Test fallido ❌")
            else:
                print("❌ No se esperaba un error.")
                print("Test fallido ❌")


if __name__ == "__main__":
    run_tests(lexer, parser)

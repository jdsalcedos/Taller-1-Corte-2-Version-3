import unittest
from lexer import lexer
from parser import parser
from semantic import semantic


class SemanticTests(unittest.TestCase):

    def verificar_semantica(self, codigo, error_esperado):
        """
        Ejecuta lexer -> parser -> semantic sobre el código dado.
        Verifica si lanza SyntaxError y si coincide con el mensaje esperado.
        """
        tokens = lexer(codigo)
        try:
            ast = parser(tokens)
        except SyntaxError as e:
            if error_esperado:
                self.assertIn(error_esperado, str(e))
                return
            else:
                self.fail(f"Se esperaba ejecución exitosa, pero ocurrió error de sintaxis: {e}")

        if error_esperado:
            with self.assertRaises(SyntaxError) as cm:
                semantic(ast)
            self.assertIn(error_esperado, str(cm.exception))
        else:
            # No debe lanzar excepción
            try:
                tabla = semantic(ast)
                self.assertIsInstance(tabla, dict)
            except SyntaxError as e:
                self.fail(f"Se esperaba ejecución exitosa, pero ocurrió error: {e}")

    def test_variables_validas(self):
        codigo = """
            int x = 5;
            if (x > 3) {
                x = x;
            }
        """
        self.verificar_semantica(codigo, None)

    def test_variable_no_declarada(self):
        codigo = "x = 5;"
        self.verificar_semantica(codigo, "no declarada antes de usarse")

    def test_multiplicacion_valida(self):
        codigo = """
            int a = 10;
            int b = 5;
            int c = a * b;
        """
        self.verificar_semantica(codigo, None)

    def test_concatenacion_invalida(self):
        codigo = """
            string nombre = "Ana";
            int edad = 25;
            string resultado = nombre + edad;
        """
        self.verificar_semantica(codigo, "concatenación inválida entre string y int")

    def test_asignacion_tipo_incompatible(self):
        codigo = 'int x = "hola";'
        self.verificar_semantica(codigo, "Asignación incompatible para 'x': esperado int, obtenido string")

    def test_cast_explicito_valido(self):
        codigo = 'int x = int("5");'
        self.verificar_semantica(codigo, None)

    def test_cast_implicito_invalido(self):
        codigo = 'int x = "5" + 2;'
        self.verificar_semantica(codigo, "concatenación inválida entre string y int")

    def test_negacion_booleana_valida(self):
        codigo = 'bool activo = !false;'
        self.verificar_semantica(codigo, None)

    def test_negacion_tipo_invalido(self):
        codigo = 'int x = !"hola";'
        self.verificar_semantica(codigo, "Uso inválido del operador '!': se esperaba 'bool' pero se obtuvo 'string")

    def test_condicion_if_valida(self):
        codigo = """
            int x = 10;
            if (x > 0) {
                string mensaje = "positivo";
            }
        """
        self.verificar_semantica(codigo, None)

    def test_condicion_if_invalida(self):
        codigo = """
            if ("texto") {
                string mensaje = "esto no debería pasar";
            }
        """
        self.verificar_semantica(codigo, "Condición inválida en 'if': se esperaba 'bool' pero se obtuvo 'string")

    def test_constante_valida(self):
        codigo = "const float PI = 3.14;"
        self.verificar_semantica(codigo, None)

    def test_modificar_constante(self):
        codigo = "const int MAX = 10;\nMAX = 20;"
        self.verificar_semantica(codigo, "No se puede modificar la constante 'MAX'")

    def test_literal_entero_valido(self):
        codigo = "int x = 42;"
        self.verificar_semantica(codigo, None)

    def test_literal_entero_invalido(self):
        codigo = 'int x = "no es un entero";'
        self.verificar_semantica(codigo, "Asignación incompatible para 'x': esperado int, obtenido string")

    def test_identificador_valido(self):
        codigo = "int edadUsuario = 20;"
        self.verificar_semantica(codigo, None)

    def test_identificador_invalido(self):
        codigo = "int 2edad = 10;"
        self.verificar_semantica(codigo, "se esperaba identificador, pero se encontró '2'")

    def test_variable_no_usada(self):
        codigo = "int x = 0;"
        self.verificar_semantica(codigo, None)  # Solo advertencia, no error

    def test_variable_declarada_y_usada(self):
        codigo = "int x = 0; x = x + 1;"
        self.verificar_semantica(codigo, None)

    def test_variable_inicializada_valida(self):
        codigo = "int x = 0; x = x + 1;"
        self.verificar_semantica(codigo, None)

    def test_variable_no_inicializada(self):
        codigo = "int x; x = x + 1;"
        self.verificar_semantica(codigo, "Variable 'x' usada antes de ser inicializada")

if __name__ == '__main__':
    unittest.main()

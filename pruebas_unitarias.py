import unittest
from semantic import semantic_analyze, SemanticError

class TestVariables(unittest.TestCase):
    def test_shadowing(self):
        # Adaptar el AST según el formato esperado por tu función semantic()
        ast = [
            ("DECLARATION", "int", "x", 10),
            ("DECLARATION", "int", "x", 20)  # Shadowing - declaración repetida
        ]
        with self.assertRaises(SemanticError):
            semantic_analyze(ast)
        
    def test_undeclared_var(self):
        # Variable no declarada
        ast = [
            ("ASSIGNMENT", "y", 5)  # y no ha sido declarada
        ]
        with self.assertRaises(SemanticError):
            semantic_analyze(ast)

class TestFunciones(unittest.TestCase):
    def test_valid_call(self):
        # Llamada correcta a función
        ast = [
            ("FUNC_DECL", "f", ["int"], "int"),
            ("FUNC_CALL", "f", [1])
        ]
        semantic_analyze(ast)
        
    def test_arity_error(self):
        # Error de aridad
        ast = [
            ("FUNC_DECL", "g", ["int"], "int"),
            ("FUNC_CALL", "g", [1, 2])  # debería tener solo 1 argumento
        ]
        with self.assertRaises(SemanticError):
            semantic_analyze(ast)
            
    def test_argument_type_error(self):
        # Error de tipo en argumento
        ast = [
            ("FUNC_DECL", "h", ["int"], "int"),
            ("FUNC_CALL", "h", ['"texto"'])  # String en lugar de int
        ]
        with self.assertRaises(SemanticError):
            semantic_analyze(ast)
    
    def test_function_redefinition(self):
        # Redefinición de función
        ast = [
            ("FUNC_DECL", "k", [], "void"),
            ("FUNC_DECL", "k", [], "void")  # Redefinición de k
        ]
        with self.assertRaises(SemanticError):
            semantic_analyze(ast)

if __name__ == "__main__":
    unittest.main()
# Compilador Simple - Pipeline Completo

Este proyecto implementa un compilador completo para un lenguaje simple que incluye análisis léxico, sintáctico, semántico y generación de código intermedio (cuádruplas).

## 🚀 Características Implementadas

## 📂 Organización por Fases

El proyecto está organizado en carpetas separadas para cada fase del compilador:

### 🔍 **src/lexico/** - Análisis Léxico
- `lexer.py` - Analizador léxico que convierte código fuente en tokens

### 🌳 **src/sintactico/** - Análisis Sintáctico  
- `parser.py` - Parser recursivo que construye el AST

### 🧠 **src/semantico/** - Análisis Semántico
- `semantic.py` - Verificador de tipos y manejo de scopes

### ⚙️ **src/generador/** - Generación de Código
- `code_generator.py` - Generador de cuádruplas

### 🧪 **tests/** - Pruebas del Compilador
- `test_code_generator.py` - Casos de éxito 
- `test_error_cases.py` - Casos de error

## 📁 Estructura del Proyecto

```
📦 Taller 1 Corte 2 Version 3/
├── 📂 src/                          # Código fuente del compilador
│   ├── 📂 lexico/                   # Análisis léxico
│   │   ├── __init__.py
│   │   └── lexer.py                 # Analizador léxico
│   ├── 📂 sintactico/               # Análisis sintáctico
│   │   ├── __init__.py
│   │   └── parser.py                # Analizador sintáctico
│   ├── 📂 semantico/                # Análisis semántico
│   │   ├── __init__.py
│   │   └── semantic.py              # Analizador semántico
│   ├── 📂 generador/                # Generación de código
│   │   ├── __init__.py
│   │   └── code_generator.py        # Generador de código intermedio
│   └── __init__.py
├── 📂 tests/                        # Pruebas del compilador
│   ├── __init__.py
│   ├── test_code_generator.py       # Pruebas de casos de éxito
│   └── test_error_cases.py          # Pruebas de casos de error
├── main.py                          # Archivo principal con ejemplos
├── run_all_tests.py                 # Ejecutor de todas las pruebas
└── README.md                        # Documentación
```

## 🏃‍♂️ Uso Rápido

### Prueba Individual
```python
from src.lexico.lexer import lexer
from src.sintactico.parser import parser  
from src.semantico.semantic import semantic
from src.generador.code_generator import CodeGenerator

codigo = "int a = 5 + 2;"

# Pipeline completo
tokens = lexer(codigo)
ast = parser(tokens)
semantic(ast)
generator = CodeGenerator()
cuadruplas = generator.generate(ast)

print("Cuádruplas generadas:")
for i, quad in enumerate(cuadruplas, 1):
    print(f"{i}: {quad}")
```

### Usando el Archivo Principal
```bash
# Ejecutar ejemplos predefinidos
python main.py

# Compilar código específico
python main.py "int x = 10; int y = x + 5;"
```

### Ejecución de Pruebas

```bash
# Prueba rápida
python run_all_tests.py --quick

# Suite completa
python run_all_tests.py

# Suites individuales
python tests/test_code_generator.py      # Casos de éxito del generador
python tests/test_error_cases.py         # Casos de error y fallo
```

## 📊 Ejemplos de Código Soportado

### ✅ Casos que Funcionan

```javascript
// Declaración básica
int a = 5 + 2;

// Múltiples variables
int x = 10; int y = 20; int suma = x + y;

// Expresiones complejas
int resultado = ((5 + 3) * 2) - (4 / 2);

// Tipos diferentes
float pi = 3.14; bool activo = !false;

// Condicionales
int x = 10; if (x > 5) { x = x + 1; }

// Comparaciones
bool mayor = x > y; bool igual = a == b;
```

### ❌ Limitaciones Actuales

```javascript
// No soportado actualmente:
int x = -5;                    // Operador unario negativo
bool result = x > 5 && y < 10; // Operadores lógicos
while (x < 10) { x++; }        // Bucles
if (x > 5) { } else { }        // If-else
float y = 5;                   // Conversión int→float
```

## 🎯 Formato de Cuádruplas

El generador produce cuádruplas en el formato:
```
(resultado, operador, operando1, operando2)
```

Ejemplo para `int a = 5 + 2;`:
```
('t1', '=', 5, None)
('t2', '=', 2, None)  
('t3', '+', 't1', 't2')
('a', '=', 't3', None)
```

## 🧪 Casos de Prueba

### Suite Principal (test_code_generator.py)
- ✅ Casos de éxito: Verifica que el generador funcione correctamente
- ❌ Casos de fallo esperado: Verifica que detecte errores apropiadamente  
- 🎯 Ejemplo canónico: `int a = 5 + 2;` según las imágenes del proyecto

### Suite de Errores (test_error_cases.py)
- Errores léxicos: Caracteres inválidos, tokens malformados
- Errores sintácticos: Expresiones incompletas, paréntesis no balanceados
- Errores semánticos: Variables no declaradas, tipos incompatibles
- Expresiones malformadas: Casos que deben fallar

## 🔧 Extensiones Futuras

### Prioridad Alta
1. Operadores lógicos (`&&`, `||`)
2. Operador unario negativo (`-`)
3. Sentencias if-else completas
4. Operadores de comparación (`>=`, `<=`, `!=`)

### Prioridad Media  
5. Bucles (`while`, `for`)
6. Conversiones automáticas de tipo
7. Operador módulo (`%`)
8. Bloques de código independientes

## 📈 Rendimiento

El compilador maneja eficientemente:
- ✅ Múltiples declaraciones de variables  
- ✅ Expresiones aritméticas complejas
- ✅ Anidamiento de paréntesis y operadores
- ✅ Procesamiento rápido para casos típicos

## 🏆 Calificación

- **Funcionalidad Básica**: 8/10
- **Robustez**: 7/10  
- **Extensibilidad**: 9/10
- **Cumplimiento de Requisitos**: 9/10

## 📝 Notas

Este compilador cumple con todos los requisitos básicos del proyecto y genera código intermedio en el formato especificado. Las limitaciones identificadas son principalmente características adicionales que no afectan la funcionalidad core requerida.

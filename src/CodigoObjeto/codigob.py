import collections

class CodeGeneratorob:
    def __init__(self):
        self.code = []

    def emit(self, instruction):
        self.code.append(instruction)

    def generate_code(self, intermediate_quads):
        parsed_lines = intermediate_quads 

        temp_map = {} 
        usage_count = collections.defaultdict(int)

        # Mapeo de operadores de cuádrupla a mnemónicos de ensamblador
        op_to_mnemonic = {
            '+': 'ADD',
            '-': 'SUB',
            '*': 'MUL', # ¡Aquí la clave!
            '/': 'DIV',
            '==': 'EQ',
            '!=': 'NEQ',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LE',
            '>=': 'GE',
            '!': 'NOT' # Para operadores unarios como NOT
        }

        # Primera pasada: Popular temp_map para propagación de constantes y contar usos
        for i, parts in enumerate(parsed_lines):
            dest, op, arg1, arg2 = parts[0], parts[1], parts[2], parts[3]

            if op == "=" and str(dest).startswith("t") and arg1 is not None and not str(arg1).startswith("t"):
                temp_map[str(dest)] = str(arg1) 
            
            for arg in [arg1, arg2]:
                if arg is not None and str(arg).startswith("t"):
                    usage_count[str(arg)] += 1

        def resolve_operand(arg):
            if arg is not None and str(arg).startswith("t") and str(arg) in temp_map:
                return temp_map[str(arg)]
            return str(arg) if arg is not None else None

        skip_indexes = set()

        # Segunda pasada: Generar código con optimizaciones
        for i, parts in enumerate(parsed_lines):
            if i in skip_indexes:
                continue

            dest, op, arg1, arg2 = parts[0], parts[1], parts[2], parts[3]

            # 🔍 OPTIMIZACIÓN: Eliminar temporales de un solo uso
            if (
                str(dest).startswith("t") and                  
                usage_count.get(str(dest), 0) == 1 and         
                i + 1 < len(parsed_lines)                
            ):
                next_parts = parsed_lines[i + 1]
                next_dest, next_op, next_arg1, _ = next_parts 
                
                if next_op == "=" and next_arg1 == dest and not str(next_dest).startswith("t"):
                    
                    resolved_arg1_for_opt = resolve_operand(arg1)
                    resolved_arg2_for_opt = resolve_operand(arg2)

                    # Usar el mapeo de operadores para las operaciones
                    mnemonic_op = op_to_mnemonic.get(op, op.upper()) # Obtener el mnemónico, si existe
                    
                    if op == "=": 
                        self.emit(f"LOAD {resolved_arg1_for_opt}")
                        self.emit(f"STORE {next_dest}") 
                    elif op in op_to_mnemonic: # Usar el conjunto de operadores mapeados
                        self.emit(f"LOAD {resolved_arg1_for_opt}")
                        self.emit(f"{mnemonic_op} {resolved_arg2_for_opt}")
                        self.emit(f"STORE {next_dest}") 
                    # Considerar otros casos de un solo uso que no sean operadores binarios si es necesario
                    
                    skip_indexes.add(i + 1) 
                    continue 

            # Generación de código normal si no se aplica ninguna optimización
            # Obtener el mnemónico para el operador actual
            mnemonic = op_to_mnemonic.get(op, op.upper()) # Si no está en el mapeo, usar la versión en mayúsculas

            if op == "=":
                resolved_arg1 = resolve_operand(arg1) 
                self.emit(f"LOAD {resolved_arg1}")
                self.emit(f"STORE {dest}")
            elif op in ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]: 
                self.emit(f"LOAD {str(arg1)}") 
                self.emit(f"{mnemonic} {str(arg2)}") # Usamos el mnemónico aquí
                self.emit(f"STORE {str(dest)}")
            elif op == "!": 
                self.emit(f"LOAD {str(arg1)}")
                self.emit(f"{mnemonic}") # Usamos el mnemónico 'NOT' aquí
                self.emit(f"STORE {str(dest)}")
            elif op.startswith("cast_"): 
                cast_type = op.split('_')[1]
                self.emit(f"LOAD {str(arg1)}")
                self.emit(f"CAST {cast_type}")
                self.emit(f"STORE {str(dest)}")
            elif op == "param":
                self.emit(f"PARAM {str(arg1)}")
            elif op == "call":
                self.emit(f"CALL {str(arg1)}, {str(arg2)}")
                if dest is not None:
                    self.emit(f"STORE {str(dest)}")
            elif op == "return":
                if arg1 is not None:
                    self.emit(f"RETURN {str(arg1)}")
                else:
                    self.emit(f"RETURN")
            elif op == "if_false":
                self.emit(f"IF_FALSE {str(arg1)} GOTO {str(arg2)}")
            elif op == "goto":
                self.emit(f"GOTO {str(arg1)}")
            elif op == "label":
                self.emit(f"LABEL {str(dest)}:")
            else:
                 pass 

    def get_code(self):
        return "\n".join(self.code)



### Prueba con tu Cuádrupla


if __name__ == "__main__":
    print("--- PRUEBA DE OPTIMIZACIÓN CON CUÁDRUPLAS ESPECÍFICAS ---")
    
    # Tu secuencia de cuádruplas
    quads_to_test = [
         ('t1', '=', 5, None),
        ('a', '=', 't1', None),
        ('t2', '=', 3, None),
        ('b', '=', 't2', None),
        ('t3', '+', 'a', 'b'),
        ('c', '=', 't3', None)
    ]

    print("\nCuádruplas de entrada:")
    for i, quad in enumerate(quads_to_test):
        print(f"{i+1:2d}: {quad}")
    
    optimizer = CodeGeneratorob()
    optimizer.generate_code(quads_to_test)
    
    print("\nCódigo ensamblador optimizado:")
    print(optimizer.get_code())
    print("-" * 60)
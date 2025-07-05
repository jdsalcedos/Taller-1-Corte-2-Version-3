# src/vm/virtual_machine.py

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.program_counter = 0
        self.program = []
        self.labels = {}

    def load_program(self, assembly_code_string):
        lines = assembly_code_string.strip().split('\n')
        self.program = []
        self.labels = {}

        for line_num, line in enumerate(lines):
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith(';'):
                continue

            parts = stripped_line.split(' ', 3)
            
            opcode_raw = parts[0]
            operand1_raw = parts[1] if len(parts) > 1 else None
            operand2_raw = parts[2] if len(parts) > 2 else None
            operand3_raw = parts[3] if len(parts) > 3 else None

            if opcode_raw.upper() == "LABEL" and operand1_raw and operand1_raw.endswith(':'):
                label_name = operand1_raw[:-1]
                self.labels[label_name] = len(self.program)
                continue

            if opcode_raw.endswith(':'):
                label_name = opcode_raw[:-1]
                self.labels[label_name] = len(self.program)
                if len(parts) == 1:
                    continue 
                opcode_raw = parts[1] 
                operand1_raw = parts[2] if len(parts) > 2 else None
                operand2_raw = parts[3] if len(parts) > 3 else None
                operand3_raw = None

            # --- Adaptación al formato de instrucciones ---
            if opcode_raw.upper() == "LOAD":
                if operand1_raw.upper() == "TRUE":
                    self.program.append(("PUSH", 1))
                elif operand1_raw.upper() == "FALSE":
                    self.program.append(("PUSH", 0))
                else:
                    try:
                        # Prioritize float conversion if there's a decimal point
                        if '.' in operand1_raw:
                            val = float(operand1_raw)
                        else:
                            val = int(operand1_raw)
                        self.program.append(("PUSH", val))
                    except ValueError:
                        self.program.append(("LOAD_VAR", operand1_raw)) 
            
            elif operand1_raw and operand1_raw.upper() == "STORE":
                try:
                    literal_to_store = int(opcode_raw)
                    target_var = operand2_raw
                    self.program.append(("PUSH_LITERAL_THEN_STORE", literal_to_store, target_var))
                except ValueError:
                    pass
            
            elif opcode_raw.upper() == "STORE":
                self.program.append(("STORE", operand1_raw))

            elif opcode_raw.upper() in ["ADD", "SUB", "MUL", "DIV", "EQ", "NEQ", "LT", "GT", "LE", "GE", "NOT"]:
                self.program.append((opcode_raw.upper(), operand1_raw))

            elif opcode_raw.upper() == "IF_FALSE":
                self.program.append(("LOAD_VAR", operand1_raw)) 
                self.program.append(("JUMPF", operand3_raw)) 

            elif opcode_raw.upper() == "GOTO":
                self.program.append(("JUMP", operand1_raw))

            elif opcode_raw.upper() in ["PRINT", "READ", "CAST", "CALL", "RETURN"]:
                self.program.append((opcode_raw.upper(), operand1_raw))
            
            else:
                raise Exception(f"Instrucción desconocida o formato inesperado en línea {line_num+1}: '{stripped_line}'")
        
        # print(f"DEBUG MV: Programa cargado (adaptado): {self.program}")


    def run(self):
        self.program_counter = 0

        while self.program_counter < len(self.program):
            instruction = self.program[self.program_counter]
            opcode = instruction[0]
            operand1 = instruction[1] if len(instruction) > 1 else None
            
            # print(f"DEBUG MV: PC={self.program_counter}, Instr='{instruction}', Stack={self.stack}, Mem={self.memory}")

            if opcode == "PUSH":
                self.stack.append(operand1) 

            elif opcode == "LOAD_VAR": 
                var_name = operand1
                if var_name in self.memory:
                    self.stack.append(self.memory[var_name])
                else:
                    raise Exception(f"Error de ejecución: Variable no inicializada o inexistente: '{var_name}'")
            
            elif opcode == "PUSH_LITERAL_THEN_STORE": 
                literal_val = operand1 
                var_location = instruction[2] 
                self.stack.append(literal_val) 
                self.memory[var_location] = literal_val 

            elif opcode == "STORE": 
                var_location = operand1
                if not self.stack:
                    raise Exception("Error de ejecución: Pila vacía, no hay valor para STORE")
                value = self.stack[-1] 
                self.memory[var_location] = value 

            elif opcode in ["ADD", "SUB", "MUL", "DIV", "EQ", "NEQ", "LT", "GT", "LE", "GE"]:
                if not self.stack:
                    raise Exception(f"Error de ejecución: Pila vacía, falta el primer operando para {opcode}")

                a = self.stack.pop() 

                b_val = None
                if operand1 is not None: 
                    try:
                        # *** CAMBIO CLAVE AQUÍ: Intentar float antes que int ***
                        if '.' in str(operand1): # Check for decimal point for float conversion
                             b_val = float(operand1)
                        else:
                             b_val = int(operand1) # Otherwise try int
                    except ValueError:
                        if operand1 in self.memory:
                            b_val = self.memory[operand1]
                        else:
                            raise Exception(f"Error de ejecución: Operando desconocido o variable no declarada para {opcode}: '{operand1}'")
                else:
                    if not self.stack:
                        raise Exception(f"Error de ejecución: Pila insuficiente, falta el segundo operando para {opcode}")
                    b_val = self.stack.pop()
                
                result = None
                if opcode == "ADD": result = a + b_val
                elif opcode == "SUB": result = a - b_val
                elif opcode == "MUL": result = a * b_val
                elif opcode == "DIV":
                    if b_val == 0: raise Exception("Error de ejecución: División por cero")
                    result = a / b_val
                elif opcode == "EQ": result = (1 if a == b_val else 0)
                elif opcode == "NEQ": result = (1 if a != b_val else 0)
                elif opcode == "LT": result = (1 if a < b_val else 0)
                elif opcode == "GT": result = (1 if a > b_val else 0)
                elif opcode == "LE": result = (1 if a <= b_val else 0)
                elif opcode == "GE": result = (1 if a >= b_val else 0)

                self.stack.append(result) 

            elif opcode == "NOT":
                if not self.stack: raise Exception("Error de ejecución: Pila vacía para NOT")
                val = self.stack.pop()
                self.stack.append(1 if not val else 0)

            elif opcode == "JUMP":
                label = operand1
                if label not in self.labels:
                    raise Exception(f"Error de ejecución: Etiqueta de salto no encontrada: '{label}'")
                self.program_counter = self.labels[label]
                continue 

            elif opcode == "JUMPF":
                label = operand1
                if not self.stack:
                    raise Exception("Error de ejecución: Pila vacía para JUMPF (se esperaba condición)")
                condition = self.stack.pop()
                if not condition: 
                    if label not in self.labels:
                        raise Exception(f"Error de ejecución: Etiqueta de salto JUMPF no encontrada: '{label}'")
                    self.program_counter = self.labels[label]
                    continue 

            elif opcode == "PRINT":
                if not self.stack: raise Exception("Error de ejecución: Pila vacía para PRINT")
                val_to_print = self.stack.pop()
                print(f"OUTPUT: {val_to_print}")

            elif opcode == "READ":
                var_location = operand1
                user_input = input(f"INPUT ({var_location}): ")
                try:
                    if '.' in user_input: self.memory[var_location] = float(user_input)
                    else: self.memory[var_location] = int(user_input)
                except ValueError:
                    self.memory[var_location] = user_input

            elif opcode == "CAST":
                if not self.stack: raise Exception("Error de ejecución: Pila vacía para CAST")
                value = self.stack.pop()
                target_type = operand1.lower()
                if target_type == "int": self.stack.append(int(value))
                elif target_type == "float": self.stack.append(float(value))
                elif target_type == "bool": self.stack.append(bool(value))
                else: raise Exception(f"Error de ejecución: Tipo de cast no soportado: '{target_type}'")

            elif opcode == "CALL":
                func_name, num_params_str = operand1.split(',')
                num_params = int(num_params_str.strip())
                if len(self.stack) < num_params:
                    raise Exception(f"Error de ejecución: No hay suficientes parámetros en la pila para CALL {func_name}")
                print(f"DEBUG MV: Llamando a función '{func_name.strip()}' con {num_params} parámetros (simulado)")

            elif opcode == "RETURN":
                if self.stack: print(f"DEBUG MV: Retornando de función con valor: {self.stack[-1]} (simulado)")
                else: print("DEBUG MV: Retornando de función sin valor (simulado)")
                break 

            else:
                raise Exception(f"Instrucción desconocida o formato inesperado: '{opcode}'")
            
            self.program_counter += 1 

    def get_final_stack_top(self):
        return self.stack[-1] if self.stack else None

    def get_memory_state(self):
        return self.memory
    

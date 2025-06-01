import json
import sys
import os

class Translator:
    def __init__(self, tree, symbol_table):
        self.AST = tree
        self.symbol_table = symbol_table
        self.vm_code = [] 
        self.label_counter = 0

    def generate_label(self, prefix="L"):
        self.label_counter += 1
        return f"{prefix.upper()}{self.label_counter}"

    def add_instruction(self, instruction, comment=None, no_tab=0):
        if comment:
            self.vm_code.append(f"    {instruction:<15} // {comment}")
        elif no_tab:
            self.vm_code.append(f"{instruction}")
        else:
            self.vm_code.append(f"    {instruction}")

    def add_label(self, label_name, comment=None):
        if comment:
             self.vm_code.append(f"// {comment}")
        self.vm_code.append(f"{label_name}:")

    def translate(self):
        try:
            if self.AST[0] == "PROGRAM" and len(self.AST) > 2 and \
               isinstance(self.AST[2], (list, tuple)) and self.AST[2][0] == "PROGRAM_BODY" and \
               len(self.AST[2]) > 1:
                   
                program_node = self.AST
                program_body_node = program_node[2] 
                declaration_part_node = program_body_node[1] 
                block_node = program_body_node[2]
                   
                if declaration_part_node and declaration_part_node[0] == "DECLARATIONS" and declaration_part_node[1]:
                    actual_declarations_list = declaration_part_node[1]
                    for decl_group_node in actual_declarations_list:
                        if decl_group_node and decl_group_node[0] == "VAR_DECLARATIONS":
                            var_list_node = decl_group_node[1]
                            if var_list_node:
                                for var_item_node in var_list_node:
                                    iD_list_names = var_item_node[1]
                                    type_node = var_item_node[2]

                                    for name_str in iD_list_names:
                                        name_lower_str = name_str.lower()
                                        if type_node[0] == "TYPE": 
                                            self.add_instruction(f"PUSHI 0", f"aloca espaço para variável '{name_str}'")
                                        elif type_node[0] == "ARRAY_TYPE": 
                                            try:
                                                array_info = self.symbol_table.get_array_info(name_lower_str)
                                                self.add_instruction(f"PUSHN {array_info['size']}", f"aloca {array_info['size']} posições para array '{name_str}'")
                                            except ValueError as e:
                                                raise ValueError(f"while getting array info for {name_str} during PUSHN generation: {e}")

                self.add_instruction("START",None,1)
                self.translate_node(block_node)
            else:
                 raise ValueError("unexpected PROGRAM structure for translation.")

            self.add_instruction("STOP",None,1)
            return "\n".join(self.vm_code) + "\n"

        except ValueError as e:
             raise
        except Exception as e: 
            raise


    def translate_node(self, node):
        if not isinstance(node, (list, tuple)) or not node:
            return 

        node_type = node[0]
        
        if node_type == "PROGRAM" or node_type == "PROGRAM_BODY" or node_type == "DECLARATIONS":
            pass 
        elif node_type == "VAR_DECLARATIONS":
            pass
        elif node_type == "FUNCTION_DECLARATION":
            pass
        elif node_type == "VAR_ITEM" or node_type == "TYPE" or node_type == "ARRAY_TYPE" or node_type == "PARAMETER":
             pass 
        elif node_type == "BLOCK" or node_type == "COMPOUND": 
            self.translate_block(node)
        elif node_type == "FUNCTION_BODY": 
            raise ValueError("user-defined functions (FUNCTION_BODY) are not supported for code generation.")
        elif node_type == "ASSIGN": 
            self.translate_assign(node)
        elif node_type == "ARRAY_ASSIGN": 
             self.translate_array_assign(node)
        elif node_type == "WRITELN":
            self.translate_writeLn(node)
        elif node_type == "WRITE":
            self.translate_write(node)
        elif node_type == "READLN":
            self.translate_readLn(node)
        elif node_type == "READ":
            self.translate_read(node)
        elif node_type == "IF":
            self.translate_if(node)
        elif node_type == "WHILE":
             self.translate_while(node)
        elif node_type == "FOR":
            self.translate_for(node)
        elif node_type == "FUNCTION_CALL": 
            self.translate_function_call_expr(node)
        elif node_type == "FUNCTION_CALL_STATEMENT": 
            pass
        elif node_type == "ARRAY_ACCESS": 
             self.translate_array_access_expr(node)
        elif node_type in ["+", "-", "*", "div", "mod"]: 
            self.translate_binary_OP(node)
        elif node_type == "/": 
            self.translate_binary_OP(node)
        elif node_type in ["=", "<>", "<", ">", "<=", ">="]: 
            self.translate_comparison_OP(node)
        elif node_type in ["and", "or"]: 
             self.translate_logical_OP(node)
        elif node_type == "not": 
             self.translate_unary_OP(node)
        elif node_type == "ID": 
            self.translate_ID_expr(node) 
        elif node_type == "NUMBER": 
            self.add_instruction(f"PUSHI {node[1]}")
        elif node_type == "REAL_NUMBER": 
            self.add_instruction(f"PUSHF {node[1]}")
        elif node_type == "STRING" or node_type == "STRING_LITERAL": 
             string_val = node[1].replace('"', '""')
             self.add_instruction(f'PUSHS "{string_val}"')
        elif node_type == "BOOLEAN": 
             bool_val_AST = node[1] 
             is_true = (isinstance(bool_val_AST, bool) and bool_val_AST) or \
                       (isinstance(bool_val_AST, str) and bool_val_AST.lower() == 'true')
             value_to_push = 1 if is_true else 0
             self.add_instruction(f"PUSHI {value_to_push}")
        elif node_type == "UMINUS": 
            self.translate_node(node[1]) 
            val_type = self.symbol_table.infer_expression_type(node[1]) 
            # negação de inteiros ou reais
            if val_type == 'integer':
                self.add_instruction("PUSHI -1")
                self.add_instruction("MUL")
            elif val_type == 'real':
                self.add_instruction("PUSHF -1.0") 
                self.add_instruction("FMUL")
            else:
                raise ValueError(f"unary minus not supported for type '{val_type}'.")
        else:
            print(f"[WARNING]: ignoring unknown node type during translation: {node_type}", file=sys.stderr)

    def translate_block(self, node):
        statements = node[1] if node[1] is not None else []
        for statement in statements:
            self.translate_node(statement)

    def translate_assign(self, node):
        target_info = node[1] 
        expression_right = node[2]

        if not (isinstance(target_info, (list, tuple)) and target_info[0] == 'ID'):
             raise ValueError(f"invalid target for simple assignment: {target_info}")

        var_name = target_info[1]
        left_type = self.symbol_table.lookup_identifier_type(var_name)
        if left_type.startswith("array of"):
            raise ValueError(f"cannot assign directly to an array name '{var_name}'. Use indexing.")

        var_address = self.symbol_table.get_variable_address(var_name)
        self.translate_node(expression_right)
        right_type = self.symbol_table.infer_expression_type(expression_right) 

        # tratamento de conversão de tipo inteiro para real ou string para char.
        if left_type != right_type:
            if left_type == 'real' and right_type == 'integer':
                self.add_instruction("ITOF", "converte inteiro para real") 
            elif left_type == 'integer' and right_type == 'char': 
                pass 
            elif left_type == 'char' and right_type == 'integer': 
                pass 
            elif left_type == 'char' and right_type == 'string':
                self.add_instruction("PUSHI 0") 
                self.add_instruction("CHARAT", "obtém primeiro char. da string")
            else:
                raise ValueError(f"type mismatch in assignment to '{var_name}': cannot assign type '{right_type}' to variable of type '{left_type}'.")
        self.add_instruction(f"STOREG {var_address}", f"guarda valor em '{var_name}'")

    def translate_array_assign(self, node):
        if len(node) != 3:
             raise ValueError(f"invalid ARRAY_ASSIGN structure: expected 3 elements, got {len(node)} -> {node}")

        array_access_node = node[1]
        value_expression_right = node[2] 

        if not (isinstance(array_access_node, (list, tuple)) and len(array_access_node) == 3 and
                array_access_node[0] == 'ARRAY_ACCESS' and
                isinstance(array_access_node[1], (list, tuple)) and array_access_node[1][0] == 'ID'):
             raise ValueError(f"invalid ARRAY_ACCESS node within ARRAY_ASSIGN: {array_access_node}")

        array_name_info = array_access_node[1] 
        index_expr_node = array_access_node[2]
        array_name = array_name_info[1]

        array_info = self.symbol_table.get_array_info(array_name)
        declared_element_type = array_info['element_type']
        
        # cálculo do endereço do elemento do array: base + (índice - início_array)
        self.add_instruction(f"PUSHGP")
        self.add_instruction(f"PUSHI {array_info['base_address']}", f"endereço base do array '{array_name}'")
        self.add_instruction("PADD", f"calcula endereço absoluto do array '{array_name}'")
        
        self.translate_node(index_expr_node) 
        index_expr_type = self.symbol_table.infer_expression_type(index_expr_node) 
        if index_expr_type != 'integer':
            raise ValueError(f"array index for '{array_name}' must be integer, but is '{index_expr_type}'.")

        self.add_instruction(f"PUSHI {array_info['start_index']}", f"índice inicial do array ({array_info['start_index']})")
        self.add_instruction("SUB", "calcula deslocamento relativo ao início (base 0)")
        
        self.translate_node(value_expression_right)
        right_value_type = self.symbol_table.infer_expression_type(value_expression_right) 
        
        # conversão de tipo ao atribuir a um elemento do array
        if declared_element_type != right_value_type:
            if declared_element_type == 'real' and right_value_type == 'integer':
                self.add_instruction("ITOF", "converte inteiro para real")
            elif declared_element_type == 'integer' and right_value_type == 'char': 
                pass
            elif declared_element_type == 'char' and right_value_type == 'integer': 
                pass
            elif declared_element_type == 'char' and right_value_type == 'string':
                self.add_instruction("PUSHI 0")
                self.add_instruction("CHARAT", "obtém primeiro char da string")
            else:
                raise ValueError(f"type mismatch in assignment to array element '{array_name}': cannot assign type '{right_value_type}' to element of type '{declared_element_type}'.")
        self.add_instruction("STOREN", f"guarda em {array_name}[deslocamento]")

    def translate_write_args(self, args, is_writeLn):
        if not args: 
            if is_writeLn:
                self.add_instruction("WRITELN")
            return

        for i, arg_expr_node in enumerate(args):
            self.translate_node(arg_expr_node)
            expr_type = self.symbol_table.infer_expression_type(arg_expr_node) 
            
            # seleção da instrução WRITE correta com base no tipo da expressão
            if expr_type == 'integer':
                 self.add_instruction("WRITEI")
            elif expr_type == 'string':
                 self.add_instruction("WRITES")
            elif expr_type == 'real':
                 self.add_instruction("WRITEF")
            elif expr_type == 'boolean':
              self.add_instruction("WRITEI")
            elif expr_type == 'char':
              self.add_instruction("WRITECHR")
            elif expr_type and expr_type.startswith("array of"):
                self.add_instruction("POP 1") 
                array_name_for_msg = arg_expr_node[1] if isinstance(arg_expr_node, (list, tuple)) and arg_expr_node[0] == "ID" else "array"
                self.add_instruction(f'PUSHS "Nao pode imprimir array \'{array_name_for_msg}\' diretamente."')
                self.add_instruction("WRITES")
            else:
                print(f"WARNING TRADUTOR: WRITELN/WRITE attempting to write potentially unsupported type '{expr_type}' for {str(arg_expr_node)[:30]}...", file=sys.stderr)
                self.add_instruction("WRITEI") 
        
        if is_writeLn:
            self.add_instruction("WRITELN")

    def translate_writeLn(self, node):
        args = node[1] if len(node) > 1 else []
        self.translate_write_args(args, is_writeLn=True)

    def translate_write(self, node):
        args = node[1] if len(node) > 1 else []
        if not args:
             raise ValueError("WRITE statement requires arguments.")
        self.translate_write_args(args, is_writeLn=False)

    def translate_read_args(self, args, is_readLn):
        # trata a leitura para variáveis simples e elementos de array, com conversão de tipo
        if not args: 
            if is_readLn:
                self.add_instruction("READ")
                self.add_instruction("POP 1") 
            return

        for i, target_node in enumerate(args):
            if isinstance(target_node, (list, tuple)) and target_node[0] == 'ID':
                var_name = target_node[1]
                var_address = self.symbol_table.get_variable_address(var_name)
                target_type = self.symbol_table.lookup_identifier_type(var_name)

                self.add_instruction("READ") 

                if target_type == 'integer':
                    self.add_instruction("ATOI")
                elif target_type == 'real':
                    self.add_instruction("ATOF")
                elif target_type == 'string':
                    pass 
                elif target_type == 'boolean':
                     self.add_instruction("ATOI")
                elif target_type == 'char':
                    self.add_instruction("PUSHI 0") 
                    self.add_instruction("CHARAT", "obtém primeiro char da string lida")
                else:
                     self.add_instruction("POP 1") 
                     raise ValueError(f"cannot read into variable '{var_name}' of type '{target_type}'.")
                self.add_instruction(f"STOREG {var_address}", f"guarda em '{var_name}'")

            elif isinstance(target_node, (list, tuple)) and target_node[0] == 'ARRAY_ACCESS':
                 array_name_id_node = target_node[1] 
                 index_expr_node = target_node[2]
                 array_name = array_name_id_node[1]

                 array_info = self.symbol_table.get_array_info(array_name)
                 target_element_type = array_info['element_type']

                 self.add_instruction(f"PUSHGP")
                 self.add_instruction(f"PUSHI {array_info['base_address']}", f"endereço base do array '{array_name}'")
                 self.add_instruction("PADD", "calcula endereço absoluto")
                 
                 self.translate_node(index_expr_node)
                 index_expr_type = self.symbol_table.infer_expression_type(index_expr_node) 
                 if index_expr_type != 'integer':
                     raise ValueError(f"array index for '{array_name}' in READ must be integer, got '{index_expr_type}'.")
                 self.add_instruction(f"PUSHI {array_info['start_index']}", f"índice inicial do array")
                 self.add_instruction("SUB", "calcula deslocamento") 
                 
                 self.add_instruction("READ") 
                 
                 if target_element_type == 'integer':
                     self.add_instruction("ATOI")
                 elif target_element_type == 'real':
                     self.add_instruction("ATOF")
                 elif target_element_type == 'string':
                     pass 
                 elif target_element_type == 'boolean':
                      self.add_instruction("ATOI")
                 elif target_element_type == 'char':
                    self.add_instruction("PUSHI 0") 
                    self.add_instruction("CHARAT", "obtém primeiro char. da string")
                 else:
                      self.add_instruction("POP 3") 
                      raise ValueError(f"cannot read into array element '{array_name}' of type '{target_element_type}'.")
                 self.add_instruction("STOREN", f"guarda em {array_name}[deslocamento]")
            else:
                 raise ValueError(f"unsupported target for READ/READLN: {target_node}")

    def translate_readLn(self, node):
        args = node[1] if len(node) > 1 else []
        self.translate_read_args(args, is_readLn=True)
        if not args: 
             self.add_instruction("READ")
             self.add_instruction("POP 1")

    def translate_read(self, node):
        args = node[1] if len(node) > 1 else []
        if not args:
            raise ValueError("READ statement requires at least one argument.")
        self.translate_read_args(args, is_readLn=False)

    def translate_if(self, node):
        # gestão de labels para saltos condicionais e incondicionais
        condition_expr_node = node[1]
        then_statement_node = node[2]
        else_statement_node = node[3] if len(node) > 3 else None

        else_label = self.generate_label("IFELSE")
        endif_label = self.generate_label("IFEND")

        self.translate_node(condition_expr_node) 
        cond_type = self.symbol_table.infer_expression_type(condition_expr_node) 
        if cond_type != 'boolean':
            raise ValueError(f"IF condition must be of boolean type, but is '{cond_type}'. Expression: {condition_expr_node}")

        self.add_instruction(f"JZ {else_label if else_statement_node else endif_label}")

        self.translate_node(then_statement_node)
        if else_statement_node is not None:
             self.add_instruction(f"JUMP {endif_label}")

        if else_statement_node is not None:
            self.add_label(else_label)
            self.translate_node(else_statement_node)
        elif else_label != endif_label : 
             self.add_label(else_label) # garante que o label existe mesmo sem 'else'
        
        self.add_label(endif_label)

    def translate_while(self, node):
        # define labels para o início e fim do ciclo, com saltos condicionais
        condition_expr_node = node[1]
        body_statement_node = node[2]

        loop_start_label = self.generate_label("WHILESTART")
        loop_end_label = self.generate_label("WHILEEND")

        self.add_label(loop_start_label, "início do ciclo while")
        self.translate_node(condition_expr_node) 
        cond_type = self.symbol_table.infer_expression_type(condition_expr_node) 
        if cond_type != 'boolean':
            raise ValueError(f"WHILE condition must be of boolean type, but is '{cond_type}'. Expression: {condition_expr_node}")

        self.add_instruction(f"JZ {loop_end_label}")
        self.translate_node(body_statement_node)
        self.add_instruction(f"JUMP {loop_start_label}")
        self.add_label(loop_end_label, "fim do ciclo while")

    def translate_for(self, node):
        # lógica para inicializar, testar e incrementar/decrementar a variável de controlo do ciclo
        loop_var_id_node = node[1]    
        start_expr_node = node[2]
        direction_str = node[3]       
        end_expr_node = node[4]
        body_statement_node = node[5]

        loop_var_name = loop_var_id_node[1]
        loop_var_address = self.symbol_table.get_variable_address(loop_var_name)
        loop_var_type = self.symbol_table.lookup_identifier_type(loop_var_name)

        if loop_var_type != 'integer': 
            raise ValueError(f"FOR loop variable '{loop_var_name}' must be of integer type, but is '{loop_var_type}'.")

        loop_body_label = self.generate_label("FORBODY")
        loop_test_label = self.generate_label("FORTEST")
        loop_end_label = self.generate_label("FOREND")

        self.translate_node(start_expr_node) 
        start_expr_type = self.symbol_table.infer_expression_type(start_expr_node) 
        if start_expr_type != 'integer':
             raise ValueError(f"FOR loop start expression for '{loop_var_name}' must be integer, but is '{start_expr_type}'.")
        self.add_instruction(f"STOREG {loop_var_address}", f"ciclo FOR: inicializa '{loop_var_name}'")
        self.add_instruction(f"JUMP {loop_test_label}")

        self.add_label(loop_body_label, "corpo do ciclo for")
        self.translate_node(body_statement_node)

        self.add_instruction(f"PUSHG {loop_var_address}") 
        self.add_instruction("PUSHI 1")                   
        if direction_str.lower() == "to":
            self.add_instruction("ADD")
        elif direction_str.lower() == "downto":
            self.add_instruction("SUB")
        else:
             raise ValueError(f"unknown direction in FOR loop: {direction_str}")
        self.add_instruction(f"STOREG {loop_var_address}", f"atualiza '{loop_var_name}'")

        self.add_label(loop_test_label, "teste do ciclo for")
        self.add_instruction(f"PUSHG {loop_var_address}")
        self.translate_node(end_expr_node)
        end_expr_type = self.symbol_table.infer_expression_type(end_expr_node) 
        if end_expr_type != 'integer':
             raise ValueError(f"FOR loop end expression for '{loop_var_name}' must be integer, but is '{end_expr_type}'.")
        
        if direction_str.lower() == "to":
            self.add_instruction("INFEQ") 
            self.add_instruction(f"JZ {loop_end_label}") 
        elif direction_str.lower() == "downto":
            self.add_instruction("SUPEQ") 
            self.add_instruction(f"JZ {loop_end_label}") 
        
        self.add_instruction(f"JUMP {loop_body_label}")
        self.add_label(loop_end_label, "fim do ciclo for")

    def translate_function_call_expr(self, node):
        func_name = node[1]
        arg_nodes = node[2] if len(node) > 2 and node[2] is not None else []
        func_name_lower = func_name.lower()

        if func_name_lower == "length":
            if len(arg_nodes) != 1:
                raise ValueError(f"function 'length' expects 1 argument, got {len(arg_nodes)}")
            self.translate_node(arg_nodes[0])
            arg_type = self.symbol_table.infer_expression_type(arg_nodes[0]) 
            if arg_type != 'string':
                raise ValueError(f"'length' expects a string argument, got {arg_type}")
            self.add_instruction("STRLEN")
        else:
             raise ValueError(f"function call '{func_name}' is not a recognized built-in function.")

    def translate_array_access_expr(self, node):
        # acesso a char. de string (índice base-1 em PASCAL) ou elemento de array
        if not (isinstance(node, (list, tuple)) and len(node) == 3 and
                isinstance(node[1], (list, tuple)) and node[1][0] == 'ID'):
            raise ValueError(f"invalid ARRAY_ACCESS structure: {node}")

        var_name_ID_node = node[1] 
        index_expr_node = node[2]
        var_name = var_name_ID_node[1]
        base_type_info = self.symbol_table.lookup_identifier_type(var_name)
        index_expr_type = self.symbol_table.infer_expression_type(index_expr_node)

        if index_expr_type != 'integer':
            raise ValueError(f"index for '{var_name}' must be integer, but is '{index_expr_type}'. expression: {index_expr_node}")

        if base_type_info == 'string': 
            var_address = self.symbol_table.get_variable_address(var_name)
            self.add_instruction(f"PUSHG {var_address}", f"carrega string '{var_name}'")
            self.translate_node(index_expr_node) 
            self.add_instruction("PUSHI 1") 
            self.add_instruction("SUB", "ajusta índice PASCAL (base 1) para VM (base 0)")    
            self.add_instruction("CHARAT") 
            
        elif base_type_info and base_type_info.startswith('array of '):
             array_info = self.symbol_table.get_array_info(var_name)
             self.add_instruction(f"PUSHGP")
             self.add_instruction(f"PUSHI {array_info['base_address']}", f"endereço base do array '{var_name}'")
             self.add_instruction("PADD", "calcula endereço absoluto")
             self.translate_node(index_expr_node)
             self.add_instruction(f"PUSHI {array_info['start_index']}", f"índice inicial do array")
             self.add_instruction("SUB", "calcula deslocamento") 
             self.add_instruction("LOADN", "carrega valor do elemento do array")
        else:
             raise ValueError(f"identifier '{var_name}' is not an array or string, or not declared for indexing.")


    def translate_binary_OP(self, node):
        OP_symbol = node[0]
        left_expr_node = node[1]
        right_expr_node = node[2]
    
        self.translate_node(left_expr_node)
        left_type = self.symbol_table.infer_expression_type(left_expr_node)
        self.translate_node(right_expr_node)
        right_type = self.symbol_table.infer_expression_type(right_expr_node)
    
        VM_instr = None
        is_real_opr = (left_type == 'real' or right_type == 'real') or OP_symbol == '/'
    
        if is_real_opr:
            if left_type == 'integer' and right_type == 'real':
                self.add_instruction("SWAP")
                self.add_instruction("ITOF", "converte operando esq. para real")
                self.add_instruction("SWAP")
            elif left_type == 'real' and right_type == 'integer':
                self.add_instruction("ITOF", "converte operando dir. para real")
            elif left_type == 'integer' and right_type == 'integer' and OP_symbol == '/':
                self.add_instruction("ITOF", "converte operando dir. para real (divisão real)")
                self.add_instruction("SWAP")
                self.add_instruction("ITOF", "converte operando esq. para real (divisão real)")
                self.add_instruction("SWAP")
    
            opr_map_real = {'+': "FADD", '-': "FSUB", '*': "FMUL", '/': "FDIV"}
            VM_instr = opr_map_real.get(OP_symbol)
            if not VM_instr:
                raise ValueError(f"real arithmetic operator '{OP_symbol}' not supported or invalid type combination.")
    
        elif left_type == 'integer' and right_type == 'integer':
            opr_map_int = {'+': "ADD", '-': "SUB", '*': "MUL", 'div': "DIV", 'mod': "MOD"}
            VM_instr = opr_map_int.get(OP_symbol)
            if not VM_instr:
                 raise ValueError(f"integer arithmetic operator '{OP_symbol}' not supported.")
    
        elif (left_type == 'char' or right_type == 'char') and OP_symbol in ['+', '-']: 
            if not ((left_type == 'char' and right_type == 'integer') or \
                    (left_type == 'integer' and right_type == 'char') or \
                    (left_type == 'char' and right_type == 'char')):
                raise ValueError(f"unsupported char arithmetic with '{left_type}', '{right_type}' for '{OP_symbol}'")
    
            opr_map_char_int = {'+': "ADD", '-': "SUB"}
            VM_instr = opr_map_char_int.get(OP_symbol)
            if not VM_instr:
                 raise ValueError(f"char arithmetic operator '{OP_symbol}' not supported.")
    
        elif left_type == 'string' and right_type == 'string' and OP_symbol == '+':
            self.add_instruction("SWAP")
            VM_instr = "CONCAT"
    
        else:
            raise ValueError(f"incompatible types for arithmetic operator '{OP_symbol}': '{left_type}' and '{right_type}'.")
    
        if VM_instr: 
             self.add_instruction(VM_instr)

    def translate_comparison_OP(self, node):
        opr_symbol = node[0]
        left_expr_node = node[1]
        right_expr_node = node[2]

        self.translate_node(left_expr_node)
        left_type = self.symbol_table.infer_expression_type(left_expr_node) 
        self.translate_node(right_expr_node)
        right_type = self.symbol_table.infer_expression_type(right_expr_node) 

        VM_instr = None
        needs_not_for_NEQ = (opr_symbol == '<>')

        if (left_type == 'real' or right_type == 'real'):
            if left_type == 'integer' and right_type == 'real':
                self.add_instruction("SWAP") 
                self.add_instruction("ITOF", "converte operando esq. para real")
                self.add_instruction("SWAP")
            elif left_type == 'real' and right_type == 'integer':
                self.add_instruction("ITOF", "converte operando dir. para real")
            
            if opr_symbol == '=':
                VM_instr = "EQUAL"
            elif opr_symbol == '<>':
                VM_instr = "EQUAL" 
            else:
                opr_map_real_others = {'<': "FINF", '>': "FSUP", '<=': "FINFEQ", '>=': "FSUPEQ"}
                VM_instr = opr_map_real_others.get(opr_symbol)

            if not VM_instr:
                raise ValueError(f"Real comparison operator '{opr_symbol}' not supported.")

        elif (left_type in ['integer', 'boolean', 'char']) and \
             (right_type in ['integer', 'boolean', 'char']):
            opr_map_int = {'=': "EQUAL", '<>': "EQUAL", '<': "INF", '>': "SUP", '<=': "INFEQ", '>=': "SUPEQ"}
            VM_instr = opr_map_int.get(opr_symbol)
            if not VM_instr: raise ValueError(f"integer/Boolean/Char comparison '{opr_symbol}' not supported.")

        elif left_type == 'string' and right_type == 'string':
            if opr_symbol in ['=', '<>']: 
                VM_instr = "EQUAL" 
            else: 
                raise ValueError(f"string comparison '{opr_symbol}' (other than '=','<>') not directly supported.")
        
        elif left_type == 'char' and right_type == 'string' and \
             isinstance(right_expr_node, (list,tuple)) and right_expr_node[0] in ('STRING', 'STRING_LITERAL') and len(right_expr_node[1]) == 1:
            char_literal = right_expr_node[1]
            ASCII_literal = ord(char_literal)
            self.add_instruction("POP 1") 
            self.add_instruction(f"PUSHI {ASCII_literal}")
            opr_map_char_cmp = {'=': "EQUAL", '<>': "EQUAL", '<': "INF", '>': "SUP", '<=': "INFEQ", '>=': "SUPEQ"}
            VM_instr = opr_map_char_cmp.get(opr_symbol)

        elif right_type == 'char' and left_type == 'string' and \
             isinstance(left_expr_node, (list,tuple)) and left_expr_node[0] in ('STRING', 'STRING_LITERAL') and len(left_expr_node[1]) == 1:
            char_literal = left_expr_node[1]
            ASCII_literal = ord(char_literal)
            self.add_instruction("SWAP") 
            self.add_instruction("POP 1") 
            self.add_instruction(f"PUSHI {ASCII_literal}") 
            self.add_instruction("SWAP") 
            opr_map_char_cmp = {'=': "EQUAL", '<>': "EQUAL", '<': "INF", '>': "SUP", '<=': "INFEQ", '>=': "SUPEQ"}
            VM_instr = opr_map_char_cmp.get(opr_symbol)
        else:
            if left_type is None or right_type is None:
                 raise ValueError(f"could not determine types for comparison '{opr_symbol}'. Left: {left_expr_node}, Right: {right_expr_node}")
            else:
                 raise ValueError(f"cannot compare types '{left_type}' and '{right_type}' with operator '{opr_symbol}'.")

        if VM_instr:
             self.add_instruction(VM_instr)
             if needs_not_for_NEQ:
                 self.add_instruction("NOT")
        else: 
            raise ValueError(f"comparison operator or type combination not supported: {opr_symbol} between {left_type} and {right_type}")

    def translate_logical_OP(self, node):
        opr_symbol = node[0]
        left_expr_node = node[1]
        right_expr_node = node[2]

        self.translate_node(left_expr_node)
        left_type = self.symbol_table.infer_expression_type(left_expr_node)
        if left_type != 'boolean':
            raise ValueError(f"left operand of '{opr_symbol}' must be boolean, got '{left_type}'. Expression: {left_expr_node}")

        if opr_symbol == 'and':
            false_label = self.generate_label("ANDFALSE")
            end_label = self.generate_label("ANDEND")
            
            self.add_instruction(f"JZ {false_label}", f"se lado esq. do AND é falso, salta (consome valor)")
            
            self.translate_node(right_expr_node)
            right_type = self.symbol_table.infer_expression_type(right_expr_node)
            if right_type != 'boolean':
                raise ValueError(f"right operand of 'and' must be boolean, got '{right_type}'. Expression: {right_expr_node}")
            self.add_instruction(f"JUMP {end_label}")
            
            self.add_label(false_label)
            self.add_instruction("PUSHI 0", "resultado do AND é falso")
            
            self.add_label(end_label)

        elif opr_symbol == 'or':
            true_label = self.generate_label("ORTRUE")
            end_label = self.generate_label("OREND")
            
            self.add_instruction("NOT", "inverte lado esq. para lógica OR com JZ") 
            self.add_instruction(f"JZ {true_label}", "se (NOT lado esq.) é falso (lado esq. era verdadeiro), salta (consome valor)")

            self.translate_node(right_expr_node)
            right_type = self.symbol_table.infer_expression_type(right_expr_node)
            if right_type != 'boolean':
                raise ValueError(f"right operand of 'or' must be boolean, got '{right_type}'. Expression: {right_expr_node}")
            self.add_instruction(f"JUMP {end_label}")

            self.add_label(true_label)
            self.add_instruction("PUSHI 1", "resultado do OR é verdadeiro")
            
            self.add_label(end_label)
        else:
             raise ValueError(f"logical operator not supported: {opr_symbol}")


    def translate_unary_OP(self, node):
        opr_symbol = node[0]
        expr_node = node[1]

        self.translate_node(expr_node) 
        expr_type = self.symbol_table.infer_expression_type(expr_node) 
        if expr_type != 'boolean': # 'not' só se aplica a booleanos
            raise ValueError(f"operand of '{opr_symbol}' must be boolean, but is '{expr_type}'. Expression: {expr_node}")

        if opr_symbol == 'not':
             self.add_instruction("NOT")
        else: # UMINUS é tratado na função principal 'translate_node'
             raise ValueError(f"unary operator {opr_symbol} not supported here")

    def translate_ID_expr(self, node):
        var_name = node[1]
        var_type = self.symbol_table.lookup_identifier_type(var_name)

        if var_type.startswith("array of"):
             raise ValueError(f"cannot use array name '{var_name}' directly as a value in this context. Use indexing.")
        
        if var_name.lower() in self.symbol_table.functions and var_name.lower() != 'length':
             raise ValueError(f"cannot use function name '{var_name}' as a variable directly.")

        var_address = self.symbol_table.get_variable_address(var_name)
        self.add_instruction(f"PUSHG {var_address}", f"carrega valor da variável global '{var_name}' (tipo {var_type})")
import sys

class SymbolTable:
    """
    tabela de símbolos (variáveis, arrays e funções) e os metadados/endereços de memória.
    considera o espaço de memória global e o respetivo apontador GP.
    """
    def __init__(self):
        # variáveis simples: {nome: endereço (offset do GP)}
        self.symbols = {}
        # tipos de variáveis simples: {nome: tipo ('integer', 'string', 'real', 'boolean', 'char')}
        self.symbol_types = {}
        # metadados de arrays: {nome: {'base_address': offset, 'start_index': int, 'size': int, 'element_type': str}}
        self.arrays = {}
        # assinaturas de funções: {nome_func: {'params': [{'name': str, 'type': str}], 'return_type': str, 'label': str}}
        self.functions = {
            'length': {'params': [{'name': 's', 'type': 'string'}], 'return_type':'integer', 'label':None} # função pré-definida
        }
        # contador para o próximo endereço de memória global disponível
        self.next_address = 0
        self.valid_types = ['integer', 'string', 'boolean', 'real', 'char']


    def add_symbol(self, name, type_info, is_param=False, func_name=None):
        """adiciona um símbolo de variável à tabela de símbolos."""
        name_lower = name.lower()
        if name_lower in self.symbols or name_lower in self.arrays or name_lower in self.functions:
            raise ValueError(f"identifier '{name}' already declared.")

        type_info_lower = type_info.lower()
        if type_info_lower not in self.valid_types:
            raise ValueError(f"unknown scalar type '{type_info}' for variable '{name}'.")

        address = self.next_address
        self.symbols[name_lower] = address
        self.symbol_types[name_lower] = type_info_lower
        self.next_address += 1
        return address

    def add_array(self, name, start_index, end_index, element_type_str):
        """adiciona um símbolo de array e reserva os espaços necessários."""
        name_lower = name.lower()
        if name_lower in self.symbols or name_lower in self.arrays or name_lower in self.functions:
            raise ValueError(f"identifier '{name}' already declared.")

        size = end_index - start_index + 1
        if size <= 0:
            raise ValueError(f"array size for '{name}' must be positive (end >= start). start = {start_index}, end = {end_index}")

        element_type_lower = element_type_str.lower()
        if element_type_lower not in self.valid_types:
            raise ValueError(f"unknown array element type: '{element_type_str}' for array '{name}'.")

        base_addr = self.next_address
        self.arrays[name_lower] = {
            'base_address': base_addr,
            'start_index': start_index,
            'size': size,
            'element_type': element_type_lower
        }
        self.next_address += size

    def lookup_identifier_type(self, name):
        """procura um identificador (variável, array, função) e retorna o respetivo tipo ou assinatura."""
        name_lower = name.lower()
        if name_lower in self.symbol_types:
            return self.symbol_types[name_lower]
        if name_lower in self.arrays:
            return f"array of {self.arrays[name_lower]['element_type']}"
        if name_lower in self.functions:
            return self.functions[name_lower]['return_type']
        raise ValueError(f"identifier '{name}' not declared.")

    def get_variable_address(self, name):
        """retorna o endereço de memória de uma variável simples."""
        name_lower = name.lower()
        if name_lower in self.arrays:
            raise ValueError(f"attempted to use array '{name}' as a simple variable to get address.")
        address = self.symbols.get(name_lower)
        if address is None:
            if name_lower in self.functions:
                raise ValueError(f"cannot get address of function '{name}'.")
            raise ValueError(f"variable '{name}' not declared.")
        return address

    def get_array_info(self, name):
        """retorna metadados de um array."""
        name_lower = name.lower()
        if name_lower in self.symbols:
            raise ValueError(f"attempted to use simple variable '{name}' as an array.")
        array_info = self.arrays.get(name_lower)
        if array_info is None:
            raise ValueError(f"array '{name}' not declared.")
        return array_info

    def get_function_signature(self, name):
        """retorna a assinatura de uma função (parâmetros e tipo que retorna)."""
        name_lower = name.lower()
        signature = self.functions.get(name_lower)
        if signature is None:
            raise ValueError(f"function '{name}' not defined.")
        return signature

    def get_total_memory_slots(self):
        """retorna o número total de endereços de memória global alocados."""
        return self.next_address

    def infer_expression_type(self, node):
        """infere o tipo de uma expressão com base no nó (usa self para acesso à tabela)."""
        if not isinstance(node, (list, tuple)) or not node: return None
        node_type = node[0]

        if node_type == "NUMBER": return 'integer'
        if node_type == "REAL_NUMBER": return 'real'
        if node_type == "STRING" or node_type == "STRING_LITERAL": return 'string'
        if node_type == "BOOLEAN": return 'boolean'
        
        if node_type == "UMINUS":
            return self.infer_expression_type(node[1])

        if node_type == "ID":
             try:
                 return self.lookup_identifier_type(node[1])
             except ValueError:
                 return None 

        if node_type in ["+", "-", "*", "mod"]:
            left_type = self.infer_expression_type(node[1])
            right_type = self.infer_expression_type(node[2])

            # ADD THIS BLOCK FOR STRING CONCATENATION:
            if node_type == '+' and left_type == 'string' and right_type == 'string':
                return 'string'

            # Existing logic for other types:
            if left_type == 'real' or right_type == 'real':
                # Ensure compatible types for real operations (e.g., int + real is valid)
                if (left_type == 'real' and (right_type == 'real' or right_type == 'integer')) or \
                   (right_type == 'real' and (left_type == 'real' or left_type == 'integer')):
                    return 'real'
            if left_type == 'integer' and right_type == 'integer':
                return 'integer'
            # Char arithmetic (e.g., char + int -> int, char - char -> int)
            if node_type in ['+', '-'] and \
               ((left_type == 'char' and right_type == 'integer') or \
                (left_type == 'integer' and right_type == 'char') or \
                (left_type == 'char' and right_type == 'char')):
                return 'integer'

            return None  

        if node_type == "div": return 'integer'
        if node_type == "/": return 'real'   

        if node_type in ["=", "<>", "<", ">", "<=", ">=", "and", "or", "not"]: return 'boolean'

        if node_type == "FUNCTION_CALL":
            func_name = node[1]
            func_name_lower = func_name.lower()
            try:
                signature = self.get_function_signature(func_name_lower)
                return signature['return_type']
            except ValueError:
                print(f"WARNING: Type inference failed for function call '{func_name}'. Function may not be declared or supported for type inference.", file=sys.stderr)
                return None


        if node_type == "ARRAY_ACCESS":
            array_name_ID_node = node[1]
            if not (isinstance(array_name_ID_node, (list,tuple)) and array_name_ID_node[0] == 'ID'):
                return None 

            array_name = array_name_ID_node[1]
            try:
                base_type_info = self.lookup_identifier_type(array_name)
                if base_type_info == 'string':
                    return 'char' 
                elif base_type_info and base_type_info.startswith('array of '):
                    return base_type_info.split(' of ')[1] 
                else: 
                    return None
            except ValueError: 
                return None
        return None

def evaluate_constant_integer_expression(node):
    if isinstance(node, (list, tuple)):
        if node[0] == "NUMBER" and isinstance(node[1], int):
            return node[1]
        elif node[0] == "UMINUS" and \
             isinstance(node[1], (list, tuple)) and \
             node[1][0] == "NUMBER" and isinstance(node[1][1], int):
            return -node[1][1]
    return None

def process_var_declarations_node(node, symbol_table):
    """
    processa um nó de VAR_DECLARATIONS e popula a tabela de símbolos.
    """
    if not (isinstance(node, (list, tuple)) and len(node) == 2 and node[0] == "VAR_DECLARATIONS"):
        return

    var_items_list = node[1]
    if not var_items_list: 
        return

    for var_item in var_items_list:
        if not (isinstance(var_item, (list, tuple)) and len(var_item) == 3 and var_item[0] == "VAR_ITEM"):
            raise ValueError(f"invalid VAR_ITEM structure: {var_item}")
            
        ID_list_names = var_item[1]
        type_node = var_item[2]

        if not isinstance(ID_list_names, list) or not all(isinstance(name, str) for name in ID_list_names):
            raise ValueError(f"invalid ID_list in VAR_ITEM: {ID_list_names}")

        if isinstance(type_node, (list, tuple)) and type_node[0] == "ARRAY_TYPE":
            if not (len(type_node) == 4): 
                raise ValueError(f"invalid ARRAY_TYPE structure: {type_node}")

            start_expr_node = type_node[1]
            end_expr_node = type_node[2]
            element_type_node = type_node[3]

            start_index_val = evaluate_constant_integer_expression(start_expr_node)
            end_index_val = evaluate_constant_integer_expression(end_expr_node)
            
            if start_index_val is None or end_index_val is None:
                raise ValueError("array limits must be evaluable to integer constants for static declaration.")
            
            start_index = start_index_val
            end_index = end_index_val

            if not (isinstance(element_type_node, (list, tuple)) and element_type_node[0] == "TYPE" and len(element_type_node) == 2):
                 raise ValueError(f"invalid element type node for array: {element_type_node}")
            element_type_str = element_type_node[1].lower()

            if element_type_str not in symbol_table.valid_types:
                 raise ValueError(f"unknown array element type: '{element_type_str}'.")

            for arr_name in ID_list_names:
                 symbol_table.add_array(arr_name, start_index, end_index, element_type_str)

        elif isinstance(type_node, (list, tuple)) and type_node[0] == "TYPE":
            if not (len(type_node) == 2): 
                raise ValueError(f"invalid TYPE structure: {type_node}")
            var_type_str = type_node[1].lower()
            if var_type_str not in symbol_table.valid_types:
                 raise ValueError(f"unknown variable type '{var_type_str}'.")
            for var_name in ID_list_names:
                 symbol_table.add_symbol(var_name, var_type_str)
        else:
             raise ValueError(f"invalid type declaration format: {type_node}")

def semantics(tree_root):
    """cria e popula uma SymbolTable a partir da raiz da AST (nó PROGRAM)."""
    symbol_table = SymbolTable() # cria uma nova tabela de símbolos

    # verifica a estrutura do nó raiz da AST (PROGRAM)
    if not tree_root or not isinstance(tree_root, (list, tuple)) or tree_root[0] != "PROGRAM" or len(tree_root) < 3:
        raise ValueError("estrutura de PROGRAM inválida ou ausente para construir a tabela de símbolos.")

    program_body_node = tree_root[2]

    # verifica a estrutura de PROGRAM_BODY
    if not isinstance(program_body_node, (list, tuple)) or \
       program_body_node[0] != "PROGRAM_BODY" or len(program_body_node) < 2:
        raise ValueError("estrutura de PROGRAM_BODY inválida para construir a tabela de símbolos.")

    declarations_node = program_body_node[1]

    # processa o nó de DECLARATIONS se existir
    if declarations_node and isinstance(declarations_node, (list, tuple)) and \
       declarations_node[0] == "DECLARATIONS" and len(declarations_node) > 1 and declarations_node[1]:
        
        for decl_group in declarations_node[1]: # itera sobre a lista de grupos de declaração
            if decl_group and isinstance(decl_group, (list, tuple)) and len(decl_group) > 0:
                if decl_group[0] == "VAR_DECLARATIONS":
                    process_var_declarations_node(decl_group, symbol_table)
    
    return symbol_table

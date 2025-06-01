import ply.yacc as yacc
import sys
import json
import os

from analex import tokens,lexer

# --- representação dos nodos da árvore ---
# através de tuplos --> (tipo,nó-filho1,nõ-filho2,...)
# para as folhas da árvr. (nums,IDs),utiliza-se um tuplo (nome,valor)

# ordens de precedência (já definidas, verificar se algo novo afeta)
# A adição de REAL_NUMBER não deve afetar a precedência diretamente,
# mas as operações com 'real' terão suas próprias regras de tipo no tradutor.

# --- regras da gramática ---

def p_program(p):
    '''program : PROGRAM ID SEMI program_body DOT'''
    p[0] = ('PROGRAM',p[2],p[4])

def p_program_body(p):
    '''program_body : declaration_part block'''
    p[0] = ('PROGRAM_BODY',p[1],p[2])

def p_declaration_part(p):
    '''declaration_part : var_declaration
                         | function_declaration_list
                         | var_declaration function_declaration_list
                         | function_declaration_list var_declaration
                         | empty'''
    declarations = []
    if len(p) == 2: 
        if p[1] is not None:
            declarations.extend(p[1]) if isinstance(p[1],list) else declarations.append(p[1])
    elif len(p) == 3: 
        if p[1] is not None:
            declarations.extend(p[1]) if isinstance(p[1],list) else declarations.append(p[1])
        if p[2] is not None:
            declarations.extend(p[2]) if isinstance(p[2],list) else declarations.append(p[2])
    p[0] = ('DECLARATIONS',declarations) if declarations else None


def p_function_declaration_list(p):
    '''function_declaration_list : function_declaration_list function_declaration
                                 | function_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN parameter_list RPAREN COLON type SEMI function_body SEMI'''
    p[0] = ('FUNCTION',p[2],p[4],p[7],p[9])

def p_function_body(p):
    '''function_body : var_declaration BEGIN statement_list END'''
    p[0] = ('FUNCTION_BODY',p[1],p[3])

def p_parameter_list(p):
    '''parameter_list : parameter_list SEMI parameter
                      | parameter
                      | empty'''
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    elif len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]


def p_parameter(p):
    '''parameter : id_list COLON type'''
    p[0] = ('PARAMETER',p[1],p[3])

def p_block(p):
    '''block : BEGIN statement_list END'''
    p[0] = ('BLOCK',p[2])

def p_var_declaration(p):
    '''var_declaration : VAR var_list SEMI
                       | empty'''
    if len(p) == 4:
        p[0] = ('VAR_DECLARATIONS',p[2])
    else:
        p[0] = None

def p_var_list(p):
    '''var_list : var_list SEMI var_item
                | var_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_var_item(p):
    '''var_item : id_list COLON type'''
    p[0] = ('VAR_ITEM',p[1],p[3])

def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_type(p):
    '''type : INTEGER
            | STRTYPE
            | BOOLEAN
            | CHAR
            | REAL
            | array_type'''
    if isinstance(p[1], tuple): 
        p[0] = p[1]
    else:
        p[0] = ('TYPE', p.slice[1].value)


def p_array_type(p):
    '''array_type : ARRAY LBRACKET expression RANGEDOTS expression RBRACKET OF type'''
    p[0] = ('ARRAY_TYPE',p[3],p[5],p[8])

def p_statement_list(p):
    '''statement_list : statement_list SEMI statement
                      | statement
                      | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 4:
        if p[3] is not None:
            p[1].append(p[3])
        p[0] = p[1]


def p_statement(p):
    '''statement : assignment_statement
                 | writeln_statement
                 | write_statement
                 | readln_statement
                 | read_statement
                 | for_statement
                 | while_statement
                 | compound_statement
                 | if_statement
                 | function_call_statement
                 | empty '''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression
                            | array_access ASSIGN expression'''
    if isinstance(p[1],tuple) and p[1][0] == 'ARRAY_ACCESS':
        p[0] = ('ARRAY_ASSIGN',p[1],p[3])
    else:
        p[0] = ('ASSIGN',('ID',p[1]),p[3])

def p_writeln_statement(p):
    '''writeln_statement : WRITELN LPAREN write_args RPAREN
                         | WRITELN'''
    if len(p) == 2:
        p[0] = ('WRITELN', [])
    else:
        p[0] = ('WRITELN',p[3])

def p_write_statement(p):
    '''write_statement : WRITE LPAREN write_args RPAREN'''
    p[0] = ('WRITE',p[3])


def p_readln_statement(p):
    '''readln_statement : READLN LPAREN read_args RPAREN
                        | READLN'''
    if len(p) == 2:
        p[0] = ('READLN', [])
    else:
        p[0] = ('READLN',p[3])


def p_read_statement(p):
    '''read_statement : READ LPAREN read_args RPAREN'''
    p[0] = ('READ',p[3])

def p_read_args(p):
    '''read_args : read_args COMMA read_arg
                 | read_arg'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_read_arg(p):
    '''read_arg : ID
                | array_access'''
    if isinstance(p[1], tuple) and p[1][0] == 'ARRAY_ACCESS':
        p[0] = p[1]
    else:
        p[0] = ('ID', p[1])


def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    if len(p) == 5:
        p[0] = ('IF',p[2],p[4],None)
    else:
        p[0] = ('IF',p[2],p[4],p[6])

def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    p[0] = ('WHILE',p[2],p[4])

def p_write_args(p):
    '''write_args : write_args COMMA write_arg
                  | write_arg'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_write_arg(p):
    '''write_arg : expression'''
    p[0] = p[1]


def p_for_statement(p):
    '''for_statement : FOR ID ASSIGN expression direction expression DO statement'''
    p[0] = ('FOR',('ID',p[2]),p[4],p[5],p[6],p[8])

def p_direction(p):
    '''direction : TO
                 | DOWNTO'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : BEGIN statement_list END'''
    p[0] = ('COMPOUND',p[2])

def p_expression(p):
    '''expression : or_expression'''
    p[0] = p[1]

def p_or_expression(p):
    '''or_expression : or_expression OR and_expression
                     | and_expression'''
    if len(p) == 4:
        p[0] = ('or', p[1], p[3])
    else:
        p[0] = p[1]

def p_and_expression(p):
    '''and_expression : and_expression AND not_expression
                      | not_expression'''
    if len(p) == 4:
        p[0] = ('and', p[1], p[3])
    else:
        p[0] = p[1]

def p_not_expression(p):
    '''not_expression : NOT comparison_expression
                      | comparison_expression'''
    if len(p) == 3:
        p[0] = ('not', p[2])
    else:
        p[0] = p[1]

def p_comparison_expression(p):
    '''comparison_expression : comparison_expression EQ additive_expression
                             | comparison_expression NE additive_expression
                             | comparison_expression LT additive_expression
                             | comparison_expression LE additive_expression
                             | comparison_expression GT additive_expression
                             | comparison_expression GE additive_expression
                             | additive_expression''' 
    if len(p) == 4: 
        p[0] = (p.slice[2].value, p[1], p[3])
    else: 
        p[0] = p[1]


def p_additive_expression(p):
    '''additive_expression : additive_expression PLUS multiplicative_expression
                           | additive_expression MINUS multiplicative_expression
                           | multiplicative_expression'''
    if len(p) == 4:
        p[0] = (p.slice[2].value, p[1], p[3])
    else:
        p[0] = p[1]

def p_multiplicative_expression(p):
    '''multiplicative_expression : multiplicative_expression TIMES unary_minus_factor
                                 | multiplicative_expression DIVIDE unary_minus_factor
                                 | multiplicative_expression MOD unary_minus_factor
                                 | multiplicative_expression DIV unary_minus_factor
                                 | unary_minus_factor'''
    if len(p) == 4:
        p[0] = (p.slice[2].value, p[1], p[3])
    else:
        p[0] = p[1]

def p_unary_minus_factor(p):
    '''unary_minus_factor : MINUS factor
                          | factor'''
    if len(p) == 3:
        p[0] = ('UMINUS', p[2])
    else:
        p[0] = p[1]

def p_factor_number_or_real(p):
    '''factor : NUMBER
              | REAL_NUMBER'''
    if p.slice[1].type == 'NUMBER':
        p[0] = ('NUMBER', p[1])
    elif p.slice[1].type == 'REAL_NUMBER':
        p[0] = ('REAL_NUMBER', p[1])


def p_factor_id(p):
    '''factor : ID'''
    p[0] = ('ID', p[1])

def p_factor_boolean(p):
    '''factor : TRUE
              | FALSE'''
    p[0] = ('BOOLEAN', p.slice[1].value)

def p_factor_string_literal(p):
    '''factor : STRING''' # STRING token is for 'a string literal'
    p[0] = ('STRING_LITERAL', p[1])

def p_factor_group(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_factor_function_call(p):
    '''factor : ID LPAREN call_arguments RPAREN'''
    p[0] = ('FUNCTION_CALL', p[1], p[3])

def p_factor_array_access(p):
    '''factor : array_access'''
    p[0] = p[1]

def p_function_call_statement(p):
    '''function_call_statement : ID LPAREN call_arguments RPAREN'''
    p[0] = ('FUNCTION_CALL_STATEMENT',p[1],p[3])

def p_call_arguments(p):
    '''call_arguments : call_arguments COMMA expression
                      | expression
                      | empty'''
    if len(p) == 2:
        if p[1] is None: # empty
            p[0] = []
        else: # expression
            p[0] = [p[1]]
    elif len(p) == 4: # call_arguments COMMA expression
        p[1].append(p[3])
        p[0] = p[1]

def p_array_access(p):
    '''array_access : ID LBRACKET expression RBRACKET'''
    p[0] = ('ARRAY_ACCESS',('ID',p[1]),p[3])


def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        line = p.lineno
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        col = (p.lexpos - line_start) + 1
        error_message = (
            f"[SYNTAX ERROR]: line {line}, column {col}: "
            f"unexpected token '{p.value}' (type: {p.type})"
        )
        print(error_message, file=sys.stderr)
    else:
        print("[SYNTAX ERROR]: unexpected EOF.", file=sys.stderr)

    raise SyntaxError("PARSING FAILED!")

parser = yacc.yacc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}-ast.json"

        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read()
            print(f"--- parsing {input_file} ---")
            lexer.lineno = 1
            tree = parser.parse(data, lexer=lexer)

            if tree:
                print(f"\n--- writing AST to {output_file} ---")
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    json.dump(tree, outfile, indent=2, ensure_ascii=False)
                print("--- AST written ---")
                

            print("\n--- PROCESSING COMPLETE! ---")

        except FileNotFoundError:
            print(f"(ERROR): file '{input_file}' not found.")
        except SyntaxError as e:
            print(f"\n--- PARSING FAILED! ({e}) ---")
        except Exception as e:
            print(f"[ERROR]: an unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("[USAGE]: python anasin.py <INPUT_FILE>")
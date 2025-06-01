import ply.lex as lex
import argparse
import re

tokens = (
    'ID',
    'NUMBER',
    'REAL_NUMBER',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    'LPAREN',
    'RPAREN',
    'SEMI',
    'COLON',
    'COMMA',
    'DOT',
    'RANGEDOTS',
    'LBRACKET',
    'RBRACKET',
    'COMMENT',
    # palavras reservadas
    'PROGRAM', 'BEGIN', 'END', 'WRITELN', 'READLN', 'VAR', 'INTEGER',
    'STRTYPE', 'FUNCTION', 'PROCEDURE', 'IF', 'THEN', 'ELSE', 'WHILE',
    'DO', 'FOR', 'TO', 'DOWNTO', 'ARRAY', 'OF', 'BOOLEAN', 'TRUE',
    'FALSE', 'MOD', 'DIV', 'NOT', 'AND', 'OR',
    'CHAR', 'REAL', 'WRITE', 'READ'
)

def t_REAL_NUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_PROGRAM(t):
    r'\bprogram\b'
    return t

def t_BEGIN(t):
    r'\bbegin\b'
    return t

def t_END(t):
    r'\bend\b'
    return t

def t_WRITELN(t):
    r'\bwriteln\b'
    return t

def t_WRITE(t):
    r'\bwrite\b'
    return t

def t_READLN(t):
    r'\breadln\b'
    return t

def t_READ(t):
    r'\bread\b'
    return t

def t_VAR(t):
    r'\bvar\b'
    return t

def t_INTEGER(t):
    r'\binteger\b'
    return t

def t_REAL(t):
    r'\breal\b'
    return t

def t_CHAR(t):
    r'\bchar\b'
    return t

def t_STRTYPE(t):
    r'\bstring\b' # 'string' keyword (for type declaration) maps to STRTYPE token
    return t

def t_FUNCTION(t):
    r'\bfunction\b'
    return t

def t_PROCEDURE(t):
    r'\bprocedure\b'
    return t

def t_IF(t):
    r'\bif\b'
    return t

def t_THEN(t):
    r'\bthen\b'
    return t

def t_ELSE(t):
    r'\belse\b'
    return t

def t_WHILE(t):
    r'\bwhile\b'
    return t

def t_DOWNTO(t):
    r'\bdownto\b'
    return t

def t_DO(t):
    r'\bdo\b'
    return t

def t_FOR(t):
    r'\bfor\b'
    return t

def t_TO(t):
    r'\bto\b'
    return t

def t_ARRAY(t):
    r'\barray\b'
    return t

def t_OF(t):
    r'\bof\b'
    return t

def t_BOOLEAN(t):
    r'\bboolean\b'
    return t

def t_TRUE(t):
    r'\btrue\b'
    return t

def t_FALSE(t):
    r'\bfalse\b'
    return t

def t_MOD(t):
    r'\bmod\b'
    return t

def t_DIV(t): # Integer division keyword
    r'\bdiv\b'
    return t

def t_NOT(t):
    r'\bnot\b'
    return t

def t_AND(t):
    r'\band\b'
    return t

def t_OR(t):
    r'\bor\b'
    return t

def t_COMMENT(t):
    r'\{[^}]*\}|\(\*([^*]|\*+[^*)])*\*+\)'
    pass  # ignorar comentários

def t_STRING(t):
    r"'(?:[^']|'')*'"
    t.value = t.value[1:-1].replace("''", "'")
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_ASSIGN  = r':='
t_EQ      = r'='
t_NE      = r'<>|!='
t_LT      = r'<'
t_LE      = r'<='
t_GT      = r'>'
t_GE      = r'>='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI    = r';'
t_COLON   = r':'
t_COMMA   = r','
t_RANGEDOTS = r'\.\.'
t_DOT     = r'\.'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print(f"[ERROR]: illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)


lexer = lex.lex(reflags=re.IGNORECASE)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='PASCAL LEXER')
    arg_parser.add_argument('input_file', help='path to the Pascal input file.')
    args = arg_parser.parse_args()
    path = args.input_file

    try:
        with open(path, 'r') as f:
            data = f.read()
        print(f"--- tokenizing {path} ---")
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
        print("--- COMPLETE! ---")
    except FileNotFoundError:
        print(f"(ERROR): file '{path}' not found.")
    except Exception as e:
        print(f"[ERROR]: an unexpected error occurred. {e}")


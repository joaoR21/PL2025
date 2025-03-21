import ply.lex as lex

tokens = (
    'NUM',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EXPONENT = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter desconhecido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)
    
lexer = lex.lex()
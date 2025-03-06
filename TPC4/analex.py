import ply.lex as lex

# palavras reservadas
reserved = {
    'select': 'SELECT',
    'where': 'WHERE',
    'LIMIT': 'LIMIT',
    'a': 'A'
}

tokens = ['VAR', 'STRING', 'TAG', 'NUMBER', 'DOT', 'COLON', 'LCURLY', 'RCURLY', 'DBO', 'FOAF', 'ID'] + list(reserved.values())

t_DOT = r'\.'
t_COLON = r':'
t_LCURLY = r'\{'
t_RCURLY = r'\}'

def t_DBO(t):
    r'dbo:[a-zA-Z_]+'
    t.value = t.value[4:]
    return t

def t_FOAF(t):
    r'foaf:[a-zA-Z_]+'
    t.value = t.value[5:]
    return t

def t_VAR(t):
    r'\?[a-zA-Z_]+'
    return t

def t_STRING(t):
    r'".+"'
    return t

def t_TAG(t):
    r'@[a-zA-Z]+'
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # verificar palavras reservadas
    return t

# caracteres a ignorar
t_ignore = ' \t\n'

def t_error(t):
    print(f"illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def main():
    data = '''select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000'''

    lexer.input(data)
    for tok in lexer:
        print(tok)

if __name__ == '__main__':
    main()
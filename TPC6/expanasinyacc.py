import ply.yacc as yacc
from expanalex import tokens

def p_exp(p):
    """exp : term"""
    print("A aplicar regra P3 : Exp -> Termo")
    p[0] = p[1]

def p_exp_plus(p):
    """exp : term PLUS exp"""
    print("A aplicar regra P1 : Exp -> Termo '+' Exp")
    p[0] = p[1] + p[3]

def p_exp_minus(p):
    """exp : term MINUS exp"""
    print("A aplicar regra P2 : Exp -> Termo '-' Exp")
    p[0] = p[1] - p[3]

def p_term_factor(p):
    """term : factor"""
    print("A aplicar regra P6: Termo -> Factor")
    p[0] = p[1]

def p_term_times(p):
    """term : factor TIMES term"""
    print("A aplicar regra P4 : Termo -> Factor '*' Termo")
    p[0] = p[1] * p[3]

def p_term_divide(p):
    """term : factor DIVIDE term"""
    print("A aplicar regra P5 : Termo -> Factor '/' Termo")
    p[0] = p[1] / p[3]

def p_factor_num(p):
    """factor : NUM"""
    print("A aplicar regra P8 : Factor -> num")
    p[0] = p[1]

def p_factor_paren(p):
    """factor : LPAREN exp RPAREN"""
    print("A aplicar regra P7 : Factor -> '(' Exp ')' ")
    p[0] = p[2]

parser = yacc.yacc()

def parse_input(data):
    return parser.parse(data)

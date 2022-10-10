# Author: Daniel E. Rodriguez Olivera
# Date: Octubre 10, 2022

#Imports
import ply.lex as lex
import ply.yacc as yacc

#######################Scanner###########################
#reserved tokens/(taken)words for the ID token
reserved = { 'def' : 'DEF', 'var' : 'VAR', 'Int' : 'INT', 'if' : 'IF','else' : 'ELSE'}

# List of Tokens
tokens = ('ID', 'DEF', 'VAR', 'INT', 'IF', 'ELSE', 'NUM', 'LPAREN', 'RPAREN',
            'LBRACE', 'RBRACE', 'EQ', 'BECOMES', 'NE', 'LT', 'GT','LE',
            'GE', 'PLUS', 'MINUS', 'STAR', 'SLASH', 'PCT', 'COMMA', 'SEMI',
            'COLON', 'ARROW', 'COMMENT', 'WHITESPACE')

# Regular Expression rules for tokens

def t_ID(t): # RE for a string consisting of a letter (in the range a-z or A-Z) followed by zero or more letters and digits (in the range 0-9), but not equal to any of the keywords def, var, Int, if, else.
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_DEF = r'def' # RE for the string (keyword) def
t_VAR = r'var' # RE for the the string (keyword) var
t_INT = r'Int' # RE for the string (keyword) Int
t_IF = r'if' # RE for the the string (keyword) if
t_ELSE = r'else' # RE for the the string (keyword) else

def t_NUM(t): # RE for a string of one or more digits
    r'[0-9]+'
    t.value = int(t.value)
    return t
    
t_LPAREN = r'\(' # RE for the string (
t_RPAREN = r'\)' # RE for the string )
t_LBRACE = r'\{' # RE for the string {
t_RBRACE = r'\}' # RE for the string }
t_EQ = r'==' # RE for the string ==
t_BECOMES = r'=' # RE for the string =
t_NE = r'\!=' # RE for the string !=
t_LT = r'\<' # RE for the string <
t_GT = r'\>' # RE for the string >
t_LE = r'\<=' # RE for the string <=
t_GE = r'\>=' # RE for the string >=
t_PLUS = r'\+' # RE for the string +
t_MINUS = r'-' # RE for the string -
t_STAR = r'\*' # RE for the string *
t_SLASH = r'/' # RE for the string /
t_PCT = r'\%' # RE for the string %
t_COMMA = r',' # RE for the string ,
t_SEMI = r';' # RE for the string ;
t_COLON = r'\:' # RE for the string :
t_ARROW = r'=\>' # RE for the string =>
t_ignore_COMMENT = r'\#.*' # RE for the string // followed by any characters other than the newline character (ascii 10, \n )
t_ignore_WHITESPACE = r'[ \t]' # RE for one of the following characters: tab (ascii 9, \t ), newline (ascii 10, \n ), carriage return (ascii 13, \r ), space (ascii 32)

#######################Input###########################
#Change input to check against scanner and parser
#fist given input
#input = """ def f(a:Int, b:Int):Int = { var c:Int;
#def g(a:Int, b:(Int)=>Int):Int = { b(a)
#}
#def h(c:Int):Int = {
#def g():Int = { c-b
#}
#g() }
#c = a+b;
#g(c,h) }"""

#second given input
input = """ def f(a:Int, b:Int):Int = { var c:Int;
def g(a:Int, b:(Int)=>Int):Int = { b(a)
}
def h(c:Int):Int = {=>
def g():Int = { c-b
}
g() }
c = a+b;
g(c,h) } """
#######################Input###########################

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(input)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

#######################Scanner###########################

#######################Parser###########################
#Functions that apply the specified Context Free Grammar
def p_defdefs_defdefdefdefs(p):
    'defdefs : defdef defdefs'
    pass

def p_defdefs_defdef(p):
    'defdefs : defdef'
    pass

def p_defdef_def(p):
    'defdef : DEF ID LPAREN parmsopt RPAREN COLON type BECOMES LBRACE vardefsopt defdefsopt expras RBRACE'
    pass

def p_parmsopt_parms(p):
    'parmsopt : parms'
    pass

def p_parmsopt_(p):
    'parmsopt : '
    pass

def p_parms_vardefcommaparms(p):
    'parms : vardef COMMA parms'
    pass

def p_parms_vardef(p):
    'parms : vardef'
    pass

def p_vardef(p):
    'vardef : ID COLON type'
    pass

def p_type_INT(p):
    'type : INT'
    pass

def p_type_arrowtype(p):
    'type : LPAREN typesopt RPAREN ARROW type'
    pass

def p_typesopt_types(p):
    'typesopt : types'
    pass

def p_typesopt_(p):
    'typesopt : '
    pass

def p_types_typecommatypes(p):
    'types : type COMMA types'
    pass

def p_types_type(p):
    'types : type'
    pass

def p_vardefsopt_varvardefsemivardefsopt(p):
    'vardefsopt : VAR vardef SEMI vardefsopt'
    pass

def p_vardefsopt_(p):
    'vardefsopt : '
    pass

def p_defdefsopt_defdefs(p):
    'defdefsopt : defdefs'
    pass

def p_defdefsopt_(p):
    'defdefsopt : '
    pass

def p_expras_exprasemiexpras(p):
    'expras : expra SEMI expras'
    pass

def p_expras_expra(p):
    'expras : expra'
    pass

def p_expra_idbecomesexpr(p):
    'expra : ID BECOMES expr'
    pass

def p_expra_expr(p):
    'expra : expr'
    pass

def p_expr_if(p):
    'expr : IF LPAREN test RPAREN LBRACE expras RBRACE ELSE LBRACE expras RBRACE'
    pass

def p_expr_term(p):
    'expr : term'
    pass

def p_expr_plus(p):
    'expr : expr PLUS term'
    pass

def p_expr_minus(p):
    'expr : expr MINUS term'
    pass

def p_term_factor(p):
    'term : factor'
    pass

def p_term_star(p):
    'term : term STAR factor'
    pass

def p_term_slash(p):
    'term : term SLASH factor'
    pass

def p_term_pct(p):
    'term : term PCT factor'
    pass

def p_factor_id(p):
    'factor : ID'
    pass

def p_factor_num(p):
    'factor : NUM'
    pass

def p_factor_lparen(p):
    'factor : LPAREN expr RPAREN'
    pass

def p_factor_factor(p):
    'factor : factor LPAREN argsopt RPAREN'
    pass

def p_test_ne(p):
    'test : expr NE expr'
    pass

def p_test_lt(p):
    'test  : expr LT expr'
    pass

def p_test_le(p):
    'test  : expr LE expr'
    pass

def p_test_ge(p):
    'test  : expr GE expr'
    pass

def p_test_gt(p):
    'test  : expr GT expr'
    pass

def p_test_eq(p):
    'test  : expr EQ expr'
    pass

def p_argsopt_args(p):
    'argsopt : args'
    pass

def p_argsopt_(p):
    'argsopt : '
    pass

def p_args_exprcomma(p):
    'args : expr COMMA args'
    pass

def p_args_expr(p):
    'args : expr'
    pass

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

#Build parser
parser = yacc.yacc()

while True:
    try:
        s = input
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
    break

#######################Parser###########################
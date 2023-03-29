import sys
import ply.lex as lex

reserved = {
    'program': 'PROGRAM',
    'function': 'FUNCTION',
    'int': 'INT',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
}

tokens = [
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LSQBRACKET',
    'RSQBRACKET',
    'COMMA',
    'SEMICOLON',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LESS',
    'LESSEQUAL',
    'GREATER',
    'GREATEREQUAL',
    'EQUAL',
    'NOTEQUAL',
    'ID',
    'NUMBER',
    'LINECOMMENT',
    'BLOCKCOMMENT',
    'NEWLINE',
] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATER = r'>'
t_GREATEREQUAL = r'>='
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_LINECOMMENT = r'//[^\n]*'

def t_BLOCKCOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

t_ignore = ' \t'

def t_error(t):
    print(f"Caracter inválido: '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

args = sys.argv

fich = ""
if len(args) > 0:
    fich = args[1]
else:
    fich=input("Insira o nome do ficheiro a analisar")
    
f = open(fich, 'r')

lines = f.readlines()

text = ""

for line in lines:
    text += line


lexer.input(text)

while True:
    tok = lex.token()
    if not tok: 
        break      
    print(tok.type, tok.value, tok.lineno, tok.lexpos)

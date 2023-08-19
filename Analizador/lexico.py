import ply.lex as lex

# Lista de palabras reservadas
reserved = {
    'mkdisk': 'MKDISK',
    '-path': 'PATH',
    '-unit': 'UNIT',
    '-fit': 'FIT',
    '-size': 'SIZE',
    'execute': 'EXECUTE',
}

# Lista de tokens
tokens = [
    'ID',
    'RUTA',
    'IGUAL',
    'COMILLADOBLE',
    'NUMERO',
    #'PUNTO',
    #'DIAGONAL',
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_RUTA = r'\/[^\r\n\"]*'
t_NUMERO = r'\d+'
t_IGUAL = r'\='
#t_PUNTO = r'\.'
#t_DIAGONAL = r'\/'
t_COMILLADOBLE = r'\"'

# Función para manejar palabras reservadas
def t_ID(t):
    r'[a-zA-Z_-][a-zA-Z0-9_-]*'
    t.type = reserved.get(t.value, 'ID')
    return t
# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Función para manejar saltos de línea
#def t_newline(t):
#    r'\n+'
#    t.lexer.lineno += len(t.value)

# Función para manejar errores de token
def t_error(t):
    #print(f"Carácter inesperado: '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
# lexer = lex.lex()

# # Ejemplo de uso
# if __name__ == '__main__':
#     data = 'mkdisk -size=3000 -unit=K -path="/home/user/Disco1_hola123*.dsk"'
#     lexer.input(data)
#     while True:
#         token = lexer.token()
#         if not token:
#             break
#         print(token)

import ply.lex as lex

# Lista de palabras reservadas
reserved = {
    #COMANDOS    
    'execute': 'EXECUTE',
    'mkdisk': 'MKDISK',
    'rmdisk': 'RMDISK',
    'fdisk': 'FDISK',
    'mount': 'MOUNT',
    'unmount': 'UNMOUNT',
    'mkfs': 'MKFS',
    'login': 'LOGIN',
    'logout': 'LOGOUT',
    'mkgrp': 'MKGRP',  
    'rmgrp': 'RMGRP',
    'mkusr': 'MKUSR',
    'rmusr': 'RMUSR',
    'mkfile': 'MKFILE',
    'cat': 'CAT',
    'remove': 'REMOVE',
    'edit': 'EDIT',
    'rename': 'RENAME',
    'mkdir': 'MKDIR',
    'copy': 'COPY',
    'move': 'MOVE',
    'find': 'FIND',
    'chown': 'CHOWN',
    'chgrp': 'CHGRP',
    'chmod': 'CHMOD',
    'pause': 'PAUSE',
    'recovery': 'RECOVERY',
    'loss': 'LOSS',
    'rep': 'REP',
    #PARAMETROS
    '-path': 'PATH',
    '-unit': 'UNIT',
    '-fit': 'FIT',
    '-size': 'SIZE',
    '-name': 'NAME',
    '-type': 'TYPE',
    '-delete': 'DELETE',
    '-id': 'ID_CMD',
    '-add': 'ADD',
    '-fs': 'FS',
    '-user': 'USER',
    '-pass': 'PASS',
    '-grp': 'GRP',
    '-r': 'R',
    '-cont': 'CONT',
    '-destino': 'DEST',
    '-ugo': 'UGO',
    '-ruta': 'RUTAC',
}

# Lista de tokens
tokens = [
    'ID',
    'RUTA',
    'IGUAL',
    #'COMILLADOBLE',
    'NUMERO',
    'CADENA',
    'BUSCAR',
    #'NEGATIVO',
    #'MENOS',
    #'PUNTO',
    #'DIAGONAL',
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_RUTA = r'\/[^\.\r\n\" ]*'
t_NUMERO = r'\d+'
#t_NEGATIVO = r'\-\d+'
t_IGUAL = r'\='
t_CADENA = r'\"[^\r\n\"]*\"'
t_BUSCAR = r'[\?\*][\.]?[\?\*]?'

#t_MENOS = r'\-'
#t_PUNTO = r'\.'
#t_DIAGONAL = r'\/'
#t_COMILLADOBLE = r'\"'

# Función para manejar palabras reservadas
def t_ID(t):
    r'[a-zA-Z_-][a-zA-Z0-9_-]*'
    t.type = reserved.get(t.value.lower(), 'ID')
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

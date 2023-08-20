import ply.yacc as yacc
#from lexico import tokens

#================================ PRODUCCION INICIAL =================================
def p_command(p):
    '''command : mkdisk_command
               | execute_command
               | rmdisk_command
    '''
    p[0] = p[1]

# =============================== Reglas de producción para MKDISK ===============================
def p_mkdisk_command(p):
    '''mkdisk_command : MKDISK opciones'''
    #Se guarda el contenido
    p[0] = {
        'command': 'mkdisk',
        **p[2],
    }
    
def p_opciones(p):
    '''opciones : opciones opciones_element 
                | opciones_element'''
    #Se guarda el contenido
    if len(p) > 2:
        p[0] = {
            **p[1],
            **p[2]
        }
    else:
        p[0] = {
            **p[1]
        }
def p_opciones_element(p):
    '''opciones_element : opcion_size
                        | opcion_path
                        | opcion_unit
                        | opcion_fit'''
    p[0] = {
        **p[1]
    }

def p_opcion_size(p):
    '''opcion_size : SIZE IGUAL NUMERO'''
    #Se guarda el contenido
    p[0] = {
        'size': p[3]
    }

def p_opcion_path(p):
    '''opcion_path : PATH IGUAL RUTA
                   | PATH IGUAL COMILLADOBLE RUTA COMILLADOBLE'''
    #Se guarda el contenido
    if len(p) > 5:
        p[0] = {
            'path': p[4]
        }
    else:
        p[0] = {
            'path': p[3]
        }

def p_opcion_unit(p):
    '''opcion_unit : UNIT IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'unit': p[3]
    }

def p_opcion_fit(p):
    '''opcion_fit : FIT IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'fit': p[3]
    }
    
# =============================== FIN MKDISK ===============================

# =============================== Reglas de producción para EXECUTE ===============================
def p_execute_command(p):
    '''execute_command : EXECUTE PATH IGUAL RUTA
                       | EXECUTE PATH IGUAL COMILLADOBLE RUTA COMILLADOBLE'''
    #Se guarda el contenido
    if len(p) > 5:
        p[0] = {
            'command': 'execute',
            'path': p[5]
        }
    else:
        p[0] = {
            'command': 'execute',
            'path': p[4]
        }
    
# =============================== FIN EXECUTE ===============================

#============================== Reglas de producción para RMDISK ===============================
def p_rmdisk_command(p):
    '''rmdisk_command : RMDISK PATH IGUAL RUTA
                      | RMDISK PATH IGUAL COMILLADOBLE RUTA COMILLADOBLE'''
                    
    #Se guarda el contenido
    if len(p) > 5:
        p[0] = {
            'command': 'rmdisk',
            'path': p[5]
        }
    else:
        p[0] = {
            'command': 'rmdisk',
            'path': p[4]
        }
#============================== FIN RMDISK ===============================


def p_error(p):
    print("Syntax error in input!")

# Construir el parser
# parser = yacc.yacc()

# # Ejemplo de uso
# if __name__ == '__main__':
#     input_string = 'mkdisk -size=5 -unit=M -path="/home/mis discos/Disco3.dsk"'
#     result = parser.parse(input_string)
#     print("Resultado:", result)

import ply.yacc as yacc
#from lexico import tokens

#================================ PRODUCCION INICIAL =================================
def p_command(p):
    '''command : mkdisk_command
               | execute_command
               | rmdisk_command
               | fdisk_command'''
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
    '''opcion_path : PATH IGUAL RUTA DSK
                   | PATH IGUAL COMILLADOBLE RUTA DSK COMILLADOBLE'''
    #Se guarda el contenido
    if len(p) > 5:
        p[0] = {
            'path': p[4] + '.' + p[5]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
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
    '''execute_command : EXECUTE PATH IGUAL RUTA ADJ
                       | EXECUTE PATH IGUAL COMILLADOBLE RUTA ADJ COMILLADOBLE'''
    #Se guarda el contenido
    if len(p) > 6:
        p[0] = {
            'command': 'execute',
            'path': p[5] + '.' +p[6]
        }
    else:
        p[0] = {
            'command': 'execute',
            'path': p[4] + '.' + p[5]
        }
    
# =============================== FIN EXECUTE ===============================

#============================== Reglas de producción para RMDISK ===============================
def p_rmdisk_command(p):
    '''rmdisk_command : RMDISK PATH IGUAL RUTA DSK
                      | RMDISK PATH IGUAL COMILLADOBLE RUTA DSK COMILLADOBLE'''
                    
    #Se guarda el contenido
    if len(p) > 6:
        p[0] = {
            'command': 'rmdisk',
            'path': p[5] + '.' + p[6]
        }
    else:
        p[0] = {
            'command': 'rmdisk',
            'path': p[4] + '.' + p[5]
        }
#============================== FIN RMDISK ===============================

#============================== Reglas de producción para FDISK ===============================
def p_fdisk_command(p):
    '''fdisk_command : FDISK opciones_fdisk'''
    #Se guarda el contenido
    p[0] = {
        'command': 'fdisk',
        **p[2],
    }
def p_opciones_fdisk(p):
    '''opciones_fdisk : opciones_fdisk opciones_element_fdisk 
                      | opciones_element_fdisk'''
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
def p_opciones_element_fdisk(p):
    '''opciones_element_fdisk : opcionfdisk_size
                              | opcionfdisk_path
                              | opcionfdisk_name
                              | opcionfdisk_unit
                              | opcionfdisk_type
                              | opcionfdisk_fit
                              | opcionfdisk_delete
                              | opcionfdisk_add'''
    p[0] = {
        **p[1]
    }
def p_opcionfdisk_size(p):
    '''opcionfdisk_size : SIZE IGUAL NUMERO'''
    #Se guarda el contenido
    p[0] = {
        'size': p[3]
    }
def p_opcionfdisk_path(p):
    '''opcionfdisk_path : PATH IGUAL RUTA DSK
                        | PATH IGUAL COMILLADOBLE RUTA DSK COMILLADOBLE'''
    #Se guarda el contenido
    if len(p) > 5:
        p[0] = {
            'path': p[4] + '.' + p[5]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionfdisk_name(p):
    '''opcionfdisk_name : NAME IGUAL ID
                        | NAME IGUAL COMILLADOBLE ID COMILLADOBLE'''
    #Se guarda el contenido
    if len(p) > 4:
        p[0] = {
            'name': p[4]
        }
    else:
        p[0] = {
            'name': p[3]
        }
def p_opcionfdisk_unit(p):
    '''opcionfdisk_unit : UNIT IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'unit': p[3]
    }
def p_opcionfdisk_type(p):
    '''opcionfdisk_type : TYPE IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'type': p[3]
    }
def p_opcionfdisk_fit(p):
    '''opcionfdisk_fit : FIT IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'fit': p[3]
    }
def p_opcionfdisk_delete(p):
    '''opcionfdisk_delete : DELETE IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'delete': p[3]
    }
def p_opcionfdisk_add(p):
    '''opcionfdisk_add : ADD IGUAL NUMERO
                       | ADD IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'add': p[3]
    }
def p_error(p):
    print("Syntax error in input!",p)

# Construir el parser
# parser = yacc.yacc()

# # Ejemplo de uso
# if __name__ == '__main__':
#     input_string = 'mkdisk -size=5 -unit=M -path="/home/mis discos/Disco3.dsk"'
#     result = parser.parse(input_string)
#     print("Resultado:", result)

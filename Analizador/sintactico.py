import ply.yacc as yacc
#from lexico import tokens

#================================ PRODUCCION INICIAL =================================
def p_command(p):
    '''command : mkdisk_command
               | execute_command
               | rmdisk_command
               | fdisk_command
               | mount_command
               | unmount_command
               | mkfs_command
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
#============================== FIN FDISK =====================================================================
#==============================COMANDO MOUNT===================================================================
def p_mount_command(p):
    '''mount_command : MOUNT opciones_mount'''
    p[0] = {
        'command': 'mount',
        **p[2],
    }
def p_opciones_mount(p):
    '''opciones_mount : opciones_mount opciones_element_mount 
                      | opciones_element_mount'''
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
def p_opciones_element_mount(p):
    '''opciones_element_mount : opcionmount_path
                              | opcionmount_name'''
    p[0] = {
        **p[1]
    }
def p_opcionmount_path(p):
    '''opcionmount_path : PATH IGUAL RUTA DSK
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
def p_opcionmount_name(p):
    '''opcionmount_name : NAME IGUAL ID
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
    
#====================FIN COMANDO MOUNT===================================================================
#====================COMANDO UNMOUNT======================================================================
def p_unmount_command(p):
    '''unmount_command : UNMOUNT ID_CMD IGUAL NUMERO ID'''
    p[0] = {
        'command': 'unmount',
        'id':p[4] + p[5],
    }
#====================FIN COMANDO UNMOUNT===================================================================
#=====================COMANDO MKFS=========================================================================
def p_mkfs_command(p):
    '''mkfs_command : MKFS opciones_mkfs'''
    p[0] = {
        'command': 'mkfs',
        **p[2],
    }
def p_opciones_mkfs(p):
    '''opciones_mkfs : opciones_mkfs opciones_element_mkfs 
                      | opciones_element_mkfs'''
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
def p_opciones_element_mkfs(p):
    '''opciones_element_mkfs : opcionmkfs_id
                              | opcionmkfs_type
                              | opcionmkfs_fs'''
    p[0] = {
        **p[1]
    }
def p_opcionmkfs_id(p):
    '''opcionmkfs_id : ID_CMD IGUAL NUMERO ID'''
    #Se guarda el contenido
    p[0] = {
        'id': p[3] + p[4]
    }
def p_opcionmkfs_type(p):
    '''opcionmkfs_type : TYPE IGUAL ID'''
    #Se guarda el contenido
    p[0] = {
        'type': p[3]
    }
def p_opcionmkfs_fs(p):
    '''opcionmkfs_fs : FS IGUAL NUMERO ID'''
    #Se guarda el contenido
    p[0] = {
        'fs': p[3] + p[4]
    }
    
def p_error(p):
    #print("\t josep-ubu@Leon-Ubuntu>>> Error al escribir el comando.",p)
    pass

# Construir el parser
# parser = yacc.yacc()

# # Ejemplo de uso
# if __name__ == '__main__':
#     input_string = 'mkdisk -size=5 -unit=M -path="/home/mis discos/Disco3.dsk"'
#     result = parser.parse(input_string)
#     print("Resultado:", result)

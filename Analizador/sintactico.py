import ply.yacc as yacc
#from lexico import tokens

#================================ PRODUCCION INICIAL =================================
def p_command(p):
    '''command : execute_command
               | mkdisk_command
               | rmdisk_command
               | fdisk_command
               | mount_command
               | unmount_command
               | mkfs_command
               | login_command
               | logout_command
               | mkgrp_command
               | rmgrp_command
               | mkusr_command
               | rmusr_command
               | mkfile_command
               | cat_command
               | rmfile_command
               | edit_command
               | rename_command
               | mkdir_command
               | copy_command
               | move_command
               | find_command
               | chown_command
               | chgrp_command
               | chmod_command
               | pause_command
               | recovery_command
               | loss_command
               | rep_command
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
    '''opcion_path : PATH IGUAL RUTA ID
                   | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        p[3] = p[3][1:len(p[3])-1]  
        p[0] = {
            'path': p[3]
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
    '''execute_command : EXECUTE PATH IGUAL RUTA ID
                       | EXECUTE PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 6:
        p[0] = {
            'command': 'execute',
            'path': p[4] + '.' +p[5]
        }
    else:
        p[4] = p[4][1:len(p[4])-1]
        p[0] = {
            'command': 'execute',
            'path': p[4]
        }
    
# =============================== FIN EXECUTE ===============================

#============================== Reglas de producción para RMDISK ===============================
def p_rmdisk_command(p):
    '''rmdisk_command : RMDISK PATH IGUAL RUTA ID
                      | RMDISK PATH IGUAL CADENA'''
                    
    #Se guarda el contenido
    if len(p) == 6:
        p[0] = {
            'command': 'rmdisk',
            'path': p[4] + '.' + p[5]
        }
    else:
        p[4] = p[4][1:len(p[4])-1]
        p[0] = {
            'command': 'rmdisk',
            'path': p[4]
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
    '''opcionfdisk_path : PATH IGUAL RUTA ID
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        p[3] = p[3][1:len(p[3])-1]  
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionfdisk_name(p):
    '''opcionfdisk_name : NAME IGUAL ID
                        | NAME IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1] 
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
    '''opcionmount_path : PATH IGUAL RUTA ID
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        p[3] = p[3][1:len(p[3])-1]  
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionmount_name(p):
    '''opcionmount_name : NAME IGUAL ID
                        | NAME IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1] 
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
    
#====================FIN COMANDO MKFS===================================================================
#======================COMANDO LOGIN====================================================================
def p_login_command(p):
    '''login_command : LOGIN opciones_login'''
    p[0] = {
        'command': 'login',
        **p[2],
    }
def p_opciones_login(p):
    '''opciones_login : opciones_login opciones_element_login 
                      | opciones_element_login'''
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
def p_opciones_element_login(p):
    '''opciones_element_login : opcionlogin_usr
                              | opcionlogin_pwd
                              | opcionlogin_id'''
    p[0] = {
        **p[1]
    }
def p_opcionlogin_usr(p):
    '''opcionlogin_usr : USER IGUAL ID
                        | USER IGUAL CADENA'''
    #Se guarda el contenido    
    if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1] 
    p[0] = {        
        'user': p[3]
    }
def p_opcionlogin_pwd(p):
    '''opcionlogin_pwd : PASS IGUAL ID
                        | PASS IGUAL NUMERO
                        | PASS IGUAL CADENA
                        | PASS IGUAL NUMERO ID'''
                        
    #Se guarda el contenido
    if(len(p) == 4):
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]            
        p[0] = {
            'pass': p[3]
        }
    elif(len(p) == 5):
        p[0] = {
            'pass': p[3] + p[4]
        }
def p_opcionlogin_id(p):
    '''opcionlogin_id : ID_CMD IGUAL NUMERO ID'''
    #Se guarda el contenido
    p[0] = {
        'id': p[3] + p[4]
    }
#====================FIN COMANDO LOGIN===================================================================
#=======================COMANDO LOGOUT===================================================================
def p_logout_command(p):
    '''logout_command : LOGOUT'''
    p[0] = {
        'command': 'logout',
    }
#====================FIN COMANDO LOGOUT===================================================================
#========================COMANDO MKGRP===================================================================
def p_mkgrp_command(p):
    '''mkgrp_command : MKGRP NAME IGUAL ID
                     | MKGRP NAME IGUAL CADENA'''
                     
    if(p[4][0] == '\"'):
        p[4] = p[4][1:len(p[4])-1]  
    p[0] = {
        'command': 'mkgrp',
        'name': p[4]
    }
#====================FIN COMANDO MKGRP===================================================================
#========================COMANDO RMGRP===================================================================
def p_rmgrp_command(p):
    '''rmgrp_command : RMGRP NAME IGUAL ID
                     | RMGRP NAME IGUAL CADENA'''
                     
    if(p[4][0] == '\"'):
        p[4] = p[4][1:len(p[4])-1]  
    p[0] = {
        'command': 'rmgrp',
        'name': p[4]
    }
#====================FIN COMANDO RMGRP===================================================================
#========================COMANDO MKUSR===================================================================
def p_mkusr_command(p):
    '''mkusr_command : MKUSR opciones_mkusr'''
    p[0] = {
        'command': 'mkusr',
        **p[2],
    }
def p_opciones_mkusr(p):
    '''opciones_mkusr : opciones_mkusr opciones_element_mkusr 
                      | opciones_element_mkusr'''
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
def p_opciones_element_mkusr(p):
    '''opciones_element_mkusr : opcionmkusr_usr
                              | opcionmkusr_pwd
                              | opcionmkusr_grp'''
    p[0] = {
        **p[1]
    }
def p_opcionmkusr_usr(p):
    '''opcionmkusr_usr : USER IGUAL ID
                        | USER IGUAL CADENA'''
    #Se guarda el contenido    
    if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1] 
    p[0] = {        
        'user': p[3]
    }
def p_opcionmkusr_pwd(p):
    '''opcionmkusr_pwd : PASS IGUAL ID
                        | PASS IGUAL NUMERO
                        | PASS IGUAL CADENA
                        | PASS IGUAL NUMERO ID'''
                        
    #Se guarda el contenido
    if(len(p) == 4):
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]            
        p[0] = {
            'pass': p[3]
        }
    elif(len(p) == 5):
        p[0] = {
            'pass': p[3] + p[4]
        }
def p_opcionmkusr_grp(p):
    '''opcionmkusr_grp : GRP IGUAL ID
                        | GRP IGUAL CADENA'''
    #Se guarda el contenido    
    if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1] 
    p[0] = {        
        'grp': p[3]
    }
#====================FIN COMANDO MKUSR===================================================================
#========================COMANDO RMUSR===================================================================
def p_rmusr_command(p):
    '''rmusr_command : RMUSR USER IGUAL ID
                     | RMUSR USER IGUAL CADENA'''
                     
    if(p[4][0] == '\"'):
        p[4] = p[4][1:len(p[4])-1]  
    p[0] = {
        'command': 'rmusr',
        'user': p[4]
    }
#====================FIN COMANDO RMUSR===================================================================
#========================COMANDO MKFILE===================================================================
def p_mkfile_command(p):
    '''mkfile_command : MKFILE opciones_mkfile'''
    p[0] = {
        'command': 'mkfile',
        **p[2],
    }
def p_opciones_mkfile(p):
    '''opciones_mkfile : opciones_mkfile opciones_element_mkfile 
                      | opciones_element_mkfile'''
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
def p_opciones_element_mkfile(p):
    '''opciones_element_mkfile : opcionmkfile_path
                              | opcionmkfile_r
                              | opcionmkfile_size
                              | opcionmkfile_cont'''
    p[0] = {
        **p[1]
    }
def p_opcionmkfile_path(p):
    '''opcionmkfile_path : PATH IGUAL RUTA ID
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        p[3] = p[3][1:len(p[3])-1]  
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionmkfile_r(p):
    '''opcionmkfile_r : R'''
    #Se guarda el contenido
    p[0] = {
        'r': True
    }
def p_opcionmkfile_size(p):
    '''opcionmkfile_size : SIZE IGUAL NUMERO'''
    #Se guarda el contenido
    p[0] = {
        'size': p[3]
    }
def p_opcionmkfile_cont(p):
    '''opcionmkfile_cont : CONT IGUAL CADENA
                        | CONT IGUAL RUTA ID'''
    #Se guarda el contenido
    if(len(p) == 4):
        p[3] = p[3][1:len(p[3])-1]  
        p[0] = {
            'cont': p[3]
        }
    else:
        p[0] = {
            'cont': p[3] + "." + p[4]
        }
#====================FIN COMANDO MKFILE===================================================================
#========================COMANDO CAT===================================================================
def p_cat_command(p):
    '''cat_command : CAT opciones_cat'''
    p[0] = {
        'command': 'cat',
        **p[2],
    }
def p_opciones_cat(p):
    '''opciones_cat : opciones_cat opciones_element_cat 
                      | opciones_element_cat'''
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
    
rutas = []
def p_opciones_element_cat(p):
    '''opciones_element_cat : opcioncat_file'''
    p[0] = {
        'file': rutas
    }
def p_opcioncat_file(p):
    '''opcioncat_file : ID IGUAL RUTA ID
                        | ID IGUAL CADENA'''
    if len(p) == 4:
        p[3] = p[3][1:len(p[3])-1]  
        ruta = p[3]
    else:
        ruta = p[3] + '.' + p[4]
    
    rutas.append(ruta)  # Agregar la ruta al vector acumulador
    
    p[0] = {
        'file': ruta  # Devolver la ruta actual
    }
#====================FIN COMANDO CAT===================================================================
#========================COMANDO REMOVE===================================================================
def p_rmfile_command(p):
    '''rmfile_command : REMOVE PATH IGUAL RUTA ID
                      | REMOVE PATH IGUAL RUTA
                      | REMOVE PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 6:
        p[0] = {
            'command': 'remove',
            'path': p[4] + '.' + p[5]
        }
    else:
        if(p[4][0] == '\"'):
            p[4] = p[4][1:len(p[4])-1]
        p[0] = {
            'command': 'remove',
            'path': p[4]
        }
    
#====================FIN COMANDO REMOVE===================================================================
#========================COMANDO EDIT===================================================================
def p_edit_command(p):
    '''edit_command : EDIT opciones_edit'''
    p[0] = {
        'command': 'edit',
        **p[2],
    }
def p_opciones_edit(p):
    '''opciones_edit : opciones_edit opciones_element_edit 
                      | opciones_element_edit'''
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
def p_opciones_element_edit(p):
    '''opciones_element_edit : opcionedit_path
                              | opcionedit_cont'''
    p[0] = {
        **p[1]
    }
def p_opcionedit_path(p):
    '''opcionedit_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionedit_cont(p):
    '''opcionedit_cont : CONT IGUAL CADENA
                        | CONT IGUAL RUTA ID'''
    #Se guarda el contenido
    if(len(p) == 4):
        p[3] = p[3][1:len(p[3])-1]  
        p[0] = {
            'cont': p[3]
        }
    else:
        p[0] = {
            'cont': p[3] + "." + p[4]
        }
#====================FIN COMANDO EDIT===================================================================
#========================COMANDO RENAME===================================================================
def p_rename_command(p):
    '''rename_command : RENAME opciones_rename'''
    p[0] = {
        'command': 'rename',
        **p[2],
    }
def p_opciones_rename(p):
    '''opciones_rename : opciones_rename opciones_element_rename 
                      | opciones_element_rename'''
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
def p_opciones_element_rename(p):
    '''opciones_element_rename : opcionrename_path
                              | opcionrename_name'''
    p[0] = {
        **p[1]
    }
def p_opcionrename_path(p):
    '''opcionrename_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionrename_name(p):
    '''opcionrename_name : NAME IGUAL ID ID
                        | NAME IGUAL ID
                        | NAME IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'name': p[3]
        }
    else:
        p[0] = {
            'name': p[3] + '.' + p[4]
        }
#====================FIN COMANDO RENAME===================================================================
#========================COMANDO MKDIR===================================================================
def p_mkdir_command(p):
    '''mkdir_command : MKDIR opciones_mkdir'''
    p[0] = {
        'command': 'mkdir',
        **p[2],
    }
def p_opciones_mkdir(p):
    '''opciones_mkdir : opciones_mkdir opciones_element_mkdir 
                      | opciones_element_mkdir'''
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
def p_opciones_element_mkdir(p):
    '''opciones_element_mkdir : opcionmkdir_path
                              | opcionmkdir_r'''
    p[0] = {
        **p[1]
    }
def p_opcionmkdir_path(p):
    '''opcionmkdir_path : PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if p[3][0] == '\"':
        p[3] = p[3][1:len(p[3])-1]  
   
    p[0] = {
        'path': p[3]
    }
def p_opcionmkdir_r(p):
    '''opcionmkdir_r : R'''
    #Se guarda el contenido
    p[0] = {
        'r': True
    }
    
#====================FIN COMANDO MKDIR===================================================================
#========================COMANDO COPY===================================================================
def p_copy_command(p):
    '''copy_command : COPY opciones_copy'''
    p[0] = {
        'command': 'copy',
        **p[2],
    }
def p_opciones_copy(p):
    '''opciones_copy : opciones_copy opciones_element_copy 
                      | opciones_element_copy'''
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
def p_opciones_element_copy(p):
    '''opciones_element_copy : opcioncopy_path
                              | opcioncopy_dest'''
    p[0] = {
        **p[1]
    }
def p_opcioncopy_path(p):
    '''opcioncopy_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcioncopy_dest(p):
    '''opcioncopy_dest : DEST IGUAL RUTA ID
                        | DEST IGUAL RUTA
                        | DEST IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'destino': p[3]
        }
    else:
        p[0] = {
            'destino': p[3] + '.' + p[4]
        }
        
#====================FIN COMANDO COPY===================================================================
#========================COMANDO MOVE===================================================================
def p_move_command(p):
    '''move_command : MOVE opciones_move'''
    p[0] = {
        'command': 'move',
        **p[2],
    }
def p_opciones_move(p):
    '''opciones_move : opciones_move opciones_element_move 
                      | opciones_element_move'''
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
def p_opciones_element_move(p):
    '''opciones_element_move : opcionmove_path
                              | opcionmove_dest'''
    p[0] = {
        **p[1]
    }
def p_opcionmove_path(p):
    '''opcionmove_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionmove_dest(p):
    '''opcionmove_dest : DEST IGUAL RUTA ID
                        | DEST IGUAL RUTA
                        | DEST IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'destino': p[3]
        }
    else:
        p[0] = {
            'destino': p[3] + '.' + p[4]
        }
        
#====================FIN COMANDO MOVE===================================================================

#========================COMANDO FIND===================================================================
def p_find_command(p):
    '''find_command : FIND opciones_find'''
    p[0] = {
        'command': 'find',
        **p[2],
    }
def p_opciones_find(p):
    '''opciones_find : opciones_find opciones_element_find 
                      | opciones_element_find'''
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
def p_opciones_element_find(p):
    '''opciones_element_find : opcionfind_path
                              | opcionfind_name'''
    p[0] = {
        **p[1]
    }
def p_opcionfind_path(p):
    '''opcionfind_path : PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionfind_name(p):
    '''opcionfind_name : NAME IGUAL BUSCAR
                        | NAME IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
        p[3] = p[3][1:len(p[3])-1]
    p[0] = {
        'name': p[3]
    }

#====================FIN COMANDO FIND===================================================================
#========================COMANDO CHOWN===================================================================
def p_chown_command(p):
    '''chown_command : CHOWN opciones_chown'''
    p[0] = {
        'command': 'chown',
        **p[2],
    }
def p_opciones_chown(p):
    '''opciones_chown : opciones_chown opciones_element_chown 
                      | opciones_element_chown'''
    #Se guarda el contenido
    if len(p) > 2:
        p[0] = {
            **p[1],
            **p[2],
        }
    else:
        p[0] = {
            **p[1]
        }
def p_opciones_element_chown(p):
    '''opciones_element_chown : opcionchown_path
                              | opcionchown_usr
                              | opcionchown_r'''
    p[0] = {
        **p[1]
    }
def p_opcionchown_path(p):
    '''opcionchown_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionchown_usr(p):
    '''opcionchown_usr : USER IGUAL ID
                        | USER IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
        p[3] = p[3][1:len(p[3])-1]
    p[0] = {
        'user': p[3]
    }
def p_opcionchown_r(p):
    '''opcionchown_r : R'''
    #Se guarda el contenido
    p[0] = {
        'r': True
    }

#====================FIN COMANDO CHOWN===================================================================
#========================COMANDO CHGRP===================================================================
def p_chgrp_command(p):
    '''chgrp_command : CHGRP opciones_chgrp'''
    p[0] = {
        'command': 'chgrp',
        **p[2],
    }
def p_opciones_chgrp(p):
    '''opciones_chgrp : opciones_chgrp opciones_element_chgrp 
                      | opciones_element_chgrp'''
    #Se guarda el contenido
    if len(p) > 2:
        p[0] = {
            **p[1],
            **p[2],
        }
    else:
        p[0] = {
            **p[1]
        }
def p_opciones_element_chgrp(p):
    '''opciones_element_chgrp : opcionchgrp_grp
                              | opcionchgrp_user'''
    p[0] = {
        **p[1]
    }
def p_opcionchgrp_grp(p):
    '''opcionchgrp_grp : GRP IGUAL ID
                        | GRP IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
        p[3] = p[3][1:len(p[3])-1]
    p[0] = {
        'grp': p[3]
    }
def p_opcionchgrp_user(p):
    '''opcionchgrp_user : USER IGUAL ID
                        | USER IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
        p[3] = p[3][1:len(p[3])-1]
    p[0] = {
        'user': p[3]
    }
    
#====================FIN COMANDO CHGRP===================================================================
#========================COMANDO CHMOD===================================================================
def p_chmod_command(p):
    '''chmod_command : CHMOD opciones_chmod'''
    p[0] = {
        'command': 'chmod',
        **p[2],
    }
def p_opciones_chmod(p):
    '''opciones_chmod : opciones_chmod opciones_element_chmod 
                      | opciones_element_chmod'''
    #Se guarda el contenido
    if len(p) > 2:
        p[0] = {
            **p[1],
            **p[2],
        }
    else:
        p[0] = {
            **p[1]
        }
def p_opciones_element_chmod(p):
    '''opciones_element_chmod : opcionchmod_path
                              | opcionchmod_r
                              | opcionchmod_ugo'''
    p[0] = {
        **p[1]
    }
def p_opcionchmod_path(p):
    '''opcionchmod_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionchmod_r(p):
    '''opcionchmod_r : R'''
    #Se guarda el contenido
    p[0] = {
        'r': True
    }
def p_opcionchmod_ugo(p):
    '''opcionchmod_ugo : UGO IGUAL NUMERO'''
    #Se guarda el contenido
    p[0] = {
        'ugo': p[3]
    }

#====================FIN COMANDO CHMOD===================================================================
#======================== PAUSE ===================================================================
def p_pause_command(p):
    '''pause_command : PAUSE'''
    p[0] = {
        'command': 'pause',
    }
#====================FIN PAUSE===================================================================
#======================== COMANDO RECOVERY ===================================================================
def p_recovery_command(p):
    '''recovery_command : RECOVERY ID_CMD IGUAL NUMERO ID'''
    p[0] = {
        'command': 'recovery',
        'id': p[4] + p[5]
    }
#====================FIN RECOVERY===================================================================
#======================== COMANDO LOSS ===================================================================
def p_loss_command(p):
    '''loss_command : LOSS ID_CMD IGUAL NUMERO ID'''
    p[0] = {
        'command': 'loss',
        'id': p[4] + p[5]
    }
    
#====================FIN LOSS===================================================================
#======================== COMANDO REP ===================================================================
def p_rep_command(p):
    '''rep_command : REP opciones_rep'''
    p[0] = {
        'command': 'rep',
        **p[2],
    }
def p_opciones_rep(p):
    '''opciones_rep : opciones_rep opciones_element_rep 
                      | opciones_element_rep'''
    #Se guarda el contenido
    if len(p) > 2:
        p[0] = {
            **p[1],
            **p[2],
        }
    else:
        p[0] = {
            **p[1]
        }
def p_opciones_element_rep(p):
    '''opciones_element_rep : opcionrep_id
                              | opcionrep_path
                              | opcionrep_name
                              | opcionrep_ruta'''
    p[0] = {
        **p[1]
    }
def p_opcionrep_id(p):
    '''opcionrep_id : ID_CMD IGUAL NUMERO ID'''
    #Se guarda el contenido
    p[0] = {
        'id': p[3] + p[4]
    }
def p_opcionrep_path(p):
    '''opcionrep_path : PATH IGUAL RUTA ID
                        | PATH IGUAL RUTA
                        | PATH IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'path': p[3]
        }
    else:
        p[0] = {
            'path': p[3] + '.' + p[4]
        }
def p_opcionrep_name(p):
    '''opcionrep_name : NAME IGUAL ID
                        | NAME IGUAL CADENA'''
    #Se guarda el contenido
    if(p[3][0] == '\"'):
        p[3] = p[3][1:len(p[3])-1]
    p[0] = {
        'name': p[3]
    }
def p_opcionrep_ruta(p):
    '''opcionrep_ruta : RUTAC IGUAL RUTA ID
                        | RUTAC IGUAL RUTA
                        | RUTAC IGUAL CADENA'''
    #Se guarda el contenido
    if len(p) == 4:
        if(p[3][0] == '\"'):
            p[3] = p[3][1:len(p[3])-1]
        p[0] = {
            'ruta': p[3]
        }
    else:
        p[0] = {
            'ruta': p[3] + '.' + p[4]
        }
    
# Error rule for syntax errors
def p_error(p):
    print("\t josep-ubu@Leon-Ubuntu>>> Error al escribir el comando.",p)
    pass

# Construir el parser
# parser = yacc.yacc()

# # Ejemplo de uso
# if __name__ == '__main__':
#     input_string = 'mkdisk -size=5 -unit=M -path="/home/mis discos/Disco3.dsk"'
#     result = parser.parse(input_string)
#     print("Resultado:", result)

"""
    Archivo principal del proyecto: Main.py
    /Analizador -> Contiene el analizador lexico y sintactico
    /Comandos -> Contiene los comandos que se pueden ejecutar
    /Comandos/Estructura -> Contiene las estructuras de datos que se utilizan
    
    Nombre: Jose David Panaza Batres
    Carnet: 202111478
    Curso: Manejo e Implementacion de Archivos
    Seccion: A
    
"""

#Importaciones------------------------------------------------------------------

from Analizador.lexico import *
from Analizador.sintactico import *
from Comandos.MkDisk import *
from Comandos.Execute import *
from Comandos.RmDisk import *
from Comandos.FDisk import *
from Comandos.Mount import *
from Comandos.Unmount import *
from Comandos.Mkfs import *
from Comandos.Login import *
from Comandos.Logout import *
from Comandos.Mkgrp import *
from Comandos.Rmgrp import *
from Comandos.Mkuser import *
from Comandos.Rmusr import *
from Utilities.Utilities import *

#Funcion ejecutar comando-------------------------------------------------------

import warnings

# Deshabilitar warnings para la clase Token y sus duplicados
warnings.filterwarnings("ignore", category=UserWarning, module="ply.lex")

def exe_command(result):
    #Se verifica si existe el comando 
    if('command' in result):
        # Comando Execute
        if(result['command'] == 'execute'):
            if('path' in result):
                c_execute = Execute()
                if(c_execute.run(result['path'])):
                    with open(c_execute.path, "r") as file:
                        lines = file.readlines()
                        for line in lines:
                            result = parser.parse(line)
                            #Si no devuelve nada
                            if result == None:
                                continue 
                            printComment("-----------------------------------------------------------------------------------------------------------------------")
                            printSubtitle("\t " + line )    
                            #se ejecuta el comando                    
                            exe_command(result)
                    printSuccess("\t Execute>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Execute>>> Error al ejecutar el comando\n")
        # Comando MkDisk
        elif(result['command'] == 'mkdisk'):
            #Se verifica que tenga los parametros obligatorios
            if('size' in result and 'path' in result):
                size = result['size']
                path = result['path']
                #Se verifica si tiene los parametros opcionales
                fit = None
                unit = None
                if('fit' in result):
                    fit = result['fit']
                if('unit' in result):
                    unit = result['unit']
                
                #Se ejecuta el comando
                c_mkdisk = MkDisk()
                if(c_mkdisk.run(size, path, fit, unit)):
                    printSuccess("\t MkDisk>>> Comando ejecutado con exito\n")
                else:
                    printError("\t MkDisk>>> Error al ejecutar el comando\n")
            else:
                printError("\t MkDisk>>> Falta un parametro obligatorio\n")
                return
        # Comando RmDisk
        elif(result['command'] == 'rmdisk'):
            if('path' in result):
                c_rmdisk = RmDisk()
                if(c_rmdisk.run(result['path'])):
                    printSuccess("\t RmDisk>>> Comando ejecutado con exito\n")
                else:
                    printError("\t RmDisk>>> Error al ejecutar el comando\n")
        
        # Comando Fdisk
        elif(result['command'] == 'fdisk'):
            if ('path' in result and 'name' in result):
                path = result['path']
                name = result['name']
                
                if(not 'delete' in result and not 'add' in result):
                    if(not 'size' in result):
                        printError("\t Fdisk>>> Falta un parametro obligatorio\n")
                        return
                    
                
                #Se verifica si tiene los parametros opcionales
                size = None
                unit = None
                type = None
                fit = None
                delete = None
                add = None
                
                if('size' in result):
                    size = result['size']
                if('unit' in result):
                    unit = result['unit']
                if('type' in result):
                    type = result['type']
                if('fit' in result):
                    fit = result['fit']
                if('delete' in result):
                    delete = result['delete']
                if('add' in result):
                    add = result['add']
                
                #Se ejecuta el comando
                c_fdisk = FDisk()
                if(c_fdisk.run(size, path, name, unit, type, fit, delete, add)):
                    printSuccess("\t Fdisk>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Fdisk>>> Error al ejecutar el comando\n")
                
            else:
                printError("\t Fdisk>>> Falta un parametro obligatorio\n")
                return
        #Comando Mount
        elif(result['command'] == 'mount'):
            if('path' in result and 'name' in result):
                c_mount = Mount()
                if(c_mount.run(result['path'], result['name'])):
                    printSuccess("\t Mount>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Mount>>> Error al ejecutar el comando\n")
            else:
                printError("\t Mount>>> Falta un parametro obligatorio\n")
                return
        #Comando Unmount
        elif(result['command'] == 'unmount'):
            if('id' in result):
                c_unmount = Unmount()
                if(c_unmount.run(result['id'])):
                    printSuccess("\t Unmount>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Unmount>>> Error al ejecutar el comando\n")
            else:
                printError("\t Unmount>>> Falta un parametro obligatorio\n")
                return
        #Comando Mkfs
        elif(result['command'] == 'mkfs'):
            if('id' in result):
                #Se verifica si tiene los parametros opcionales
                type = None
                fs = None
                
                if('type' in result):
                    type = result['type']
                if('fs' in result):
                    fs = result['fs']
                    
                
                c_mkfs = Mkfs()
                if(c_mkfs.run(result['id'], type, fs)):
                    printSuccess("\t Mkfs>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Mkfs>>> Error al ejecutar el comando\n")
            else:
                printError("\t Mkfs>>> Falta un parametro obligatorio\n")
                return
        #Comando Login
        elif(result['command'] == 'login'):
            if('user' in result and 'pass' in result and 'id' in result):
                c_login = Login()
                if(c_login.run(result['user'], result['pass'], result['id'])):
                    printSuccess("\t Login>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Login>>> Error al ejecutar el comando\n")
            else:
                printError("\t Login>>> Falta un parametro obligatorio\n")
                return
        #Comando Logout
        elif(result['command'] == 'logout'):
            c_logout = Logout()
            if(c_logout.run()):
                printSuccess("\t Logout>>> Comando ejecutado con exito\n")
            else:
                printError("\t Logout>>> Error al ejecutar el comando\n")
        #Comando Mkgrp
        elif(result['command'] == 'mkgrp'):
            if('name' in result):
                c_mkgrp = Mkgrp()
                if(c_mkgrp.run(result['name'])):
                    printSuccess("\t Mkgrp>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Mkgrp>>> Error al ejecutar el comando\n")
            else:
                printError("\t Mkgrp>>> Falta un parametro obligatorio\n")
                return
        #Comando Rmgrp
        elif(result['command'] == 'rmgrp'):
            if('name' in result):
                c_rmgrp = Rmgrp()
                if(c_rmgrp.run(result['name'])):
                    printSuccess("\t Rmgrp>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Rmgrp>>> Error al ejecutar el comando\n")
            else:
                printError("\t Rmgrp>>> Falta un parametro obligatorio\n")
                return
        #Comando Mkuser
        elif(result['command'] == 'mkusr'):
            if('user' in result and 'pass' in result and 'grp' in result):
                c_mkusr = Mkuser()
                if(c_mkusr.run(result['user'], result['pass'], result['grp'])):
                    printSuccess("\t Mkusr>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Mkusr>>> Error al ejecutar el comando\n")
            else:
                printError("\t Mkusr>>> Falta un parametro obligatorio\n")
                return
        #Comando Rmusr
        elif(result['command'] == 'rmusr'):
            if('user' in result):
                c_rmusr = Rmusr()
                if(c_rmusr.run(result['user'])):
                    printSuccess("\t Rmusr>>> Comando ejecutado con exito\n")
                else:
                    printError("\t Rmusr>>> Error al ejecutar el comando\n")
            else:
                printError("\t Rmusr>>> Falta un parametro obligatorio\n")
                return
                

#Main--------------------------------------------------------------------------

if __name__ == '__main__':
    lex = lex.lex() #Se crea el analizador lexico
    parser = yacc.yacc() #Se crea el analizador sintactico
    
    #Se ejecuta el programa
    while True:
        printComment("-----------------------------------------------------------------------------------------------------------------------")
        try:
            s = inputConsole("josep-ubu@Leon-Ubuntu>>> ")
            print("")
        except EOFError:
            break
        if not s:
            continue
        if(s == 'exit'):
            break
        #Se ejecuta el comando
        result = parser.parse(s)
        if(result == None):
            #print("\t josep-ubu@Leon-Ubuntu>>> Comando no reconocido, o existe un error en su escritura.\n")
            continue
        exe_command(result) #Se llama a la funcion que ejecuta el comando
                
                    
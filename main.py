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

#Funcion ejecutar comando-------------------------------------------------------

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
                            print(line)
                            result = parser.parse(line)
                            exe_command(result)
                    print("\t Execute>>> Comando ejecutado con exito\n")
                else:
                    print("\t Execute>>> Error al ejecutar el comando\n")
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
                    print("\t MkDisk>>> Comando ejecutado con exito\n")
                else:
                    print("\t MkDisk>>> Error al ejecutar el comando\n")
            else:
                print("\t MkDisk>>> Falta un parametro obligatorio\n")
                return
        # Comando RmDisk
        elif(result['command'] == 'rmdisk'):
            if('path' in result):
                c_rmdisk = RmDisk()
                if(c_rmdisk.run(result['path'])):
                    print("\t RmDisk>>> Comando ejecutado con exito\n")
                else:
                    print("\t RmDisk>>> Error al ejecutar el comando\n")
        
        # Comando Fdisk
        elif(result['command'] == 'fdisk'):
            if ('path' in result and 'name' in result):
                path = result['path']
                name = result['name']
                
                if(not 'delete' in result and not 'add' in result):
                    if(not 'size' in result):
                        print("\t Fdisk>>> Falta un parametro obligatorio\n")
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
                    print("\t Fdisk>>> Comando ejecutado con exito\n")
                else:
                    print("\t Fdisk>>> Error al ejecutar el comando\n")
                
            else:
                print("\t Fdisk>>> Falta un parametro obligatorio\n")
                return
                
                

#Main--------------------------------------------------------------------------

if __name__ == '__main__':
    lex = lex.lex() #Se crea el analizador lexico
    parser = yacc.yacc() #Se crea el analizador sintactico
    
    #Se ejecuta el programa
    while True:
        try:
            s = input('josep-ubu@Leon-Ubuntu: ')
        except EOFError:
            break
        if not s:
            continue
        #Se ejecuta el comando
        result = parser.parse(s)
        exe_command(result) #Se llama a la funcion que ejecuta el comando
                
                    
from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *
class Rmgrp():
    
    #Constructor---------------------------------------------------------------------------
    def __init__(self) -> None:
        self.name = None
        
    #Setters-------------------------------------------------------------------------------
    
    def set_name(self, name): #Definir el nombre
        if name == None:
            printError("\t Rmgrp>>> Falta el nombre del grupo\n")
            return False
        self.name = name
        return True
    
    #Definir el RMGRP-----------------------------------------------------------------------
    
    def run(self, name): #Ejecutar el comando
        if(not self.set_name(name)): return False
        
        if(self.eliminar_grupo()):
            printText("\t Rmgrp>>> Grupo eliminado con exito\n")
            return True
        return False
    
    #Eliminar un grupo----------------------------------------------------------------------
    
    def eliminar_grupo(self):
        if(len(user_session) == 0):
            printError("\t Rmgrp>>> No existe una sesion iniciada\n")
            return False
        
        crruser = user_session[0]
        
        if (crruser.user != "root"):
            printError("\t Rmgrp>>> No tiene permisos de administrador\n")
            return False
        
        #Se verifica si existe el grupo
        #Se obtiene el contenido
        vecArch = getInodeInfo(crruser.partitionId, 'user.txt')
        #se une todo el contenido en un solo vector
        contenidoarch = ['']
        for contenido in vecArch:
            contenidoarch[0] = contenidoarch[0] + contenido[0]
        contgrupo = 1
        cadena = []
        for contenido in contenidoarch:
            usuarios = contenido.split('\n')
            for usuario in usuarios:  
                if usuario != '':              
                    cadena.append(usuario + '\n')
                elif usuario == '':
                    continue
                usuarioparam = usuario.split(',')
                if usuarioparam[0] == '0':
                    continue
                if len(usuarioparam) == 3:
                    #Se verifica si existe el grupo
                    if usuarioparam[2] == self.name:
                        #Se elimina el grupo
                        cadena.pop()                        
                        cadena_nueva = '0' + ',G,' + self.name + '\n'    
                        cadena.append(cadena_nueva)                   
                    contgrupo += 1
                

        #Se concatena el contenido del vector
        cont = ''
        for contenido in cadena:
            cont += contenido
            
        #Se guarda el contenido en el archivo
        if(modifyBlockContent(crruser.partitionId, crruser.numfblock, cont)):
            return True
        return False
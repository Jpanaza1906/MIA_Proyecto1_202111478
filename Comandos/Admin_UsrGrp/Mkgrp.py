from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *
class Mkgrp():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.name = None
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_name(self, name): #Definir el nombre
        if name == None:
            printError("\t Mkgrp>>> Falta el nombre del grupo\n")
            return False
        self.name = name
        return True
    
    #Definir el MKGRP--------------------------------------------------------------------------------
    
    def run(self, name): #Ejecutar el comando
        if(not self.set_name(name)): return False
        
        if(self.crear_grupo()): 
            printText("\t Mkgrp>>> Grupo creado con exito\n")
            return True
        return False
    
    #Crear un grupo-----------------------------------------------------------------------------------
    
    def crear_grupo(self):
        if(len(user_session) == 0):
            printError("\t Mkgrp>>> No existe una sesion iniciada\n")
            return False
        
        crruser = user_session[0]
        
        if (crruser.user != "root"):
            printError("\t Mkgrp>>> No tiene permisos de administrador\n")
            return False
        
        ##Se obtiene el contenido
        vecArch = getInodeInfo(crruser.partitionId, 'user.txt')
        #se une todo el contenido en un solo vector
        contenidoarch = ['']
        for contenido in vecArch:
            contenidoarch[0] = contenidoarch[0] + contenido[0]
        
        contgrupo = 1
        for contenido in contenidoarch:
            usuarios = contenido.split('\n')
            for usuario in usuarios:
                usuarioparam = usuario.split(',')
                if usuarioparam[0] == '0':
                    continue
                if len(usuarioparam) == 3:
                    #Se verifica si existe el grupo
                    if usuarioparam[2] == self.name:
                        printError("\t Mkgrp>>> El grupo ya existe\n")
                        return False
                    contgrupo += 1
        
        contenido = contenidoarch[0]
        #Se crea el grupo
        contenido += str(contgrupo) + ',G,' + self.name + '\n'
        
        if (modifyInodePointers(crruser.partitionId, 'user.txt', contenido)):
            return True
        return False
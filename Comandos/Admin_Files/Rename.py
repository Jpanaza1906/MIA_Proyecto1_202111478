from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

class Rename():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.path = None
        self.name = None
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if path == None:
            printError("\t Rename>>> Falta el path\n")
            return False
        self.path = path
        return True
    
    def set_name(self, name): #Definir el name
        if name == None:
            printError("\t Rename>>> Falta el name\n")
            return False
        self.name = name
        return True
    
    #Definir el RENAME--------------------------------------------------------------------------------
    
    def run(self, path, name): #Ejecutar el comando
        
        if(not self.set_path(path)): return False
        if(not self.set_name(name)): return False
        
        if(self.renombrar()):
            printText("\t Rename>>> Archivo renombrado con exito\n")
            return True
        return False
    
    #Renombrar un archivo-----------------------------------------------------------------------------------
    
    def renombrar(self):
        if(len(user_session)==0):
            printError("\t Rename>>> No existe una sesion iniciada\n")
            return False
        
        crruser = user_session[0]
        
        ninodo = getInodeNumberFromPath(crruser.partitionId, self.path)
        
        if ninodo == -1:
            printError("\t Rename>>> El archivo no existe\n")
            return False
        
        #Se separa el nodo padre del archivo o carpeta
        rutacompleta = [elemento for elemento in self.path.split('/') if elemento]
        #se obtiene el nombre del archivo
        nombre = rutacompleta.pop()
        
        rutafinalpadre = ""
        for elemento in rutacompleta:
            rutafinalpadre = rutafinalpadre + "/" + elemento
            
        
        if(modifyNameContent(crruser.partitionId, rutafinalpadre, nombre, self.name)):
            return True
        return False
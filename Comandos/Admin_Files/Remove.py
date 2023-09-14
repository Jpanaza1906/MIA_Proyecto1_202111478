from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

class Remove():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.path = ''
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if path == None:
            printError("\t Remove>>> Falta el path\n")
            return False
        self.path = path
        return True
    
    #Definir el REMOVE-----------------------------------------------------------------------------------
    
    def run(self, path): #Ejecutar el comando        
        
        if(not self.set_path(path)): return False
        
        if(self.eliminar_archivo()):
            printText("\t Remove>>> Archivo eliminado con exito\n")
            return True
        return False
    
    #Funciones---------------------------------------------------------------------------------------
    
    def eliminar_archivo(self):
        if(len(user_session) == 0):
            printError("\t Remove>>> No hay sesion activa\n")
            return False
                
        crruser = user_session[0]
        
        #se obtiene el nombre del archivo con la ruta que viene en file
        
        ninodo = getInodeNumberFromPath(crruser.partitionId, self.path)
        
        if ninodo == -1:
            printError("\t Remove>>> No existe el archivo " + self.path + "\n")
            return False
        
        #Se separa el nodo padre del archivo o carpeta
        rutacompleta = [elemento for elemento in self.path.split('/') if elemento]
        #se obtiene el nombre del archivo
        nombre = rutacompleta.pop()
        
        rutafinalpadre = ""
        for elemento in rutacompleta:
            rutafinalpadre = rutafinalpadre + "/" + elemento
            
        
        #Se obtiene el inodo del archivo
        
        if(removeFolderFile(crruser.partitionId, rutafinalpadre, nombre)):
            return True
        return False
        
        
        
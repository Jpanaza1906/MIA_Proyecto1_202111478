from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *
from datetime import datetime

class Copy():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.path = ''
        self.dest = ''
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if path == None:
            printError("\t Copy>>> Falta el path\n")
            return False
        self.path = path
        return True
    
    def set_dest(self, dest): #Definir el path
        if dest == None:
            printError("\t Copy>>> Falta el destino\n")
            return False
        self.dest = dest
        return True
    
    #Definir el COPY-----------------------------------------------------------------------------------
    
    def run(self, path, dest): #Ejecutar el comando
        
        if(not self.set_path(path)): return False
        if(not self.set_dest(dest)): return False
        
        if(self.copiar_archivo()):
            printText("\t Copy>>> Archivo copiado con exito\n")
            return True
        return False
    
    #Funciones---------------------------------------------------------------------------------------
    
    def copiar_archivo(self):
        if(len(user_session) == 0):
            printError("\t Copy>>> No hay sesion activa\n")
            return False
        
        crruser = user_session[0]
        
        #se obtiene el nombre del archivo con la ruta que viene en file
        
        ninodo = getInodeNumberFromPath(crruser.partitionId, self.path)
        
        if ninodo == -1:
            printError("\t Copy>>> No existe el directorio " + self.path + "\n")
            return False
        
        ninodo_dest = getInodeNumberFromPath(crruser.partitionId, self.dest)
        
        if ninodo_dest == -1:
            printError("\t Copy>>> No existe el directorio " + self.dest + "\n")
            return False
        
        if(copyFolderFile(crruser.partitionId, self.path, self.dest, datetime.now().strftime("%d/%m/%Y"))):
            return True
        return False
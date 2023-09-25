from datetime import datetime
from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

class Mkdir():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.path = None
        self.r = False
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if path == None:
            printError("\t Mkdir>>> Falta el path\n")
            return False
        self.path = path
        return True
    
    def set_r(self, r): #Definir el r
        self.r = r
        return True
    
    #Definir el MKDIR--------------------------------------------------------------------------------
    
    def run(self, path, r): #Ejecutar el comando
        if(not self.set_path(path)): return False
        if(not self.set_r(r)): return False
        
        if(self.crear_directorio()):
            printText("\t Mkdir>>> Directorio creado con exito\n")
            return True
        return False
    
    #Crear un directorio-----------------------------------------------------------------------------------
    
    def crear_directorio(self):
        if(len(user_session) == 0):
            printError("\t Mkdir>>> No existe una sesion iniciada\n")
            return False

        #Se crea la carpeta en el sistema de archivos
        crruser = user_session[0]        
        #Se obtiene la fecha
        fecha = datetime.now().strftime("%d/%m/%Y")
        contr = 0
        if(self.r):
            #Se verifica que exista carpeta por carpeta en el sistema de archivos
            carpetas = [elemento for elemento in self.path.split('/') if elemento != '']
            path = ''
            
            if len(carpetas) == 1:
                printError("\t Mkdir>>> El parametro -r solo puede ser utilizado cuando no existen las carpetas\n")
                return False
            
            for i in range(len(carpetas)):
                path = path + '/' + carpetas[i] 
                inodon = getInodeNumberFromPath(crruser.partitionId, path) 
                
                if inodon == -1:
                    if(createFolder(crruser.partitionId, path, fecha)):
                        continue
                    return False
                else:
                    contr += 1
                
                if contr == len(carpetas) - 1:
                    printError("\t Mkdir>>> Ya existe la carpeta padre para utilizar -r\n")   
            return True
                
        if(createFolder(crruser.partitionId, self.path, fecha)):
            return True
        return False

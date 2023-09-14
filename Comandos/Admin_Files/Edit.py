from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

class Edit():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.path = None
        self.cont = None
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if path == None:
            printError("\t Edit>>> Falta el path\n")
            return False
        self.path = path
        return True
    
    def set_cont(self, cont): #Definir el cont
        self.cont = cont
        return True
    
    #Definir el EDIT--------------------------------------------------------------------------------
    
    def run(self, path, cont): #Ejecutar el comando
        
        if(not self.set_path(path)): return False
        if(not self.set_cont(cont)): return False
        
        if(self.editar_archivo()):
            printText("\t Edit>>> Archivo editado con exito\n")
            return True
        return False
    
    #Editar un archivo-----------------------------------------------------------------------------------
    
    def editar_archivo(self):
        if(len(user_session) == 0):
            printError("\t Edit>>> No existe una sesion iniciada\n")
            return False
        
        crruser = user_session[0]
        
        ninodo = getInodeNumberFromPath(crruser.partitionId, self.path)
        
        if ninodo == -1:
            printError("\t Edit>>> El archivo no existe\n")
            return False
        
        contenido = ''
        #Se obtiene el contenido del archivo cont 
        try:
            archivo = open(self.cont, "r")
            contenido = archivo.read()
            archivo.close()
        except Exception as e:
            printError("\t Edit>>> No se pudo abrir el archivo\n")
            return False
        
        if (modifyFileContent(crruser.partitionId, self.path, contenido)):
            printText("\t Edit>>> Se edito el archivo con exito\n")
            return True
        return False
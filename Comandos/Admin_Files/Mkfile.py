from Utilities.Utilities import *
from Global.Global import *

class Mkfile():
        
        #Constructor-------------------------------------------------------------------------------------
        
        def __init__(self) -> None:
            self.path = None
            self.r = False
            self.size = None
            self.cont = None
            
        #Setters-----------------------------------------------------------------------------------------
        
        def set_path(self, path): #Definir el path
            if path == None:
                printError("\t Mkfile>>> Falta el path\n")
                return False
            self.path = path
            return True
        
        def set_r(self, r): #Definir el r
            self.r = r
            return True
        
        def set_size(self, size): #Definir el size
            try:
                size = int(size)
                if size > 0:
                    self.size = size
                    return True
                else:
                    printError("\t Mkfile>>> El size debe ser mayor a 0\n")
                    return False
            except Exception as e:
                printError("\t Mkfile>>> El size debe ser un numero entero\n")
                return False
            
        def set_cont(self, cont): #Definir el cont
            self.cont = cont
            return True
        
        #Definir el MKFILE--------------------------------------------------------------------------------
        
        def run(self, path, r, size, cont): #Ejecutar el comando
            if(not self.set_path(path)): return False
            if(not self.set_r(r)): return False
            if(not self.set_size(size)): return False
            if(not self.set_cont(cont)): return False
            
            if(self.crear_archivo()):
                printText("\t Mkfile>>> Archivo creado con exito\n")
                return True
            return False
        
        #Crear un archivo-----------------------------------------------------------------------------------
        
        def crear_archivo(self):
            pass
                
            
            
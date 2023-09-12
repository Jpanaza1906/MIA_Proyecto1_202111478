#COMANDO RMDISK
import os
from Utilities.Utilities import *

class RmDisk():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.path = ''

    #Setters-------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if(not os.path.isfile(path)):
            printError("\t RmDisk>>> El disco no existe\n")
            return False
        if(not path.endswith('.dsk')):
            printError("\t RmDisk>>> El path no tiene la extension .dsk\n")
            return False
        #Se guarda el path
        self.path = path
        return True

    #Definir el RMDISK-------------------------------------------------------------------
    
    def run(self, path): #Ejecutar el comando
        if(not self.set_path(path)): return False
        
        try:
            #Mensaje de confirmacion
            confirm = inputWarning("\t RmDisk>>> Esta seguro que desea eliminar el disco? (Y/N):")
            if(confirm.lower() != 'y'): return False
            
            #Se elimina el disco
            os.remove(self.path)
            printText("\t RmDisk>>> Disco eliminado exitosamente\n")
            return True
        except Exception as e:
            printError("\t RmDisk>>> Ocurrio un error al eliminar el disco\n")
            return False
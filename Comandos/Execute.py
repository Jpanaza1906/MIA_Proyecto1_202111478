#COMANDO EXECUTE
import os
from Utilities.Utilities import *

class Execute():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.path = ''
    
    #Setters-------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if(not os.path.exists(path)):
            printError("\t Execute>>> El path no existe\n")
            return False
        if(not path.endswith('.adsj')):
            printError("\t Execute>>> El path no tiene la extension .adsj\n")
            return False
        self.path = path
        return True
    
    #Definir el EXECUTE--------------------------------------------------------
    
    def run(self, path):
        if(not self.set_path(path)): return False
        
        #Se confirma el execute
        printTitle("\t Execute>>> Ejecutando el archivo: " + path +" \n")
        return True
    

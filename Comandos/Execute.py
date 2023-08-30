#COMANDO EXECUTE
import os

class Execute():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.path = ''
    
    #Setters-------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if(not os.path.exists(path)):
            print("\t Execute>>> El path no existe")
            return False
        if(not path.endswith('.adsj')):
            print("\t Execute>>> El path no tiene la extension .adsj")
            return False
        self.path = path
        return True
    
    #Definir el EXECUTE--------------------------------------------------------
    
    def run(self, path):
        if(not self.set_path(path)): return False
        
        #Se confirma el execute
        print("\t Execute>>> Ejecutando el archivo: " + path)
        return True
    

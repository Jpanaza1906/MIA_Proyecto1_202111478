#COMANDO RMDISK
import os

class RmDisk():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.path = ''

    #Setters-------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if(not os.path.isfile(path)):
            print("\t RmDisk>>> El disco no existe")
            return False
        if(not path.endswith('.dsk')):
            print("\t RmDisk>>> El path no tiene la extension .dsk")
            return False
        #Se guarda el path
        self.path = path
        return True

    #Definir el RMDISK-------------------------------------------------------------------
    
    def run(self, path): #Ejecutar el comando
        if(not self.set_path(path)): return False
        
        try:
            #Mensaje de confirmacion
            confirm = input("\t RmDisk>>> Esta seguro que desea eliminar el disco? (Y/N): ")
            if(confirm.lower() != 'y'): return False
            
            #Se elimina el disco
            os.remove(self.path)
            print("\t RmDisk>>> Disco eliminado exitosamente")
            return True
        except Exception as e:
            print("\t RmDisk>>> Ocurrio un error al eliminar el disco")
            return False
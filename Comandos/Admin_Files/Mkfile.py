from datetime import datetime
from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

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
            if size == None:
                self.size = None
                return True
            try:
                size = int(size)
                if size >= 0:
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
            if(len(user_session) == 0):
                printError("\t Mkfile>>> No existe una sesion iniciada\n")
                return False
            
            crruser = user_session[0]
            #Se obtiene la fecha
            fecha = datetime.now().strftime("%d/%m/%Y")
            contr = 0
            if(self.r):
                #Se verifica que exista carpeta por carpeta en el sistema de archivos
                carpetas = [elemento for elemento in self.path.split('/') if elemento != '']
                path = ''
                
                if len(carpetas) == 1:
                    printError("\t Mkfile>>> El parametro -r solo puede ser utilizado cuando no existen las carpetas\n")
                    return False
                
                for i in range(len(carpetas)):
                    path = path + '/' + carpetas[i] 
                    inodon = getInodeNumberFromPath(crruser.partitionId, path) 
                    
                    if inodon == -1:
                        if i == len(carpetas) - 1:
                            if(createFile(crruser.partitionId, path, fecha, self.size, self.cont)):
                                continue
                            return False
                        if(createFolder(crruser.partitionId, path, fecha)):
                            continue
                        return False
                    else:
                        contr += 1
                    
                    if contr == len(carpetas) - 1:
                        break
                return True
            
            if(createFile(crruser.partitionId, self.path, fecha, self.size, self.cont)):
                return True
            return False
            
                
            
            
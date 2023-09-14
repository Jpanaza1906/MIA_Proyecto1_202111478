from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

class Cat():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.files = []
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_files(self, files): #Definir los files
        if files == None:
            printError("\t Cat>>> Falta el files\n")
            return False
        self.files = files
        return True
    
    #Definir el CAT-----------------------------------------------------------------------------------
    
    def run(self, files): #Ejecutar el comando
        
        if(not self.set_files(files)): return False
        
        if (self.leer_archivos()):
            printText("\t Cat>>> Archivos leidos con exito\n")
            return True
        return False
    
    #Funciones---------------------------------------------------------------------------------------
    
    def leer_archivos(self):
        if(len(user_session) == 0):
            printError("\t Cat>>> No hay sesion activa\n")
            return False
        
        crruser = user_session[0]
                
        #Contenido de los archivos
        contenidoleido = ""
        for file in self.files:
            #se obtiene el nombre del archivo con la ruta que viene en file
            rutacompleta = file
            #se obtiene el nombre del archivo
            nombre = rutacompleta.split("/").pop()
            
            ninodo = getInodeNumberFromPath(crruser.partitionId, rutacompleta)
            
            if ninodo == -1:
                printError("\t Cat>>> No existe el archivo " + nombre + "\n")
                return False
            
            vecArch = getFileContentFromPath(crruser.partitionId, rutacompleta)
            #Se une todo el contenido en un solo vector
            contenidoarch = ['']
            for contenido in vecArch:
                contenidoarch[0] = contenidoarch[0] + contenido[0]
            
            if contenidoarch[0] == '':
                printError("\t Cat>>> No existe contenido en el archivo " + nombre + "\n")
                return False
            contenidoleido = contenidoleido + "Contenido del archivo " + nombre + ":\n"
            contenidoleido = contenidoleido + contenidoarch[0] + "\n"
            
        printText(contenidoleido)
        return True
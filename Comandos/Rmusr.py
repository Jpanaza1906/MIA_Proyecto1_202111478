from Utilities.Utilities import *
from Global.Global import *
from .Estructura.Funcs import *

class Rmusr():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.user = None
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_user(self, user): #Definir el nombre
        if user == None:
            printError("\t Rmusr>>> Falta el nombre del usuario\n")
            return False
        self.user = user
        return True
    
    #Definir el RMUSR--------------------------------------------------------------------------------
    
    def run(self, user): #Ejecutar el comando
        if(not self.set_user(user)): return False
        
        if(self.eliminar_usuario()):
            printText("\t Rmusr>>> Usuario eliminado con exito\n")
            return True
        return False
    
    #Eliminar un usuario-----------------------------------------------------------------------------------
    
    def eliminar_usuario(self):
        if(len(user_session) == 0):
            printError("\t Rmusr>>> No existe una sesion iniciada\n")
            return False
        
        crruser = user_session[0]
        
        if (crruser.user != "root"):
            printError("\t Rmusr>>> No tiene permisos de administrador\n")
            return False
        
        if self.user == 'root':
            printError("\t Rmusr>>> No se puede eliminar al usuario root\n")
            return False
        
        #Se verifica si existe el usuario
        #Se obtiene el contenido
        vecArch = getInodeInfo(crruser.partitionId, 'user.txt')
        #se une todo el contenido en un solo vector
        contenidoarch = ['']
        for contenido in vecArch:
            contenidoarch[0] = contenidoarch[0] + contenido[0]
        
        cadena = []
        for contenido in contenidoarch:
            usuarios = contenido.split('\n')
            for usuario in usuarios:  
                if usuario != '':              
                    cadena.append(usuario + '\n')
                elif usuario == '':
                    continue
                usuarioparam = usuario.split(',')
                if usuarioparam[0] == '0':
                    continue
                if len(usuarioparam) == 3:                    
                    continue
                else:
                    #Se verifica si existe el usuario
                    if usuarioparam[3] == self.user:
                        #Se elimina el usuario
                        cadena.pop()                        
                        cadena_nueva = '0' + ',U,' + usuarioparam[2] + ',' + usuarioparam[3] + ',' + usuarioparam[4] + '\n'    
                        cadena.append(cadena_nueva)      
                    
        #Se escribe en el archivo
        cont = ''
        for contenido in cadena:
            cont += contenido
            
        #Se guarda el contenido en el archivo
        if(modifyBlockContent(crruser.partitionId, crruser.numfblock, cont)):
            return True
        return False
    
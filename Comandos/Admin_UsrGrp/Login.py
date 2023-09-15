from Utilities.Utilities import *
from ..Estructura.Super_block import *
from ..Estructura.Ebr import *
from ..Estructura.Table_inode import *
from ..Estructura.Load import *
from ..Estructura.Folder_block import *
from ..Estructura.File_block import *
from ..Estructura.Journaling import *
from ..Estructura.Funcs import *

class Login():
    
    # Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.user = ''
        self.password = ''
        self.id = ''
    
    # Setters-------------------------------------------------------------------
    
    def set_user(self, user): # Definir el usuario
        if(user == None):
            printError("\t Login>>> Usuario no definido\n")
            return False
        # Se guarda el usuario
        self.user = user
        return True
    
    def set_password(self, password): # Definir la contraseña
        if(password == None):
            printError("\t Login>>> Contraseña no definida\n")
            return False
        # Se guarda la contraseña
        self.password = password
        return True
    
    def set_id(self, id): # Definir el id
        if(id == None):
            printError("\t Login>>> Falta un parametro obligatorio\n")
            return False
        # Se guarda el id
        self.id = id
        return True
    
    # Definir el LOGIN-----------------------------------------------------------
    
    def run(self, user, password, id): # Ejecutar el comando
        if(not self.set_user(user)): return False
        if(not self.set_password(password)): return False
        if(not self.set_id(id)): return False
        
        # Se verifica si existe el usuario
        if (self.iniciar_sesion()):
            printText("\t Login>>> Se inicio sesion con exito\n")
            return True
        return False
    
    # Iniciar sesion------------------------------------------------------------
    
    def iniciar_sesion(self):
        if len(user_session) > 0:
            printError("\t Login>>> Ya existe una sesion iniciada\n")
            return False
        
        #Se verifica si existe la particion
        crrpartition = buscar_particion(self.id)
        
        if crrpartition == None:
            printError("\t Login>>> No existe la particion\n")
            return False
        
        #Se obtiene el contenido
        vecArch = getFileContentFromPath(self.id, 'user.txt')
        #se une todo el contenido en un solo vector
        contenidoArch = ['']
        for contenido in vecArch:
            contenidoArch[0] = contenidoArch[0] + contenido[0]
        
        #se evalua el contenido del archivo    
        flag = True      
        for contenido in contenidoArch:
            usuarios = contenido.split('\n')
            for usuario in usuarios:
                if usuario == '':
                    continue
                usuarioparam = usuario.split(',')
                if len(usuarioparam) == 3:
                    if usuarioparam[0] == '0':
                        flag = False
                        continue
                    flag = True
                    continue
                if not flag:
                    continue
                if usuarioparam[0] == '0':
                    continue
                if usuarioparam[3] == self.user:
                    if usuarioparam[4] == self.password:
                        usertemp = UserActive(usuarioparam[0], usuarioparam[1], usuarioparam[2], usuarioparam[3], usuarioparam[4],contenidoArch[0][1] ,self.id)
                        user_session.append(usertemp)
                        return True
                    else:
                        printError("\t Login>>> Contraseña incorrecta\n")
                        return False
        printError("\t Login>>> Usuario no encontrado\n")
        return False              
        
        
        
from Utilities.Utilities import *
from Global.Global import *
from ..Estructura.Funcs import *

class Mkuser():
    
    #Constructor-------------------------------------------------------------------------------------
    
    def __init__(self) -> None:
        self.user = None
        self.password = None
        self.group = None
    
    #Setters-----------------------------------------------------------------------------------------
    
    def set_user(self, user): #Definir el nombre
        if user == None:
            printError("\t Mkuser>>> Falta el nombre del usuario\n")
            return False
        self.user = user
        return True
    
    def set_password(self, password): #Definir la contraseña
        if password == None:
            printError("\t Mkuser>>> Falta la contraseña del usuario\n")
            return False
        self.password = password
        return True
    
    def set_group(self, group): #Definir el grupo
        if group == None:
            printError("\t Mkuser>>> Falta el grupo del usuario\n")
            return False
        self.group = group
        return True
    
    #Definir el MKUSER--------------------------------------------------------------------------------
    
    def run(self, user, password, group): #Ejecutar el comando
        if(not self.set_user(user)): return False
        if(not self.set_password(password)): return False
        if(not self.set_group(group)): return False
        
        if(self.crear_usuario()):
            printText("\t Mkuser>>> Usuario creado con exito\n")
            return True
        return False
    
    #Crear un usuario-----------------------------------------------------------------------------------
    
    def crear_usuario(self):
        if(len(user_session) == 0):
            printError("\t Mkuser>>> No existe una sesion iniciada\n")
            return False
        
        crruser = user_session[0]
        
        if (crruser.user != "root"):
            printError("\t Mkuser>>> No tiene permisos de administrador\n")
            return False
        
        #Se verifica si existe el usuario
        #Se obtiene el contenido
        vecArch = getInodeInfo(crruser.partitionId, 'user.txt')
        #se une todo el contenido en un solo vector
        contenidoarch = ['']
        for contenido in vecArch:
            contenidoarch[0] = contenidoarch[0] + contenido[0]
            
        cont_grupo = 0
        cadena = []
        buengrupo = False
        encontrado = False
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
                    if buengrupo:
                        cadena_nueva = str(cont_grupo) + ',U,' + self.group + ',' + self.user + ',' + self.password + '\n'
                        cadena.append(cadena_nueva)
                        buengrupo = False
                    if usuarioparam[2] == self.group:
                        buengrupo = True
                        encontrado = True
                    cont_grupo += 1
                    continue
                else:
                    if usuarioparam[3] == self.user:
                        printError("\t Mkuser>>> El usuario ya existe\n")
                        return False
        
        if buengrupo:
            cadena_nueva = str(cont_grupo) + ',U,' + self.group + ',' + self.user + ',' + self.password + '\n'
            cadena.append(cadena_nueva)
            buengrupo = False
                    
        if not encontrado:
            printError("\t Mkuser>>> El grupo no existe\n")
            return False
        
        #Se concatena el contenido del vector
        cont = ''
        for contenido in cadena:
            cont += contenido
            
        #Se guarda el contenido en el archivo
        if(modifyBlockContent(crruser.partitionId, crruser.numfblock, cont)):
            return True
        return False
    
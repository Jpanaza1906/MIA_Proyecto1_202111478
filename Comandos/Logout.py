from Utilities.Utilities import *
from Global.Global import *
class Logout():
    
    # Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.logout = True
    
    # Definir el LOGOUT-----------------------------------------------------------
    
    def run(self): # Ejecutar el comando
        if (self.cerrar_sesion()):
            printText("\t Logout>>> Se cerro sesion con exito\n")
            return True
        return False
    
    # Cerrar sesion------------------------------------------------------------
    
    def cerrar_sesion(self):
        if len(user_session) == 0:
            printError("\t Logout>>> No existe una sesion iniciada\n")
            return False
        
        user_session.pop()
        return True
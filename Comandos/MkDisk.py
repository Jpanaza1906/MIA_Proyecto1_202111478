#COMANDO MKDISK
import os
import subprocess
from .Estructura.Load import *
from .Estructura.Mbr import *
from Utilities.Utilities import *
from datetime import datetime
import random


class MkDisk():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.size = 0
        self.path = ''
        self.fit = ''
        self.unit = ''

    #Setters-------------------------------------------------------------------
    
    def set_size(self, size): #Definir el tamaño
        try:
            size = int(size)
            if size > 0:
                if(self.unit == 'K'):
                    size = size * 1024
                elif(self.unit == 'M'):
                    size = size * 1024 * 1024
                else:
                    printError("\t MkDisk>>> Ocurrio un error al definir el tamaño\n")
                    return False
            else:
                printError("\t MkDisk>>> El tamaño debe ser mayor a 0\n")
                return False
            
            #Se guarda el tamaño en bytes
            self.size = size
            return True
        except Exception as e:
            printError("\t MkDisk>>> El tamaño debe ser un numero entero\n")
            return False
    
    def set_path(self, path): #Definir el path
        if(os.path.exists(path)):
            printError("\t MkDisk>>> El path ya existe\n")
            return False
        if(not path.endswith('.dsk')):
            printError("\t MkDisk>>> El path no tiene la extension .dsk\n")
            return False
        #Se guarda el path
        folder_path = os.path.dirname(path)
        os.makedirs(folder_path, exist_ok=True)
        self.path = path
        return True
    
    def set_fit(self, fit): #Definir el fit
        if fit == None:
            self.fit = 'F'
            return True
        elif fit.lower() == 'bf' or 'ff' or 'wf' :
            self.fit = fit[0].upper()
            return True
        printError("\t MkDisk>>> El fit no es valido\n")
        return False
    
    def set_unit(self, unit): #Definir el unit
        if unit == None:
            self.unit = "M"
            return True  
        elif unit.lower() == 'k' or 'm' :
            self.unit = unit.upper()
            return True
        printError("\t MkDisk>>> El unit no es valido\n")
        return False
    
    #Definir el MKDISK --------------------------------------------------------
    
    def run(self, size, path, fit, unit):
        if(not self.set_unit(unit)): return False
        if(not self.set_size(size)): return False
        if(not self.set_fit(fit)): return False
        if(not self.set_path(path)): return False
        
        #Se crea el disco
        if(self.crear_disco()):
            printText("\t MkDisk>>> Disco creado con exito\n")
            return True
        return False
    
    # Crear un disco -----------------------------------------------------------
    
    def crear_disco(self):
        try:
            #Se crea el Mbr
            disco = Mbr()
            disco.set_mbr(self.size, datetime.now().strftime("%d/%m/%Y"), random.randint(1,99999999), self.fit)
            
            #Se escribe el Mbr en el disco
            if(Fcreate_file(self.path)) : return
            file = open(self.path, "rb+")
            Winit_size(file, self.size)
            inicio = 0 #Se escribe en el primer byte del disco
            
            Fwrite_displacement(file, inicio, disco)
            file.close()
            return True
        except Exception as e:
            printError("\t MkDisk>>> Ocurrio un error al crear el disco\n")
            return False
        
        
    
# COMANDO MKDISK
import os
from .Estructura.load import *
from .Estructura.Mbr import *
from datetime import datetime
import random

class Mkdisk():
    def __init__(self):
        self.size = 0
        self.path = ""
        self.fit = ""
        self.unit = ""
        self.mbr = Mbr()
    
    #Setters
    #Definir el tamaño
    def set_size(self, size):
        if(self.unit == 'K'):
            size = size * 1024
        elif(self.unit == 'M'):
            size = size * 1024 * 1024
        else:
            return False
        self.size = size
        return True
    #Definir el path 
    def set_path(self, path):
        self.path = path
        return True
    #Definir el fit
    def set_fit(self, fit):
        if fit == None:
            self.fit = "FF"
            return True
        elif fit.lower() == 'bf' or 'ff' or 'wf' :
            self.fit = fit.upper()
            return True
        return False
    #Definir el unit
    def set_unit(self, unit): 
        if unit == None:
            self.unit = "M"
            return True  
        elif unit.lower() == 'k' or 'm' :
            self.unit = unit.upper()
            return True
        return False
    #Definir el MKDISK
    def set_mkdisk(self, size, path, fit, unit): 
        if(not self.set_unit(unit)): return False
        if(not self.set_size(int(size))): return False
        if(not self.set_fit(fit)): return False
        if(not self.set_path(path)): return False
        return True
    
    
    # Verificar si existe el path    
    def existe_path(self):
        return os.path.exists(self.path)
    
      
    #Crear un disco
    def crear_disco(self):
        try:
            if not self.existe_path():
                #Crear MBR despues de verificar los datos del comando                                
                fecha_actual = datetime.now().strftime("%d/%m/%Y")
                self.mbr.set_mbr(self.size,fecha_actual,random.randint(1,99999999),self.fit)
                    
                if(Fcreate_file(self.path)) : exit()
                Crrfile = open(self.path, "rb+") 
                Winit_size(Crrfile, self.size)   
                Fwrite_displacement(Crrfile,0,self.mbr)
                Crrfile.close()
            else:
                print("El path ya existe")
        except Exception as e:
            print("Error al crear el disco")
    def leer_disco(self):
        try:
            if self.existe_path():
                Crrfile = open(self.path, "rb+")                
                Fread_displacement(Crrfile,0,self.mbr)
                self.mbr.display_info()
                Crrfile.close() 
            else:
                print("El path no existe")
        except Exception as e:
            print("Error al leer el disco")
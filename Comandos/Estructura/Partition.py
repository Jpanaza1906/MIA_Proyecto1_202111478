import ctypes
import struct
from .Load import *
from .Ebr import *

const = "1s 1s 1s i i 16s"

class Partition(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('part_status', ctypes.c_char), # 1 byte
        ('part_type', ctypes.c_char), # 1 byte
        ('part_fit', ctypes.c_char), # 1 byte
        ('part_start', ctypes.c_int), # 4 bytes
        ('part_size', ctypes.c_int), # 4 bytes
        ('part_name', ctypes.c_char * 16) # 16 bytes
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.part_status = b'\0'
        self.part_type = b'\0'
        self.part_fit = b'\0'
        self.part_start = -1
        self.part_size = -1
        self.part_name = b'\0'*16
    
    #Setters--------------------------------------------------------------------
    
    def set_part_status(self, status): # Definir el status
        self.part_status = coding_str(status, 1)
    
    def set_part_type(self, type): # Definir el tipo
        self.part_type = coding_str(type, 1)
    
    def set_part_fit(self, fit): # Definir el fit
        self.part_fit = coding_str(fit, 1)
    
    def set_part_start(self, start): # Definir el inicio
        self.part_start = start
    
    def set_part_size(self, size): # Definir el tamaño
        self.part_size = size
    
    def set_part_name(self, name): # Definir el nombre
        self.part_name = coding_str(name, 16)
    
    #Definir la particion--------------------------------------------------------
    
    def set_partition(self, status, type, fit, start, size, name):
        self.set_part_status(status)
        self.set_part_type(type)
        self.set_part_fit(fit)
        self.set_part_start(start)
        self.set_part_size(size)
        self.set_part_name(name)
    
    #Getters--------------------------------------------------------------------
    
    def get_const(self): # Obtener la constante
        return const
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self): # Serializar la particion
        return struct.pack(
            const,
            self.part_status,
            self.part_type,
            self.part_fit,
            self.part_start,
            self.part_size,
            self.part_name
        )
    
    #Deserialize----------------------------------------------------------------
    
    def doDeseralize(self, data): # Deserializar la particion
        unpacked = struct.unpack(const, data)
        self.part_status = unpacked[0]
        self.part_type = unpacked[1]
        self.part_fit = unpacked[2]
        self.part_start = unpacked[3]
        self.part_size = unpacked[4]
        self.part_name = unpacked[5]
        
    
    #Display--------------------------------------------------------------------
    
    def display_info(self):
        print("===================PARTITION INFO===================")
        print(f"Status: {self.part_status.decode()}")
        print(f"Type: {self.part_type.decode()}")
        print(f"Fit: {self.part_fit.decode()}")
        print(f"Start: {self.part_start}")
        print(f"Size: {self.part_size}")
        print(f"Name: {self.part_name.decode()}")       
        print("----------------------------------------------------")
    
    
    #Generar reporte tabla de particiones---------------------------------------
    
    def generar_reporte(self,path):
        reporte = ""
        #Se agrega el tipo de la particion
        reporte += "<tr><td colspan='2' bgcolor='#5004a4'><font color='white'><b>Particion</b></font></td></tr>"
        #Se agrega el status de la particion
        reporte += "<tr><td>Status</td><td>" + self.part_status.decode() + "</td></tr>"
        #Se agrega el tipo de la particion
        reporte += "<tr><td bgcolor='#d7c7e9'>Tipo</td><td bgcolor='#d7c7e9'>" + self.part_type.decode() + "</td></tr>"
        #Se agrega el fit de la particion
        reporte += "<tr><td>Fit</td><td>" + self.part_fit.decode() + "</td></tr>"
        #Se agrega el inicio de la particion
        reporte += "<tr><td bgcolor='#d7c7e9'>Inicio</td><td bgcolor='#d7c7e9'>" + str(self.part_start) + "</td></tr>"
        #Se agrega el tamaño de la particion
        reporte += "<tr><td >Tamaño</td><td>" + str(self.part_size) + "</td></tr>"
        #Se agrega el nombre de la particion
        reporte += "<tr><td bgcolor='#d7c7e9'>Nombre</td><td bgcolor='#d7c7e9'>" + self.part_name.decode() + "</td></tr>"
        
        #Si es una particion extendida se agrega el reporte de las particiones logicas
        if self.part_type.decode().lower() == 'e':
            #se abre el archivo donde comienza la particion extendida
            ebr_file = open(path, "rb+")
            #Se lee el ebr
            startp = self.part_start
            while (startp != -1):
                ebr = Ebr()
                Fread_displacement(ebr_file, startp, ebr)
                reporte += ebr.generar_reporte(path)
                startp = ebr.part_next
            #Se cierra el archivo
            ebr_file.close()
            
        return reporte
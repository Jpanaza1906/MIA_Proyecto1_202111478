import ctypes
import struct
from .Load import *

const = "1s 1s I I I 16s"

class Ebr(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('part_status', ctypes.c_char), # 1 byte
        ('part_fit', ctypes.c_char), # 1 byte
        ('part_start', ctypes.c_int), # 4 bytes
        ('part_size', ctypes.c_int), # 4 bytes
        ('part_next', ctypes.c_int), # 4 bytes
        ('part_name', ctypes.c_char * 16) # 16 bytes
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.part_status = b'\0'
        self.part_fit = b'\0'
        self.part_start = 0
        self.part_size = 0
        self.part_next = 0
        self.part_name = b'\0'*16
        
    #Setters--------------------------------------------------------------------
    
    def set_part_status(self, status): # Definir el status
        self.part_status = coding_str(status, 1)
        
    def set_part_fit(self, fit): # Definir el fit
        self.part_fit = coding_str(fit, 1)
        
    def set_part_start(self, start): # Definir el inicio
        self.part_start = start
        
    def set_part_size(self, size): # Definir el tamaño
        self.part_size = size
        
    def set_part_next(self, next): # Definir el siguiente
        self.part_next = next
    
    def set_part_name(self, name): # Definir el nombre
        self.part_name = coding_str(name, 16)
        
    #Definir el EBR-------------------------------------------------------------
    
    def set_ebr(self, status, fit, start, size, next, name):
        self.set_part_status(status)
        self.set_part_fit(fit)
        self.set_part_start(start)
        self.set_part_size(size)
        self.set_part_next(next)
        self.set_part_name(name)
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self): # Obtener la constante
        return const
    
    def get_logic_partition(self, file, displacement): # Obtener la particion logica
        lista_ebr = []
        while True:
            ebr = Ebr()
            Fread_displacement(file, displacement, ebr)            
            lista_ebr.append(ebr)
            if ebr.part_next == 0:
                break
            displacement = ebr.part_next
        return lista_ebr
        
    def get_freespace(self, lista_ebr, tamaño_p): # Obtener el espacio libre
        lista_free = []
        for ebr in lista_ebr:
            if(ebr.part_next == 0):
                tamaño_entre = tamaño_p - (ebr.part_start + ebr.part_size)
            else: tamaño_entre = ebr.part_next - (ebr.part_start + ebr.part_size)
            lista_free.append(tamaño_entre)
        return lista_free
            
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self): # Serializar el EBR
        return struct.pack(
            const,
            self.part_status,
            self.part_fit,
            self.part_start,
            self.part_size,
            self.part_next,
            self.part_name
        )
    
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data): # Deserializar el EBR
        unpacked = struct.unpack(const, data)
        self.part_status = unpacked[0]
        self.part_fit = unpacked[1]
        self.part_start = unpacked[2]
        self.part_size = unpacked[3]
        self.part_next = unpacked[4]
        self.part_name = unpacked[5]
        
        
        
    #Display--------------------------------------------------------------------
    
    def display_info(self):
        print(f"Status: {self.part_status.decode()}")
        print(f"Fit: {self.part_fit.decode()}")
        print(f"Start: {self.part_start}")
        print(f"Size: {self.part_size}")
        print(f"Next: {self.part_next}")
        print(f"Name: {self.part_name.decode()}")
        print("")
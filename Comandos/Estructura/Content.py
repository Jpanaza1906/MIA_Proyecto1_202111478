import ctypes
import struct
from .Load import *

const = "12s I"

class Content(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('b_name', ctypes.c_char * 12),
        ('b_inodo', ctypes.c_int)
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.b_name = b'\0'*12
        self.b_inodo = 0
        
    #Setters--------------------------------------------------------------------
    
    def set_name(self, name): # Definir el nombre
        self.b_name = coding_str(name, 12)
        
    def set_inodo(self, inodo): # Definir apuntador inodo
        self.b_inodo = inodo
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self):
        return const
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self):
        return struct.pack(
            const,
            self.b_name,
            self.b_inodo
        )
        
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data):
        unpacked = struct.unpack(const, data)
        self.b_name = unpacked[0]
        self.b_inodo = unpacked[1]
        
    #Display_info---------------------------------------------------------------
    
    def display_info(self):
        print("Nombre: ", self.b_name)
        print("Inodo: ", self.b_inodo)
        print("--------------------------------------------------")
    
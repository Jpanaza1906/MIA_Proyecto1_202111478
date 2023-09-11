import ctypes
import struct
from .Load import *

const = "64s"

class File_block(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('b_content', ctypes.c_char * 64)
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.b_content = b'\0'*64
        
    #Setters--------------------------------------------------------------------
    
    def set_b_content(self, content): # Definir el contenido
        self.b_content = coding_str(content, 64)
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self):
        return const
    
    #Serializer-----------------------------------------------------------------
    
    def doSerialize(self):
        return struct.pack(
            const, 
            self.b_content
        )
        
    #Deserializer---------------------------------------------------------------
    
    def doDeserialize(self, data):
        self.b_content = struct.unpack(const, data)
        
    #Printer--------------------------------------------------------------------
    
    def display_info(self):
        print("=====================File block=====================")
        print(f"b_content: {self.b_content.decode()}")
        print("----------------------------------------------------")
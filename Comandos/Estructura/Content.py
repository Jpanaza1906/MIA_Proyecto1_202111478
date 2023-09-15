import ctypes
import struct
from .Load import *

const = "i 12s"

class Content(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('b_inodo', ctypes.c_int),
        ('b_name', ctypes.c_char * 12)
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):        
        self.b_inodo = -1
        self.b_name = b'\0'*12
        
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
            self.b_inodo,
            self.b_name
        )
        
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data):
        unpacked = struct.unpack(const, data)        
        self.b_inodo = unpacked[0]
        self.b_name = unpacked[1]
        
    #Display_info---------------------------------------------------------------
    
    def display_info(self):
        print("===================CONTENT INFO===================")        
        print("Inodo: ", self.b_inodo)
        print("Nombre: ", self.b_name)
        print("--------------------------------------------------")
    
    #Reportes-------------------------------------------------------------------
    
    def generar_reporte(self):
        reporte = ""
        #Se crea la etiqueta
        reporte += "<tr><td>" + self.b_name.decode() + "</td><td>" + str(self.b_inodo) + "</td></tr>"
        return reporte
    
    def generarContentRep(self, n):
        reporte = ""
        #Se crea la etiqueta
        reporte += "<tr><td>" + self.b_name.decode() + "</td><td port=\"" + str(n+1) + "\">" + str(self.b_inodo) + "</td></tr>"
        
        return reporte
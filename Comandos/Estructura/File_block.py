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
        unpacked = struct.unpack(const, data)
        self.b_content = unpacked[0]
        
    #Printer--------------------------------------------------------------------
    
    def display_info(self):
        print("=====================File block=====================")
        print(f"b_content: {self.b_content.decode()}")
        print("----------------------------------------------------")
        
    #Reportes-------------------------------------------------------------------
    
    def generar_reporte(self, n):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Bloque" + str(n) + "[label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\" port=\"0\" >Bloque Archivo "+ str(n) +"</td></tr>"
        reporte += "<tr><td>Contenido</td><td>"+ self.b_content.decode() +"</td></tr>"
        reporte += "</table>>];"
        return reporte
    
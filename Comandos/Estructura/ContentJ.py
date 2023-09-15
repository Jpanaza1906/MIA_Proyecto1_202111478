import ctypes
import struct
from .Load import *

const = "10s 100s 100s 10s"

class ContentJ(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('operation', ctypes.c_char * 10),
        ('path', ctypes.c_char * 100),
        ('content', ctypes.c_char * 100),
        ('date', ctypes.c_char * 10)
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.operation = b'\0'*10
        self.path = b'\0'*100
        self.content = b'\0'*100
        self.date = b'\0'*10
    
    #Setters--------------------------------------------------------------------
    
    def set_operation(self, operation): # Definir la operacion
        self.operation = coding_str(operation, 10)
        
    def set_path(self, path): # Definir el path
        self.path = coding_str(path, 100)
        
    def set_content(self, content): # Definir el contenido
        self.content = coding_str(content, 100)
        
    def set_date(self, date): # Definir la fecha
        self.date = coding_str(date, 10)
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self):
        return const
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self):
        return struct.pack(
            const,            
            self.operation,
            self.path,
            self.content,
            self.date
        )
    
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data):
        unpacked = struct.unpack(const, data)        
        self.operation = unpacked[0]
        self.path = unpacked[1]
        self.content = unpacked[2]
        self.date = unpacked[3]
    
    #Display_info---------------------------------------------------------------
    
    def display_info(self):
        print("===================CONTENT JOURNALING INFO===================")        
        print("Operacion: ", self.operation)
        print("Path: ", self.path)
        print("Contenido: ", self.content)
        print("Fecha: ", self.date)
        print("--------------------------------------------------------------")
        
    #Reporte--------------------------------------------------------------------
    
    def generar_reporte(self):
        reporte = ""
        reporte += "<tr><td>" + self.operation.decode() + "</td>"
        reporte += "<td>" + self.path.decode() + "</td>"
        reporte += "<td>" + self.content.decode() + "</td>"
        reporte += "<td>" + self.date.decode() + "</td></tr>"
        
        return reporte
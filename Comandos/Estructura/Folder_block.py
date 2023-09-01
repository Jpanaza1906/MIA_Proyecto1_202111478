import struct
from Content import *

class Folder_block():
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.b_content = [Content() for _ in range(4)]
        
    #Setters--------------------------------------------------------------------
    
    def set_b_content(self, content, index): # Definir un contenido especifico
        self.b_content[index] = content
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self): # Serializar el bloque carpeta
        folder_data = b''
        for content in self.b_content:
            folder_data += content.doSerialize()
        return folder_data
    
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data): # Deserializar el bloque carpeta
        for i in range(4):
            content = Content()
            content.doDeserialize(data[i*16:(i+1)*16])
            self.b_content[i] = content
            
    #Display_info---------------------------------------------------------------
    
    def display_info(self): # Mostrar informacion del bloque carpeta
        i = 0
        for content in self.b_content:
            print(f"Contenido {i}:")
            content.display_info()
            i += 1
            
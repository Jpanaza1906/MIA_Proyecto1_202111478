import struct
from .Content import *

const = "64s"
class Folder_block():
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.b_content = [Content() for _ in range(4)]
        
    #Setters--------------------------------------------------------------------
    
    def set_b_content(self, index, content): # Definir un contenido especifico
        self.b_content[index] = content
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self): # Obtener la constante
        return const
    
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
        print("===================FOLDER BLOCK===================")
        for content in self.b_content:
            print(f"Contenido {i}:")
            content.display_info()
            i += 1
        print("--------------------------------------------------")
            
    #Reportes-------------------------------------------------------------------
    
    def generar_reporte(self, n):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Bloque" + str(n) + "[label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\">Bloque Carpeta "+ str(n) +"</td></tr>"
        reporte += "<tr><td>Nombre</td><td>Apuntador</td></tr>"
        for content in self.b_content:
            reporte += content.generar_reporte()
        reporte += "</table>>];"
        
        return reporte
    
    def generarBloqueRep(self, n):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Bloque" + str(n) + "[label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\" port=\"0\" >Bloque "+ str(n) +"</td></tr>"
        cont = 0
        for content in self.b_content:
            reporte += content.generarContentRep(cont)
            cont += 1
        reporte += "</table>>];"
        
        return reporte
    
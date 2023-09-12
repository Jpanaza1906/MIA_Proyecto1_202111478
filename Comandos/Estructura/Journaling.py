from .ContentJ import *

const = "6000s" # (10s 100s 100s 10s) * 50 = 6000s
class Journaling():
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.journaling = [ContentJ() for _ in range(50)]
        
    #Setters--------------------------------------------------------------------
    
    def set_journaling(self, index, content): # Definir un contenido especifico
        self.journaling[index] = content
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self): # Obtener la constante
        return const
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self): # Serializar el journaling
        journaling_data = b''
        for content in self.journaling:
            journaling_data += content.doSerialize()
        return journaling_data
    
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data): # Deserializar el journaling
        for i in range(50):
            content = ContentJ()
            content.doDeserialize(data[i*120:(i+1)*120])
            self.journaling[i] = content
            
    #Display_info---------------------------------------------------------------
    
    def display_info(self): # Mostrar informacion del journaling
        i = 0
        print("===================JOURNALING===================")
        for content in self.journaling:
            print(f"Contenido {i}:")
            content.display_info()
            i += 1
        print("--------------------------------------------------")
        
        

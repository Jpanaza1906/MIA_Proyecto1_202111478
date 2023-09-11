#COMANDO UNMOUNT
import os
from Global.Global import mounted_partitions

class Unmount():    
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.id = ''
    
    #Setters-------------------------------------------------------------------
    
    def set_id(self, id): #Definir el id
        if(id == None):
            print("\t Unmount>>> Falta el id de la particion")
            return False
        self.id = id
        return True
    
    #Definir el UNMOUNT--------------------------------------------------------
    
    def run(self, id):
        if(not self.set_id(id)): return False
        
        for data in mounted_partitions:
            if data[0] == id:
                mounted_partitions.remove(data)
                #Se confirma el unmount
                print("\t Unmount>>> Desmontando la particion: " + id)
                self.mostrar_particion()
                return True
        print("\t Unmount>>> No se encontro la particion: " + id)
        return False
        
    def mostrar_particion(self):
        print("\t\t Lista de particiones montadas:")    
        for data in mounted_partitions:
            print(f"\t\t id:{data[0]} path:{data[2]} name:{data[1].part_name.decode()}")
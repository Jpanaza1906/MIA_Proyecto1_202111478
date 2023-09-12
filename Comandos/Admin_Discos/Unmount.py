#COMANDO UNMOUNT
import os
from Global.Global import mounted_partitions
from Utilities.Utilities import *
class Unmount():    
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.id = ''
    
    #Setters-------------------------------------------------------------------
    
    def set_id(self, id): #Definir el id
        if(id == None):
            printError("\t Unmount>>> Falta el id de la particion\n")
            return False
        self.id = id
        return True
    
    #Definir el UNMOUNT--------------------------------------------------------
    
    def run(self, id):
        if(not self.set_id(id)): return False
        
        for data in mounted_partitions:
            if data.id == id:
                mounted_partitions.remove(data)
                #Se confirma el unmount
                printText("\t Unmount>>> Desmontando la particion: " + id + "\n")
                self.mostrar_particion()
                return True
        printError("\t Unmount>>> No se encontro la particion: " + id +"\n")
        return False
        
    def mostrar_particion(self):
        print("\t\t Lista de particiones montadas:")    
        for data in mounted_partitions:
            print(f"\t\t id:{data.id} path:{data.path} name:{data.partition.part_name.decode()}")
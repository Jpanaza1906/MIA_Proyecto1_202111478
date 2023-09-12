#COMANDO MOUNT
import os
from ..Estructura.Mbr import *
from ..Estructura.Ebr import *
from ..Estructura.Load  import *
from Global.Global import *
from Utilities.Utilities import *
class Mount():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.path = ''
        self.name = ''
        
    #Setters-------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if(not os.path.isfile(path)):
            printError("\t Mount>>> El disco no existe\n")
            return False
        if(not path.endswith('.dsk')):
            printError("\t Mount>>> El path no tiene la extension .dsk\n")
            return False
        #Se guarda el path
        self.path = path
        return True
    
    def set_name(self, name): #Definir el nombre
        if name == None:
            printError("\t Fdisk>>> Falta el nombre de la particion\n")
            return False
        self.name = name
        return True
    
    #Definir el MOUNT-------------------------------------------------------------------
    
    def run(self, path, name): #Ejecutar el comando
        if(not self.set_path(path)): return False
        if(not self.set_name(name)): return False
        
        if(self.montar_partition()): 
            return True
        return False
    
    #Montar una particion-------------------------------------------------------------------
    
    def montar_partition(self):
        try:
            #se crea el MBR temporal
            crr_mbr = Mbr()
            file = open(self.path, 'rb+')
            
            #Se lee el MBR
            Fread_displacement(file, 0, crr_mbr)
            
            #Se verifica si existe la particion con el mismo nombre
            existeP = False
            existePext = False
            particion_montar = None
            particion_extendida = None
            indexP_montar = 0
            
            for partition in crr_mbr.mbr_partition:
                if(partition.part_type.decode() == 'E'):
                    existePext = True
                    particion_extendida = partition
                if(partition.part_name.decode() == self.name):
                    existeP = True
                    particion_montar = partition
                    break
                indexP_montar += 1
            
            if(not existeP):
                if(not existePext):
                    printError(f"\t Mount>>> No existe una particion extendida\n")
                    return False                  
                        
                startp = particion_extendida.part_start
                ebr = Ebr()
                lista_ebr = ebr.get_logic_partition(file, startp)
                for cadaebr in lista_ebr:
                    if cadaebr.part_name.decode() == self.name:
                        particion_montar = cadaebr
                        break
                if particion_montar == None:
                    printError(f"\t Mount>>> No existe la particion: {self.name}\n")
                    return False
                
                #Se llama la funcion que agrega las particiones montadas a memoria                
                file.close()
                if(self.agregar_partition(particion_montar, True)):
                    return True
                return False
                
                #
            #Si es una particion primaria
            
            if(particion_montar.part_type.decode() == 'E'):
                printError(f"\t Mount>>> La particion:{self.name} es una particion extendida, se deben montar sus particiones lógicas.\n")
                return False
            
            #Se llama la funcion que agrega las particiones montadas a memoria            
            file.close()
            if(self.agregar_partition(particion_montar, False)):
                return True
            return False
                
        except Exception as e:
            printError(f"\t Mount>>> Ocurrio un error al montar la particion:{e}\n")
            return False
    #montar particion
    def agregar_partition(self, particion_montar, islogic):
        if(particion_montar.part_status.decode() == '0'):
                printError(f"\t Mount>>> La particion:{self.name} no esta formateada\n")
                return False
        if(particion_montar.part_size == -1):
            printError(f"\t Mount>>> La particion:{self.name} no esta formateada\n")
            return False
        #Se verifica si la particion ya esta montada
        for data in mounted_partitions:
            if(data.partition.part_name.decode() == particion_montar.part_name.decode()):
                printError(f"\t Mount>>> La particion:{self.name} ya esta montada\n")
                return False
        
        #Clave para guardar particion = CARNET.substring(6,8) + NUMERO_PARTICION + NOMBRE DISCO
        nombre_archivo = os.path.splitext(os.path.basename(self.path))[0]
        index = 1
        for data in mounted_partitions:
            if(data.path == self.path):
                index = int(data.id[2:3]) + 1
                    
        id = "78" + str(index) + nombre_archivo
        
        temp = MountedPartition(id, particion_montar, self.path, islogic, None)
        mounted_partitions.append(temp)
        printText(f"\t Mount>>> Se monto la particion:{self.name} con el id:{id}\n")
        #Se muestra la lista de particiones montadas
        self.mostrar_particion()
        
        return True
    
    def mostrar_particion(self):
        printInfo("\t\t Lista de particiones montadas:")    
        for data in mounted_partitions:
            printInfo(f"\t\t\t id:{data.id} path:{data.path} name:{data.partition.part_name.decode()}")
        print("")
        
        
    
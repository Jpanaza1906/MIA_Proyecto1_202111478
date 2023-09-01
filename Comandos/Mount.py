#COMANDO MOUNT
import os
from .Estructura.Mbr import *
from .Estructura.Ebr import *
from .Estructura.Load  import *
from Global.Global import mounted_partitions
class Mount():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.path = ''
        self.name = ''
        
    #Setters-------------------------------------------------------------------
    
    def set_path(self, path): #Definir el path
        if(not os.path.isfile(path)):
            print("\t Mount>>> El disco no existe")
            return False
        if(not path.endswith('.dsk')):
            print("\t Mount>>> El path no tiene la extension .dsk")
            return False
        #Se guarda el path
        self.path = path
        return True
    
    def set_name(self, name): #Definir el nombre
        if name == None:
            print("\t Fdisk>>> Falta el nombre de la particion")
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
                    print(f"\t Mount>>> No existe la particion: {self.name}")
                    return False
                startp = particion_extendida.part_start
                ebr = Ebr()
                lista_ebr = ebr.get_logic_partition(file, startp)
                for cadaebr in lista_ebr:
                    if cadaebr.part_name.decode() == self.name:
                        particion_montar = cadaebr
                        break
                if particion_montar == None:
                    print(f"\t Mount>>> No existe la particion: {self.name}")
                    return False
                
                #Se llama la funcion que agrega las particiones montadas a memoria                
                file.close()
                if(self.agregar_partition(particion_montar)):
                    return True
                return False
                
                #
            #Si es una particion primaria
            
            if(particion_montar.part_type.decode() == 'E'):
                print(f"\t Mount>>> La particion:{self.name} es una particion extendida, se deben montar sus particiones lógicas.")
                return False
            
            #Se llama la funcion que agrega las particiones montadas a memoria            
            file.close()
            if(self.agregar_partition(particion_montar)):
                return True
            return False
                
        except Exception as e:
            print(f"\t Mount>>> Ocurrio un error al montar la particion:{e}")
            return False
    #montar particion
    def agregar_partition(self, particion_montar):
        if(particion_montar.part_status.decode() == '0'):
                print(f"\t Mount>>> La particion:{self.name} no esta formateada")
                return False
        if(particion_montar.part_size == 0):
            print(f"\t Mount>>> La particion:{self.name} no esta formateada")
            return False
        #Se verifica si la particion ya esta montada
        for data in mounted_partitions:
            if(data[2] == particion_montar.part_name.decode()):
                print(f"\t Mount>>> La particion:{self.name} ya esta montada")
                return False
        
        #Clave para guardar particion = CARNET.substring(6,8) + NUMERO_PARTICION + NOMBRE DISCO
        nombre_archivo = os.path.splitext(os.path.basename(self.path))[0]
        index = 1
        for data in mounted_partitions:
            if(data[2] == self.path):
                index = int(data[0][2:3]) + 1
                    
        id = "78" + str(index) + nombre_archivo
            
        temp = [id, particion_montar, self.path]
        mounted_partitions.append(temp)
        print(f"\t Mount>>> Se monto la particion:{self.name} con el id:{id}")
        return True
        
        
    
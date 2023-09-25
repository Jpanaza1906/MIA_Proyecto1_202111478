import ctypes
import struct
from .Partition import *
from .Load import *

const = "i 10s i 1s"

class Mbr(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
     
    _fields_ = [
        ('mbr_tamano', ctypes.c_int), # 4 bytes
        ('mbr_fecha_creacion', ctypes.c_char * 10), # 10 bytes
        ('mbr_dsk_signature', ctypes.c_int), # 4 bytes
        ('dsk_fit', ctypes.c_char), # 1 byte
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.mbr_tamano = -1
        self.mbr_fecha_creacion = b'\0'*10
        self.mbr_dsk_signature = -1
        self.dsk_fit = b'\0'
        self.mbr_partition = [Partition() for _ in range(4)]
    
    #Setters--------------------------------------------------------------------
    
    def set_mbr_tamano(self, tamano): # Definir el tamaño
        self.mbr_tamano = tamano
    
    def set_mbr_fecha_creacion(self, fecha): # Definir la fecha
        self.mbr_fecha_creacion = coding_str(fecha, 10)
        
    def set_mbr_dsk_signature(self, signature): # Definir la firma
        self.mbr_dsk_signature = signature
    
    def set_dsk_fit(self, fit): # Definir el fit
        self.dsk_fit = coding_str(fit, 1)
        
    def set_mbr_partition(self, partition, index): # Definir una particion especifica
        self.mbr_partition[index] = partition
    
    #Definir el MBR----------------------------------------------------------------
    
    def set_mbr(self, tamano, fecha, signature, fit):
        self.set_mbr_tamano(tamano)
        self.set_mbr_fecha_creacion(fecha)
        self.set_mbr_dsk_signature(signature)
        self.set_dsk_fit(fit)
    
    #Getters--------------------------------------------------------------------
    
    def get_const(self): # Obtener la constante
        return const
    
    def exist_partition(self, name): # Verificar si existe una particion
        for partition in self.mbr_partition:
            if partition.part_name.decode() == name:
                return True
    
    def get_partition(self, name): # Obtener una particion
        for partition in self.mbr_partition:
            if partition.part_name.decode() == name:
                return partition
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self): # Serializar el MBR
        mbr_data = struct.pack(
            const,
            self.mbr_tamano,
            self.mbr_fecha_creacion,
            self.mbr_dsk_signature,
            self.dsk_fit
        )
        return mbr_data + self.doSerializePartitions()
    
    def doSerializePartitions(self): # Serializar las particiones
        partitions = b''
        for partition in self.mbr_partition:
            partitions += partition.doSerialize()
        return partitions
    
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data): # Deserializar el MBR
        #Obtener el tamaño del MBR y Particion
        sizeMbr = struct.calcsize(const)
        
        #Deserializar el MBR
        mbr_data = data[:sizeMbr]
        unpacked = struct.unpack(const, mbr_data)
        self.mbr_tamano = unpacked[0]
        self.mbr_fecha_creacion = unpacked[1]
        self.mbr_dsk_signature = unpacked[2]
        self.dsk_fit = unpacked[3]
        
        #Llamar funcion para Deserializar las particiones
        self.doDeserializePartitions(data[sizeMbr:])
        
    def doDeserializePartitions(self, data): # Deserializar las particiones
        #Obtener el tamaño de la particion
        sizePartition = struct.calcsize(self.mbr_partition[0].get_const())
        
        #Deserializar las particiones
        for i in range(4):            
            partition_data = data[i*sizePartition:(i+1)*sizePartition]
            self.mbr_partition[i].doDeseralize(partition_data)
        
    #Display--------------------------------------------------------------------
    
    def display_info(self):
        print("========================MBR============================")
        print(f"Size: {self.mbr_tamano}")
        print(f"Date: {self.mbr_fecha_creacion.decode()}")
        print(f"Signature: {self.mbr_dsk_signature}")
        print(f"Fit: {self.dsk_fit.decode()}")
        print("")
        print("==================== Partitions: =======================\n")
        cont = 0
        for partition in self.mbr_partition:
            print("Partition ", cont," :")
            partition.display_info()
            cont += 1
        print("------------------------------------------------------\n")
    
    def generar_reporte(self, path):
        reporte = ""
        #Se agrega el tama;o del disco
        reporte += "<tr><td>Tamaño</td><td>" + str(self.mbr_tamano) + "</td></tr>"
        #Se agrega la fecha de creacion
        reporte += "<tr><td  bgcolor=\"#d7c7e9\">Fecha de Creacion</td><td bgcolor=\"#d7c7e9\">" + self.mbr_fecha_creacion.decode() + "</td></tr>"
        #Se agrega la firma
        reporte += "<tr><td>Firma</td><td>" + str(self.mbr_dsk_signature) + "</td></tr>"
        
        #Se agregan las patriciones
        for partition in self.mbr_partition:
            reporte += partition.generar_reporte(path)
        
        return reporte
    
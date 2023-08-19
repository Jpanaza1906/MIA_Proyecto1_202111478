import ctypes
import struct
from .Utilities import * 
from .Partition import *

const = "I 10s I 1s"
class Mbr(ctypes.Structure):
    _fields_ = [
        ('mbr_tamano', ctypes.c_int), # 4 bytes
        ('mbr_fecha_creacion', ctypes.c_char * 10), # 10 bytes
        ('mbr_dsk_signature', ctypes.c_int), # 4 bytes
        ('dsk_fit', ctypes.c_char), # 1 byte
    ]
    #Constructor
    def __init__(self):
        self.mbr_tamano = 0
        self.mbr_fecha_creacion = b'\x00'*10
        self.mbr_dsk_signature = 0
        self.dsk_fit = b'\x00'
        self.mbr_partition = [Partition() for _ in range(4)]
    
    #Setters
    def set_mbr_tamano(self, tamano):
        self.mbr_tamano = tamano
    
    def set_mbr_fecha_creacion(self, fecha):
        self.mbr_fecha_creacion = coding_str(fecha, 10)
        
    def set_mbr_dsk_signature(self, signature):
        self.mbr_dsk_signature = signature
    
    def set_dsk_fit(self, fit):
        self.dsk_fit = coding_str(fit, 1)
        
    def set_mbr_partition(self, partition, index):
        self.mbr_partition[index] = partition
    
    def set_mbr(self, tamano, fecha, signature, fit):
        self.set_mbr_tamano(tamano)
        self.set_mbr_fecha_creacion(fecha)
        self.set_mbr_dsk_signature(signature)
        self.set_dsk_fit(fit)
    
    #Get const
    def get_const(self):
        return const
    
    #Serialize
    
    def doSerialize(self):
        mbr_data = struct.pack(
            const,
            self.mbr_tamano,
            self.mbr_fecha_creacion,
            self.mbr_dsk_signature,
            self.dsk_fit
        )
        return mbr_data + self.doSerializePartitions()
    
    def doSerializePartitions(self):
        partitions = b''
        for partition in self.mbr_partition:
            partitions += partition.doSerialize()
        return partitions
    
    def doDeserialize(self, data):
        #Obtener el tamaño del MBR y Particion
        sizeMbr = struct.calcsize(const)
        sizePartition = struct.calcsize(self.mbr_partition[0].get_const())
        
        #Deserializar el MBR
        mbr_data = data[:sizeMbr]
        unpacked = struct.unpack(const, mbr_data)
        self.mbr_tamano = unpacked[0]
        self.mbr_fecha_creacion = unpacked[1]
        self.mbr_dsk_signature = unpacked[2]
        self.dsk_fit = unpacked[3]
        
        #Llamar funcion para Deserializar las particiones
        self.doDeserializePartitions(data[sizePartition:])
    
    def doDeserializePartitions(self, data):
        #Obtener el tamaño de la particion
        #sizePartition = struct.calcsize(self.mbr_partition[0].get_const())
        #sizePartition = len(self.mbr_partition[0].doSerialize())
        
        #Deserializar las particiones
        for i in range(4):            
            sizePartition = len(self.mbr_partition[i].doSerialize())
            partition_data = data[i*sizePartition:(i+1)*sizePartition]
            self.mbr_partition[i].doDeseralize(partition_data)
        
        
    def display_info(self):
        print("MBR")
        print(f"Size: {self.mbr_tamano}")
        print(f"Date: {self.mbr_fecha_creacion}")
        print(f"Signature: {self.mbr_dsk_signature}")
        print(f"Fit: {self.dsk_fit}")
        print("")
        print("Partitions:")
        cont = 0
        for partition in self.mbr_partition:
            print("Partition ", cont," :")
            partition.display_info()
            cont += 1
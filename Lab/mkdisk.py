import random
import time
from Lab.estructuras import Mbr,Partition
import struct
import os
class MkDisk:
    def __init__(self):
        self.size = 0
        self.path = ''
        self.fit = ''
        self.unit = ''
    
    #Driver para mandar la informacion validadd
    def driver(self, disco):
        complete_path = disco.path + disco.name
        mbr_partition = [Partition() for _ in range(4)]
        
        if self.existPath(disco.path):
            pass
        else:
            self.createPath(disco.path)
    
    #verificar si existe el path
    def existPath(self,path):
        return os.path.isdir(path)
    
    #crear path en caso que no exista la ruta
    def createPath(self,path):
        try:
            os.makedirs(path, exist_ok=True)
            print("Ruta creada con exito.")
        except OSError as e:
            pass
        
    
    #crear un disco
    def create(self, disco):
        try:
            with open(disco.path, "wb") as file:
                buffer = bytearray(1024)
                if disco.unit.lower == 'k':
                    for _ in range(disco.size):
                        file.write(buffer)
                    pass
                else:
                    for _ in range(disco.size * 1024):
                        file.write(buffer)
            size = disco.size * 1024 if not disco.unit or disco.unit.lower == 'm' else disco.size*1024*1024
            
            #crear el MBR
            mbr_disco = Mbr()
            
            #asignar valor al MBR segun el MKDISK
            mbr_disco.dsk_fit = 'F'
            mbr_disco.mbr_fecha_creacion = int(time.time())
            mbr_disco.mbr_dsk_signature = random.randint(1,99999999)
            mbr_disco.mbr_tamano = size
            
            
            #crear particiones
            part_vacia = Partition()
            part_vacia.part_status = '0'
            part_vacia.part_type = '-'
            part_vacia.part_fit = '-'
            part_vacia.part_start = -1
            part_vacia.part_size = -1
            part_vacia.part_name = b'0' * 16
            
            #asginar particion
            mbr_disco.mbr_partition = [part_vacia]*4
            
            with open(disco.path, "rb+") as file:
                file.write(struct.pack('',mbr_disco.mbr_tamano,
                                       mbr_disco.mbr_fecha_creacion,
                                       mbr_disco.mbr_dsk_signature,
                                       mbr_disco.dsk_fit.encode(),
                                       mbr_disco.mbr_partition[0],
                                       mbr_disco.mbr_partition[1],
                                       mbr_disco.mbr_partition[2],
                                       mbr_disco.mbr_partition[3]
                                       ))
            
        except OSError as e:
            pass
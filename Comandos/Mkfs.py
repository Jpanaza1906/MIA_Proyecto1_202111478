#COMANDO MKFS
import datetime
import math
import os
import struct

from .Estructura.Super_block import *
from .Estructura.Table_inode import *
from .Estructura.File_block import *
from .Estructura.Load import *
from Global.Global import *
from .Estructura.Ext import *

class Mkfs():
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.id = ''
        self.type = ''
        self.fs = ''
        
    #Setters-------------------------------------------------------------------
    
    def set_id(self, id): #Definir el id
        if(id == None):
            print("\t Mkfs>>> Falta un parametro obligatorio")
            return False
        #Se guarda el id
        self.id = id
        return True
    
    def set_type(self, type): #Definir el type
        if(type == None):
            self.type = 'full'
            return True
        elif(type.lower() != 'full'):
            print("\t Mkfs>>> El type no es valido")
            return False
        #Se guarda el type
        self.type = type
        return True
    
    def set_fs(self, fs): #Definir el fs
        if(fs == None):
            self.fs = '2fs'
            return True
        elif(fs.lower() != '2fs' or '3fs'):
            print("\t Mkfs>>> El fs no es valido")
            return False
        #Se guarda el fs
        self.fs = fs
        return True
    
    #Definir el MKFS-----------------------------------------------------------
    
    def run(self, id, type, fs):
        if(not self.set_id(id)): return False
        if(not self.set_type(type)): return False
        if(not self.set_fs(fs)): return False
        
        #Se formatea la partcion
        if(self.formatear_particion()):
            print("\t Mkfs>>> Se formateo la particion con exito")
            return True
        return False
    def formatear_particion(self):
        mPartition = None
        for partition in mounted_partitions:
            if(partition.id == self.id):
                mPartition = partition
                break
        if(mPartition == None):
            print("\t Mkfs>>> No se encontro la particion")
            return False
        
        #Se formatea la particion
        numerator = mPartition[1].part_size - struct.calcsize(Super_block().get_const())
        denominador = 4 + struct.calcsize(Table_inode().get_const()) + 3 * struct.calcsize(File_block().get_const())
        temp = 0 if (self.fs == '2fs') else 0
        denominador += temp
        n = math.floor(numerator / denominador)
        
        #creando super bloque
        new_super_block = Super_block()
        new_super_block.set_s_inodes_count(0)
        new_super_block.set_s_blocks_count(0)
        
        new_super_block.set_s_free_blocks_count(3 * n)
        new_super_block.set_free_inodes_count(n)
        
        date = datetime.now().strftime("%d/%m/%Y")
        new_super_block.set_s_mtime(date)
        new_super_block.set_s_umtime(date)
        new_super_block.mount_count = 1
        #Creando super bloque
        if(self.fs == '2fs'):
            create_ext2(n, mPartition, new_super_block, date)
        elif(self.fs == '3fs'):
            pass
        
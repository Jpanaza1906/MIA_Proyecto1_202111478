import ctypes
import struct
from .Load import *

const = "I I I 10s 10s 10s 15I 1s 9s"

class Table_inode(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('i_uid', ctypes.c_int),
        ('i_gid', ctypes.c_int),
        ('i_size', ctypes.c_int),
        ('i_atime', ctypes.c_char * 10),
        ('i_ctime', ctypes.c_char * 10),
        ('i_mtime', ctypes.c_char * 10),
        ('i_block', ctypes.c_int * 15),
        ('i_type', ctypes.c_char),
        ('i_perm', ctypes.c_char * 9)
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.i_uid = 0
        self.i_gid = 0
        self.i_size = 0
        self.i_atime = b'\0'*10
        self.i_ctime = b'\0'*10
        self.i_mtime = b'\0'*10
        self.i_block = (ctypes.c_int * 15)(*[0] * 15)
        self.i_type = b'\0'
        self.i_perm = b'\0'*9
        
    #Setters--------------------------------------------------------------------
    
    def set_i_uid(self, uid): # Definir el uid
        self.i_uid = uid
        
    def set_i_gid(self, gid): # Definir el gid
        self.i_gid = gid
        
    def set_i_size(self, size): # Definir el tamaño
        self.i_size = size
        
    def set_i_atime(self, atime): # Definir el atime
        self.i_atime = coding_str(atime, 10)
        
    def set_i_ctime(self, ctime): # Definir el ctime
        self.i_ctime = coding_str(ctime, 10)
        
    def set_i_mtime(self, mtime): # Definir el mtime
        self.i_mtime = coding_str(mtime, 10)
        
    def set_i_block(self, block, index): # Definir un bloque especifico
        self.i_block[index] = block
        
    def set_i_type(self, type): # Definir el tipo
        self.i_type = coding_str(type, 1)
        
    def set_i_perm(self, perm): # Definir los permisos
        self.i_perm = coding_str(perm, 9)
        
    #Getters--------------------------------------------------------------------
    
    def get_const(self):
        return const
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self):
        return struct.pack(
            const,
            self.i_uid,
            self.i_gid,
            self.i_size,
            self.i_atime,
            self.i_ctime,
            self.i_mtime,
            *self.i_block,
            self.i_type,
            self.i_perm
        )
        
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data):
        unpacked_data = struct.unpack(const, data)
        (
            self.i_uid,
            self.i_gid,
            self.i_size,
            self.i_atime,
            self.i_ctime,
            self.i_mtime
        ) = unpacked_data[:6]
        
        self.i_block = (ctypes.c_int * 15)(*unpacked_data[6:21])
        
        (
            self.i_type,
            self.i_perm
        ) = unpacked_data[21:]
        
    #Reportes-------------------------------------------------------------------
    
    def display_info(self):
        print("Table Inode")
        print(f"i_uid: {self.i_uid}")
        print(f"i_gid: {self.i_gid}")
        print(f"i_size: {self.i_size}")
        print(f"i_atime: {self.i_atime.decode()}")
        print(f"i_ctime: {self.i_ctime.decode()}")
        print(f"i_mtime: {self.i_mtime.decode()}")
        print(f"i_block: {list(self.i_block)}")
        print(f"i_type: {self.i_type.decode()}")
        print(f"i_perm: {self.i_perm.decode()}")
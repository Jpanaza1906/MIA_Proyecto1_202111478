import ctypes
import struct
from .Load import *

const = "i i i i i 10s 10s i H i i i i i i i i"

class Super_block(ctypes.Structure):
    
    #Tipos----------------------------------------------------------------------
    
    _fields_ = [
        ('filesystem_type', ctypes.c_int),
        ('inodes_count', ctypes.c_int),
        ('blocks_count', ctypes.c_int),
        ('free_blocks_count', ctypes.c_int),
        ('free_inodes_count', ctypes.c_int),
        ('mount_time', ctypes.c_char * 10),
        ('unmount_time', ctypes.c_char * 10),
        ('mount_count', ctypes.c_int),
        ('magic', ctypes.c_uint16),
        ('inodes_size', ctypes.c_int),
        ('block_size', ctypes.c_int),
        ('first_inode', ctypes.c_int),
        ('first_block', ctypes.c_int),
        ('bm_inode_start', ctypes.c_int),
        ('bm_block_start', ctypes.c_int),
        ('inode_start', ctypes.c_int),
        ('block_start', ctypes.c_int),
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.filesystem_type = -1
        self.inodes_count = -1
        self.blocks_count = -1
        self.free_blocks_count = -1
        self.free_inodes_count = -1
        self.mount_time = b'\0'*10
        self.unmount_time = b'\0'*10
        self.mount_count = -1
        self.magic = 0xEF53
        self.inodes_size = -1
        self.block_size = -1
        self.first_inode = -1
        self.first_block = -1
        self.bm_inode_start = -1
        self.bm_block_start = -1
        self.inode_start = -1
        self.block_start = -1
    
    #Setters--------------------------------------------------------------------
    
    def set_filesystem_type(self, type): # Definir el tipo
        self.filesystem_type = type
    
    def set_inodes_count(self, count): # Definir el numero de inodos
        self.inodes_count = count
        
    def set_blocks_count(self, count): # Definir el numero de bloques
        self.blocks_count = count
        
    def set_free_blocks_count(self, count): # Definir el numero de bloques libres
        self.free_blocks_count = count
        
    def set_free_inodes_count(self, count): # Definir el numero de inodos libres
        self.free_inodes_count = count
        
    def set_mount_time(self, time): # Definir el tiempo de montaje
        self.mount_time = coding_str(time, 10)
        
    def set_unmount_time(self, time): # Definir el tiempo de desmontaje
        self.unmount_time = coding_str(time, 10)
        
    def set_mount_count(self, count): # Definir el numero de montajes
        self.mount_count = count
        
    def set_magic(self, magic): # Definir la firma
        self.magic = magic
        
    def set_inodes_size(self, size): # Definir el tamaño de los inodos
        self.inodes_size = size
        
    def set_block_size(self, size): # Definir el tamaño de los bloques
        self.block_size = size
        
    def set_first_inode(self, inode): # Definir el primer inodo
        self.first_inode = inode
        
    def set_first_block(self, block): # Definir el primer bloque
        self.first_block = block
        
    def set_bm_inode_start(self, start): # Definir el inicio del bitmap de inodos
        self.bm_inode_start = start
        
    def set_bm_block_start(self, start): # Definir el inicio del bitmap de bloques
        self.bm_block_start = start
        
    def set_inode_start(self, start): # Definir el inicio de los inodos
        self.inode_start = start
        
    def set_block_start(self, start): # Definir el inicio de los bloques
        self.block_start = start
        
    
    #Getters--------------------------------------------------------------------
    
    def get_const(self): # Obtener la constante
        return const
    
    #Methods
    
    def reduce_free_block(self):
        self.free_blocks_count -= 1
    
    def reduce_free_inode(self):
        self.free_inodes_count -= 1
    
    #Serialize------------------------------------------------------------------
    
    def doSerialize(self): # Serializar el super bloque
        return struct.pack(
            const,
            self.filesystem_type,
            self.inodes_count,
            self.blocks_count,
            self.free_blocks_count,
            self.free_inodes_count,
            self.mount_time,
            self.unmount_time,
            self.mount_count,
            self.magic,
            self.inodes_size,
            self.block_size,
            self.first_inode,
            self.first_block,
            self.bm_inode_start,
            self.bm_block_start,
            self.inode_start,
            self.block_start
        )
    
    #Deserialize----------------------------------------------------------------
    
    def doDeserialize(self, data): # Deserializar el super bloque
        self.filesystem_type,
        self.inodes_count,
        self.blocks_count,
        self.free_blocks_count,
        self.free_inodes_count,
        self.mount_time,
        self.unmount_time,
        self.mount_count,
        self.magic,
        self.inodes_size,
        self.block_size,
        self.first_inode,
        self.first_block,
        self.bm_inode_start,
        self.bm_block_start,
        self.inode_start,
        self.block_start = struct.unpack(const, data)
        
    #Reportes-------------------------------------------------------------------
    
    def display_info(self):
        print("=====================Super Block=====================")
        print(f"Filesystem type: {self.filesystem_type}")
        print(f"Inodes count: {self.inodes_count}")
        print(f"Blocks count: {self.blocks_count}")
        print(f"Free blocks count: {self.free_blocks_count}")
        print(f"Free inodes count: {self.free_inodes_count}")
        print(f"Mount time: {self.mount_time.decode()}")
        print(f"Unmount time: {self.unmount_time.decode()}")
        print(f"Mount count: {self.mount_count}")
        print(f"Magic: {hex(self.magic)}")
        print(f"Inodes size: {self.inodes_size}")
        print(f"Block size: {self.block_size}")
        print(f"First inode: {self.first_inode}")
        print(f"First block: {self.first_block}")
        print(f"Bitmap inode start: {self.bm_inode_start}")
        print(f"Bitmap block start: {self.bm_block_start}")
        print(f"Inode start: {self.inode_start}")
        print(f"Block start: {self.block_start}")
        print("-----------------------------------------------------")
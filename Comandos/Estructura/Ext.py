import struct
from Super_block import *
from Table_inode import *
from File_block import *
from Load import *
#FUNCION PARA CREAR EL EXT2

def create_ext2(n, mPartition, new_super_block, date):
    print("Creando EXT2")
    new_super_block = Super_block()
    #Se coloca el tipo de sistema de archivos
    new_super_block.set_filesystem_type(2)
    
    #Se coloca donde comienza el bitmap de inodos
    new_super_block.set_bm_inode_start(mPartition[1].part_start + struct.calcsize(Super_block().get_const()))
    
    #Se coloca donde comienza el bitmap de bloques
    new_super_block.set_bm_block_start(new_super_block.bm_inode_start + n)
    
    #Se coloca donde comienzan los inodos
    new_super_block.set_inode_start(new_super_block.bm_block_start + 3 * n)
    
    #Se coloca donde comienzan los bloques
    new_super_block.set_block_start(new_super_block.inode_start + n * struct.calcsize(Table_inode().get_const()))
    
    #Se actualizan los valores del superbloque
    #Posteriormente se debe crear un inodo 0
    new_super_block.reduce_free_inode()
    
    #Posteriormente se debe crear un bloque de carpetas
    new_super_block.reduce_free_block()
    
    #Posteriormente se debe crear un inodo 1
    new_super_block.reduce_free_inode()
    
    #Posteriormente se debe crear un bloque de archivos
    new_super_block.reduce_free_block()
    
    Crrfile = open(mPartition[2], 'rb+')
    
    
    Fwrite_displacement(Crrfile, mPartition[1].part_start, new_super_block)
    
    #Se llenan las estructuras del ext2
    
    #Se crea un inodo 0
    
    zero = '0'
    #Se llena el bitmap de inodos
    for i in range(n):
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_inode_start + i, zero)
    
    #Se llena el bitmap de bloques
    for i in range(3 * n):
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_block_start + i, zero)
        
    #Se llena la tabla de inodos
    new_Tinode = Table_inode()
    for i in range(n):
        Fwrite_displacement(Crrfile, new_super_block.inode_start + i * struct.calcsize(Table_inode().get_const()), new_Tinode)
    
    #Se llena la tabla de bloques
    new_Fblock = File_block()
    for i in range(3 * n):
        Fwrite_displacement(Crrfile, new_super_block.block_start + i * struct.calcsize(File_block().get_const()), new_Fblock)
        
    #Se cierra el archivo
    Crrfile.close()
    
    #Se deben crear las nuevas estructuras


def create_ext3(n, mPartition, new_super_block, date):
    print("Creando EXT3")
    new_super_block = Super_block()
    #Se coloca el tipo de sistema de archivos
    new_super_block.set_filesystem_type(3)
    
    
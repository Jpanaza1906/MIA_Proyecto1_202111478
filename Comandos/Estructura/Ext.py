import struct

from Comandos.Estructura.Ebr import Ebr
from .Super_block import *
from .Table_inode import *
from .Folder_block import *
from .File_block import *
from .Content import *
from .Load import *
from .Journaling import *
from Utilities.Utilities import *
#FUNCION PARA CREAR EL EXT2

def create_ext2(n, mPartition, new_super_block, date):
    try:
        #CREAR EL EXT2 CONLLEVA
        #crear la carpte raiz "/" -> se crea el inodo 0
        #crear el archivo user.txt -> se crea el inodo 1
        
        #crear carpeta de bloques (bloque 0) -> apunta al inodo 1
        #crear archivo de bloque  (bloque 1) -> alamcena el contenido del user.txt
        
        #RECORRIDO
        #inodo 0 -> bloque 0 -> inodo 1 -> bloque 1
        
        printText("\t Mkfs>>> Creando EXT2")
        #Se coloca el tipo de sistema de archivos
        new_super_block.set_filesystem_type(2)
        Write_Start = 0
        # Si es una particion logica se suma el ebr
        if(mPartition.islogic):
            Write_Start = mPartition.partition.part_start + struct.calcsize(Ebr().get_const())
            new_super_block.set_bm_inode_start(Write_Start + struct.calcsize(Super_block().get_const()))
        else:
            #Se coloca donde comienza el bitmap de inodos
            Write_Start = mPartition.partition.part_start
            new_super_block.set_bm_inode_start(Write_Start + struct.calcsize(Super_block().get_const()))
        
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
        
        Crrfile = open(mPartition.path, 'rb+')
                
        
        #Se llenan las estructuras del ext2
        
        #Se crea un inodo 0
        ##########################################################################################################PROBARRRRRR
        zero = b'\0'
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
        
                
        #Se deben crear las nuevas estructuras
        
        #Se crea el inodo 0
        Inode0 = Table_inode()
        Inode0.set_i_uid(1)
        Inode0.set_i_gid(1)
        Inode0.set_i_size(0)
        Inode0.set_i_atime(date)
        Inode0.set_i_ctime(date)
        Inode0.set_i_mtime(date)
        Inode0.set_i_block(0, 0)        #apunta al bloque 0
        Inode0.set_i_type('0')
        Inode0.set_i_perm('664')
        
        #Se crea un objeto contenido
        
        
        #EL folder block tiene 4 contenidos
        #contenido n: nombre | apuntada a nodo n
        #contenido 0: . | 0
        #contenido 1: .. | 0
        #contenido 2: user.txt | 1
        #contenido 3: espacio
        
        folderb0 = Folder_block()
        #Se llena el contenido 0
        folderb0.b_content[0].set_inodo(0)
        folderb0.b_content[0].set_name('.')
        #Se llena el contenido 1
        folderb0.b_content[1].set_inodo(0)
        folderb0.b_content[1].set_name('..')
        #Se llena el contenido 2
        folderb0.b_content[2].set_inodo(1) # apunta al inodo 1
        folderb0.b_content[2].set_name('user.txt')
        
        #Se muestra el contenido del folder block
        #folderb0.display_info()
        
        #Se crea el inodo 1
        Inode1 = Table_inode()
        Inode1.set_i_uid(1)
        Inode1.set_i_gid(1)
        Inode1.set_i_size(struct.calcsize(File_block().get_const()))
        Inode1.set_i_atime(date)
        Inode1.set_i_ctime(date)
        Inode1.set_i_mtime(date)
        Inode1.set_i_block(0, 1) #apunta al bloque 1
        Inode1.set_i_type('1')
        Inode1.set_i_perm('664')
               
        
        data_usertxt = '1,G,root\n1,U,root,root,123\n'
        fileb1 = File_block()
        fileb1.set_b_content(data_usertxt)
        
        #Se escribe el super bloque
        Fwrite_displacement(Crrfile, Write_Start, new_super_block)
        
        #Se llena el bitmap de inodos
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_inode_start, b'\1')
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_inode_start + 1, b'\1')
        
        #Se llena el bitmap de bloques
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_block_start, b'\1')
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_block_start + 1, b'\1')
        
        #Se llenan los indodos
        Fwrite_displacement(Crrfile, new_super_block.inode_start, Inode0)
        Fwrite_displacement(Crrfile, new_super_block.inode_start + struct.calcsize(Table_inode().get_const()), Inode1)
        
        #Se llenan los bloques
        Fwrite_displacement(Crrfile, new_super_block.block_start, folderb0)
        Fwrite_displacement(Crrfile, new_super_block.block_start + struct.calcsize(File_block().get_const()), fileb1)
        
        
        #Se cierra el archivo
        Crrfile.close()       
        
        return True
    except Exception as e:
        print("Error al crear el EXT2")
        return False


def create_ext3(n, mPartition, new_super_block, date):
    try:
        printText("\t Mkfs>>> Creando EXT3")
        #Se coloca el tipo de sistema de archivos
        new_super_block = Super_block()
        new_super_block.set_filesystem_type(3)
        Write_Start = 0
        
        # Si es una particion logica se suma el ebr
        if(mPartition.islogic):
            Write_Start = mPartition.partition.part_start + struct.calcsize(Ebr().get_const())
            new_super_block.set_bm_inode_start(Write_Start + struct.calcsize(Journaling().get_const()) + struct.calcsize(Super_block().get_const()))
        else:
            #Se coloca donde comienza el bitmap de inodos
            Write_Start = mPartition.partition.part_start 
            new_super_block.set_bm_inode_start(Write_Start + struct.calcsize(Journaling().get_const()) + struct.calcsize(Super_block().get_const()))
        
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
        
        Crrfile = open(mPartition.path, 'rb+')
        
        #Se llenan las estructuras del ext3
        
        #Se crea un inodo 0
        ##########################################################################################################PROBARRRRRR        
        zero = b'\0'
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
            
        #Se deben crear las nuevas estructuras
        
        #Se crea el inodo 0
        Inode0 = Table_inode()
        Inode0.set_i_uid(1)
        Inode0.set_i_gid(1)
        Inode0.set_i_size(0)
        Inode0.set_i_atime(date)
        Inode0.set_i_ctime(date)
        Inode0.set_i_mtime(date)
        Inode0.set_i_block(0, 0)        #apunta al bloque 0
        Inode0.set_i_type('0')
        Inode0.set_i_perm('664')
        
        #Se crea un objeto contenido
        
        #EL folder block tiene 4 contenidos
        #contenido n: nombre | apuntada a nodo n
        #contenido 0: . | 0
        #contenido 1: .. | 0
        #contenido 2: user.txt | 1
        #contenido 3: espacio
        
        folderb0 = Folder_block()
        #Se llena el contenido 0
        folderb0.b_content[0].set_inodo(0)
        folderb0.b_content[0].set_name('.')
        #Se llena el contenido 1
        folderb0.b_content[1].set_inodo(0)
        folderb0.b_content[1].set_name('..')
        #Se llena el contenido 2
        folderb0.b_content[2].set_inodo(1) # apunta al inodo 1
        folderb0.b_content[2].set_name('user.txt')
        
        #Se muestra el contenido del folder block
        #folderb0.display_info()
        
        #Se crea el inodo 1
        Inode1 = Table_inode()
        Inode1.set_i_uid(1)
        Inode1.set_i_gid(1)
        Inode1.set_i_size(struct.calcsize(File_block().get_const()))
        Inode1.set_i_atime(date)
        Inode1.set_i_ctime(date)
        Inode1.set_i_mtime(date)
        Inode1.set_i_block(0, 1) #apunta al bloque 1
        Inode1.set_i_type('1')
        Inode1.set_i_perm('664')
        
        data_usertxt = '1,G,root\n1,U,root,root,123\n'
        fileb1 = File_block()
        fileb1.set_b_content(data_usertxt)
        
        #Se crea el journaling
        journaling = Journaling()
        
        #se crea un contenido
        content1 = ContentJ()
        content1.set_operation("mkdir")
        content1.set_path("/")
        content1.set_content("")
        content1.set_date(date)
        
        #se crea otro contenido
        content2 = ContentJ()
        content2.set_operation("mkfile")
        content2.set_path("/user.txt")
        content2.set_content("1,G,root\n1,U,root,root,123\n")
        content2.set_date(date)
        
        #se agregan al journaling
        
        journaling.set_journaling(0, content1)
        journaling.set_journaling(1, content2)
        
        
        #Se escribe el super bloque
        Fwrite_displacement(Crrfile, Write_Start, new_super_block)
        
        #Se escribe el journaling
        Fwrite_displacement(Crrfile, Write_Start + struct.calcsize(Super_block().get_const()), journaling)
        
        #Se llena el bitmap de inodos
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_inode_start, b'\1')
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_inode_start + 1, b'\1')
        
        #Se llena el bitmap de bloques
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_block_start, b'\1')
        Fwrite_displacement_normal(Crrfile, new_super_block.bm_block_start + 1, b'\1')
        
        #Se llenan los indodos
        Fwrite_displacement(Crrfile, new_super_block.inode_start, Inode0)
        Fwrite_displacement(Crrfile, new_super_block.inode_start + struct.calcsize(Table_inode().get_const()), Inode1)
        
        #Se llenan los bloques
        Fwrite_displacement(Crrfile, new_super_block.block_start, folderb0)
        Fwrite_displacement(Crrfile, new_super_block.block_start + struct.calcsize(File_block().get_const()), fileb1)
        
        #Se cierra el archivo
        Crrfile.close()        
        
        return True
    except Exception as e:
        print("Error al crear el EXT3")
        return False
    
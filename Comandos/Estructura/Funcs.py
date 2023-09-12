from Utilities.Utilities import *
from Comandos.Estructura.Super_block import *
from Comandos.Estructura.Ebr import *
from Comandos.Estructura.Table_inode import *
from Comandos.Estructura.Load import *
from Comandos.Estructura.Folder_block import *
from Comandos.Estructura.File_block import *
from Comandos.Estructura.Journaling import *
from Global.Global import *

# Funciones -----------------------------------------------------------------------------

# Return INODE INFO from id partition and name file

def getInodeInfo(id, name):
    # Se busca la particion

    mPartition = buscar_particion(id)

    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False

    # Se verifica que ya este formateada la particion a traves del super bloque
    # Se crea el super bloque temporal
    Temp_suberB = Super_block()

    # Se abre el archivo
    Crrfile = open(mPartition.path, 'rb+')

    # Si es una particion extendida se suma el ebr
    if (mPartition.islogic):
        Fread_displacement(Crrfile, mPartition.partition.part_start +
                           struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(
            Crrfile, mPartition.partition.part_start, Temp_suberB)

    # Temp_suberB.display_info()

    # Se obtiene el inodo de inicio
    inicioInodo = Table_inode()
    Fread_displacement(Crrfile, Temp_suberB.inode_start, inicioInodo)
    contenidoArch = []
    # Se recorren los bloques del nodo de inicio
    for i in range(15):
        if (inicioInodo.i_block[i] == -1):
            break
        # Se lee el bloque
        bloque = Folder_block()
        Fread_displacement(Crrfile, Temp_suberB.block_start +
                           inicioInodo.i_block[i] * struct.calcsize(Folder_block().get_const()), bloque)

        # Se recorre el bloque
        for j in range(4):
            if (bloque.b_content[j].b_name.decode() == name):
                # Se verifica la contraseña
                if (bloque.b_content[j].b_inodo == -1):
                    printError("\t Error>>> El usuario no tiene contraseña\n")
                    return False
                # Se obtiene el inodo del usuario\
                inodoUser = Table_inode()
                Fread_displacement(Crrfile, Temp_suberB.inode_start +
                                   bloque.b_content[j].b_inodo * struct.calcsize(Table_inode().get_const()), inodoUser)

                # Se busca entre los bloques del inodo

                for i in range(15):
                    if (inodoUser.i_block[i] == -1):
                        break
                    # Se lee el bloque
                    bloqueUser = File_block()
                    Fread_displacement(Crrfile, Temp_suberB.block_start +
                                       inodoUser.i_block[i] * struct.calcsize(File_block().get_const()), bloqueUser)
                    temp = [bloqueUser.b_content.decode(), inodoUser.i_block[i]]
                    contenidoArch.append(temp)
    # Se returna el contenido encontrado
    return contenidoArch

#funcion para escribir en el bloque archivo n
def modifyBlockContent(id, n, contenido):
    
    #se busca la particion
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    # Se verifica que ya este formateada la particion a traves del super bloque
    # Se crea el super bloque temporal
    Temp_suberB = Super_block()
    
    # Se abre el archivo
    Crrfile = open(mPartition.path, 'rb+')
    
    # Si es una particion extendida se suma el ebr
    if (mPartition.islogic):
        Fread_displacement(Crrfile, mPartition.partition.part_start +
                           struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(
            Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Se obtiene el inicio de bloques
    
    iniciobloques = Temp_suberB.block_start
    
    # Se lee el bloque
    bloque = File_block()
    Fread_displacement(Crrfile, iniciobloques + n * struct.calcsize(File_block().get_const()), bloque)
    
    # Se modifica el contenido
    bloque.set_b_content(contenido)
    
    # Se escribe el bloque
    Fwrite_displacement(Crrfile, iniciobloques + n * struct.calcsize(File_block().get_const()), bloque)
    
    # Se cierra el archivo
    Crrfile.close()
    
    return True
    
    
    
    

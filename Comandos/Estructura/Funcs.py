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

#funcion para obtener el numero del inodo
def getInodeNumber(id, name):
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
                return bloque.b_content[j].b_inodo


#funcion para modificar los apuntadores de un inodo
def modifyInodePointers(id, name, contenidocompleto):
    # Se busca la particion
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    ninodo = getInodeNumber(id, name)
    
    # Se verifica que ya este formateada la particion a traves del super bloque
    # Se crea el super bloque temporal
    Temp_suberB = Super_block()
    
    # Se abre el archivo
    Crrfile = open(mPartition.path, 'rb+')
    
    WriteStart = mPartition.partition.part_start
    
    # Si es una particion extendida se suma el ebr
    if (mPartition.islogic):
        WriteStart += struct.calcsize(Ebr().get_const())
        Fread_displacement(Crrfile, mPartition.partition.part_start +
                           struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(
            Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodo = Table_inode()
    Fread_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
    
    #se divide el contenido en bloques de 64 caracteres
    bloques = []
    for i in range(0, len(contenidocompleto), 64):
        bloques.append(contenidocompleto[i:i+64])
    
    #se verifica que el contenido no exceda los 15 bloques del inodo
    
    if (len(bloques) >= 15):
        printError("\t Error>>> El archivo es demasiado grande\n")
        return False
    
    #se recorren los bloques del inodo
    nblock = getCurrentNblock(id)
    for i in range(15):
        if (i < len(bloques)):
            #se verifica que el bloque no este ocupado
            if (inodo.i_block[i] == -1):
                #se crea un nuevo bloque
                modifyBlockContent(id, nblock, bloques[i])
                inodo.i_block[i] = nblock
                
                #se actualiza el numero de bloques en el super bloque
                Temp_suberB.Block_Created()
                
                #Se escribe el bloque en el bitmap de bloques
                bitmap = Fread_displacement_normal(Crrfile, Temp_suberB.bm_block_start, Temp_suberB.inode_start)
                arraybytes = list(bitmap)
                arraybytes[nblock] = 1
                bitmap = bytes(arraybytes)
                Fwrite_displacement_normal(Crrfile, Temp_suberB.bm_block_start, bitmap)                
                nblock += 1
            else:
                #se lee el bloque
                modifyBlockContent(id, inodo.i_block[i], bloques[i])
        else:
            break
    
    #Se escribe el superbloque
    Fwrite_displacement(Crrfile, WriteStart, Temp_suberB)
    
    #se escribe el inodo
    Fwrite_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
    
    
    
    #se cierra el archivo
    Crrfile.close()
    
    return True
            
            

def getCurrentNblock(id):
    #funcion que recorre el bitmap de bloques, cuenta los 1s y devuelve el numero que toca
    mPartition = buscar_particion(id)
    
    Temp_superB = Super_block()
    
    Crrfile = open(mPartition.path, 'rb+')
    
    #Si es una particion logica se le suma el ebr
    if (mPartition.islogic):
        Fread_displacement(Crrfile, mPartition.partition.part_start +
                           struct.calcsize(Ebr().get_const()), Temp_superB)
    else:
        Fread_displacement(
            Crrfile, mPartition.partition.part_start, Temp_superB)
    
    inicioBitmapBloques = Temp_superB.bm_block_start
    
    #se lee el bitmap de bloques
    bitmap = Fread_displacement_normal(Crrfile, inicioBitmapBloques, Temp_superB.inode_start)
        
    #se recorre el bitmap y se cuentan los 1s
    contador = 0
    for i in range(len(bitmap)):
        if (bitmap[i] != 1):
            break
        contador += 1
    #se cierra el archivo
    Crrfile.close()
    
    return contador

def getCurrentNinode(id):
    #funcion que recorre el bitmap de inodos, cuenta los 1s y devuelve el numero que toca
    mPartition = buscar_particion(id)
    
    Temp_superB = Super_block()
    
    Crrfile = open(mPartition.path, 'rb+')
    
    #Si es una particion logica se le suma el ebr
    if (mPartition.islogic):
        Fread_displacement(Crrfile, mPartition.partition.part_start +
                           struct.calcsize(Ebr().get_const()), Temp_superB)
    else:
        Fread_displacement(
            Crrfile, mPartition.partition.part_start, Temp_superB)
    
    inicioBitmapInodos = Temp_superB.bm_inode_start
    
    #se lee el bitmap de bloques
    bitmap = Fread_displacement_normal(Crrfile, inicioBitmapInodos, Temp_superB.bm_block_start)
        
    #se recorre el bitmap y se cuentan los 1s
    contador = 0
    for i in range(len(bitmap)):
        if (bitmap[i] != 1):
            break
        contador += 1
    #se cierra el archivo
    Crrfile.close()
    
    return contador
    

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
    
    
    
    

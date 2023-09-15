import random
from Utilities.Utilities import *
from Comandos.Estructura.Super_block import *
from Comandos.Estructura.Ebr import *
from Comandos.Estructura.Table_inode import *
from Comandos.Estructura.Load import *
from Comandos.Estructura.Folder_block import *
from Comandos.Estructura.File_block import *
from Comandos.Estructura.Journaling import *
from Comandos.Estructura.ContentJ import *
from Global.Global import *
from datetime import datetime

# Funciones -----------------------------------------------------------------------------

#funcion para modificar los apuntadores de un inodo---------------------------------------------------------------
def modifyFileContent(id, path, contenidocompleto):
    # Se busca la particion
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    ninodo = getInodeNumberFromPath(id, path)
    
    if (ninodo == -1):
        printError("\t Error>>> Error al escribir en archivo")
        return False
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
    
    if (Temp_suberB.filesystem_type == 3):
        content = ContentJ()
        content.set_operation("edit")
        content.set_path(path)
        content.set_content(contenidocompleto)
        content.set_date(datetime.now().strftime("%d/%m/%Y"))
        n = 0
        for i in range(50):
            ContenidoJ = ContentJ()
            Fread_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + (i * struct.calcsize(ContentJ().get_const())), ContenidoJ)
            #si la fecha es vacia se termina
            if ContenidoJ.operation == b'':
                n = i
                break
        
        
        #Se escribe el journaling
        Fwrite_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + n * struct.calcsize(ContentJ().get_const()), content)
    
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
        #se cierra el archivo
        Crrfile.close()
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
            
#FUNCION PARA MODIFICAR NOMBRE DE ARCHIVO O CARPETA--------------------------------------------------------------------
def modifyNameContent(id, path, nombre, nuevonombre):
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    ninodo = getInodeNumberFromPath(id, path)
    
    if (ninodo == -1):
        printError("\t Error>>> Error al escribir en archivo")
        return False
    
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
    
    if (Temp_suberB.filesystem_type == 3):
        content = ContentJ()
        content.set_operation("rename")
        content.set_path(path)
        content.set_content(nuevonombre)
        content.set_date(datetime.now().strftime("%d/%m/%Y"))
        n = 0
        for i in range(50):
            ContenidoJ = ContentJ()
            Fread_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + (i * struct.calcsize(ContentJ().get_const())), ContenidoJ)
            #si la fecha es vacia se termina
            if ContenidoJ.operation == b'':
                n = i
                break
        
        
        #Se escribe el journaling
        Fwrite_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + n * struct.calcsize(ContentJ().get_const()), content)
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodo = Table_inode()
    Fread_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
    
    # Se obtiene el nombre del inodo
    for i in range(15):
        if (inodo.i_block[i] != -1):
            bloque = Folder_block()
            Fread_displacement(Crrfile, Temp_suberB.block_start + inodo.i_block[i] * struct.calcsize(Folder_block().get_const()), bloque)
            for j in range(4):
                if (bloque.b_content[j].b_inodo != -1):
                    if (bloque.b_content[j].b_name.decode() == nombre):
                        bloque.b_content[j].set_name(nuevonombre)
                        Fwrite_displacement(Crrfile, Temp_suberB.block_start + inodo.i_block[i] * struct.calcsize(Folder_block().get_const()), bloque)
                        Crrfile.close()
                        return True
    Crrfile.close()
    return False
               
#FUNCION PARA OBTENER EL BLOQUE ACTUAL--------------------------------------------------------------------------------------------
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

#FUNCION PARA OBTENER EL NUMERO DE INODO ACTUAL-------------------------------------------------------------------------
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
    

#funcion para escribir en el bloque archivo n--------------------------------------------------------------------------
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

#funcion para crear carpeta haciendo una busqueda en los inodos------------------------------------------------------

def createFolder(id, path, date):
    # Se busca la particion
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    ninodo = getInodeNumberFromPath(id, path)
    
    if (ninodo != -1):
        printError("\t Error>>> Ya existe una carpeta con ese nombre\n")
        return False
    
    #Se obtiene la ruta completa hasta la carpeta padre
    carpetas = [elemento for elemento in path.split('/') if elemento]
    nombre = carpetas.pop()
    pathpadre = ''
    for carpeta in carpetas:
        pathpadre = pathpadre + '/' + carpeta
        
    #Se obtiene el numero del inodo de la carpeta padre
    if (pathpadre == ''):
        ninodopadre = 0
    else:
        ninodopadre = getInodeNumberFromPath(id, pathpadre)
    
    if (ninodopadre == -1):
        printError("\t Error>>> No existe la carpeta padre\n")
        return False
    
    # Se verifica que ya este formateada la particion a traves del super bloque    
    # Se crea el super bloque temporal
    Temp_suberB = Super_block()
    
    # Se abre el archivo
    Crrfile = open(mPartition.path, 'rb+')
    
    WriteStart = mPartition.partition.part_start
    
    # Si es una particion extendida se suma el ebr
    if (mPartition.islogic):
        WriteStart += struct.calcsize(Ebr().get_const())
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    if (Temp_suberB.filesystem_type == 3):
        content = ContentJ()
        content.set_operation("mkdir")
        content.set_path(path)
        content.set_content('')
        content.set_date(datetime.now().strftime("%d/%m/%Y"))
        n = 0
        for i in range(50):
            ContenidoJ = ContentJ()
            Fread_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + (i * struct.calcsize(ContentJ().get_const())), ContenidoJ)
            #si la fecha es vacia se termina
            if ContenidoJ.operation == b'':
                n = i
                break
        
        
        #Se escribe el journaling
        Fwrite_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + n * struct.calcsize(ContentJ().get_const()), content)
    
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodopadre = Table_inode()
    Fread_displacement(Crrfile, inicioInodo + ninodopadre * struct.calcsize(Table_inode().get_const()), inodopadre)
    
    # Se busca entre sus apuntadores de bloques si existe un espacio
    ninodo = getCurrentNinode(id)
    nbloque = getCurrentNblock(id)
    # Se recorren los bloques del nodo de inicio
    for i in range(15):
        apuntador = inodopadre.i_block[i]
        if apuntador != -1:
        # Se lee el bloque
            bloque = Folder_block()
            Fread_displacement(Crrfile, Temp_suberB.block_start + apuntador * struct.calcsize(Folder_block().get_const()), bloque)
            # Se recorre el bloque
            for j in range(4):
                if (bloque.b_content[j].b_inodo == -1) or (bloque.b_content[j].b_inodo == -2):
                    #Se modifica el bloque actual con el nuevo inodo
                    bloque.b_content[j].set_inodo(ninodo)
                    bloque.b_content[j].set_name(nombre)
                    
                    # Se escribe el bloque
                    Fwrite_displacement(Crrfile, Temp_suberB.block_start + apuntador * struct.calcsize(Folder_block().get_const()), bloque)
                    
                    # Se crea el nuevo inodo que representa a la carpeta
                    inodo = Table_inode()
                    inodo.set_i_uid(ninodo)
                    inodo.set_i_gid(ninodo)
                    inodo.set_i_size(0)
                    inodo.set_i_atime(date)
                    inodo.set_i_ctime(date)
                    inodo.set_i_mtime(date)
                    inodo.set_i_type('0')
                    inodo.set_i_perm('664')
                    inodo.set_i_block(0, nbloque) #apunta a un bloque nuevo que indicara su contenido
                    
                    # Se escribe el inodo
                    Fwrite_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
                    
                    
                    # Se crea un nuevo bloque vacio
                    bloque = Folder_block()
                    #Se llena el contenido de 0
                    bloque.b_content[0].set_inodo(nbloque)
                    bloque.b_content[0].set_name('.')
                    #Se llena el contenido de 1
                    bloque.b_content[1].set_inodo(ninodo)
                    bloque.b_content[1].set_name('..')
                    
                    #Los otros dos se dejan vacios porque solo se esta creando la carpeta
                    
                    # Se escribe el bloque
                    Fwrite_displacement(Crrfile, Temp_suberB.block_start + nbloque * struct.calcsize(Folder_block().get_const()), bloque)
                    
                                
                    # Se actualiza el numero de inodos en el super bloque
                    addBlocktoBitmap(id, nbloque)
                    addInodetoBitmap(id, ninodo)
                    Temp_suberB.Inode_Created()
                    Temp_suberB.Block_Created()
                    
                    # Se escribe el superbloque
                    Fwrite_displacement(Crrfile, WriteStart, Temp_suberB)
                    
                    # Se cierra el archivo
                    Crrfile.close()
                    
                    return True
        #Si no existe un espacio se crea un nuevo bloque
        else:
            inodopadre.i_block[i] = nbloque
            #Se escribe el inodo padre
            Fwrite_displacement(Crrfile, inicioInodo + ninodopadre * struct.calcsize(Table_inode().get_const()), inodopadre)
            
            #Se crea un nuevo bloque vacio
            bloque = Folder_block()
            #Se llena el contenido de 0
            bloque.b_content[0].set_inodo(ninodo)
            bloque.b_content[0].set_name(nombre)
            
            #Se escribe el bloque
            Fwrite_displacement(Crrfile, Temp_suberB.block_start + nbloque * struct.calcsize(Folder_block().get_const()), bloque)
            nbloque += 1
            
            #Se crea el nuevo inodo que representa a la carpeta
            inodo = Table_inode()
            inodo.set_i_uid(ninodo)
            inodo.set_i_gid(ninodo)
            inodo.set_i_size(0)
            inodo.set_i_atime(date)
            inodo.set_i_ctime(date)
            inodo.set_i_mtime(date)
            inodo.set_i_type('0')
            inodo.set_i_perm('664')
            inodo.set_i_block(0, nbloque) #apunta a un bloque nuevo que indicara su contenido
            
            #Se escribe el inodo
            Fwrite_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
            
            #Se crea un nuevo bloque vacio
            bloque = Folder_block()
            #Se llena el contenido de 0
            bloque.b_content[0].set_inodo(nbloque)
            bloque.b_content[0].set_name('.')
            #Se llena el contenido de 1
            bloque.b_content[1].set_inodo(ninodo)
            bloque.b_content[1].set_name('..')
            
            #Los otros dos se dejan vacios porque solo se esta creando la carpeta
            
            #Se escribe el bloque
            Fwrite_displacement(Crrfile, Temp_suberB.block_start + nbloque * struct.calcsize(Folder_block().get_const()), bloque)
            
            #Se actualizan los valores del super bloque
            addInodetoBitmap(id, ninodo)
            Temp_suberB.Inode_Created()
            
            addBlocktoBitmap(id, nbloque-1)
            Temp_suberB.Block_Created()
            
            addBlocktoBitmap(id, nbloque)
            Temp_suberB.Block_Created()
            
            #Se escribe el superbloque
            Fwrite_displacement(Crrfile, WriteStart, Temp_suberB)
            
            #Se cierra el archivo
            Crrfile.close()
            
            return True
            

#FUNCION PARA CREAR UN ARCHIVO CON LA RUTA COMPLETA----------------------------------------------
def createFile(id, path, date, size, cont):
    # Se busca la particion
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    ninodo = getInodeNumberFromPath(id, path)
    
    if (ninodo != -1):
        printError("\t Error>>> Ya existe un archivo con ese nombre en la misma ruta\n")
        return False
    
    #Se obtiene la ruta completa hasta la carpeta padre
    carpetas = [elemento for elemento in path.split('/') if elemento]
    nombre = carpetas.pop()
    pathpadre = ''
    for carpeta in carpetas:
        pathpadre = pathpadre + '/' + carpeta
        
    #Se obtiene el numero del inodo de la carpeta padre
    if (pathpadre == ''):
        ninodopadre = 0
    else:
        ninodopadre = getInodeNumberFromPath(id, pathpadre)
    
    if (ninodopadre == -1):
        printError("\t Error>>> No existe la carpeta padre\n")
        return False
    
    contenidofinal = ''
    #Se verifica si la variable cont es None
    if (cont != None):
        #Se lee el contenido de la ruta del archivo en la computadora
        try:
            archivo = open(cont, 'r')
            contenidofinal = archivo.read()
            archivo.close()
        except Exception as e:
            printError("\t Error>>> No existe el archivo\n")
            return False
    elif (size != None):
        #Se llena el contenido con numeros del 0 al 9 random
        for i in range(int(size)):
            contenidofinal = contenidofinal + str(random.randint(0, 9))
    else:
        printError("\t Error>>> Falta el parametro size o cont\n")
        return False
        
    
    # Se verifica que ya este formateada la particion a traves del super bloque    
    # Se crea el super bloque temporal
    Temp_suberB = Super_block()
    
    # Se abre el archivo
    Crrfile = open(mPartition.path, 'rb+')
    
    WriteStart = mPartition.partition.part_start
    
    # Si es una particion extendida se suma el ebr
    if (mPartition.islogic):
        WriteStart += struct.calcsize(Ebr().get_const())
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodopadre = Table_inode()
    Fread_displacement(Crrfile, inicioInodo + ninodopadre * struct.calcsize(Table_inode().get_const()), inodopadre)
    
    #si es EXT3 se agrega el journaling
    if (Temp_suberB.filesystem_type == 3):
        content = ContentJ()
        content.set_operation("mkfile")
        content.set_path(path)
        content.set_content(contenidofinal)
        content.set_date(datetime.now().strftime("%d/%m/%Y"))
        n = 0
        for i in range(50):
            ContenidoJ = ContentJ()
            Fread_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + (i * struct.calcsize(ContentJ().get_const())), ContenidoJ)
            #si la fecha es vacia se termina
            if ContenidoJ.operation == b'':
                n = i
                break
        
        
        #Se escribe el journaling
        Fwrite_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + n * struct.calcsize(ContentJ().get_const()), content)
        
        
    
    # Se busca entre sus apuntadores de bloques si existe un espacio
    ninodo = getCurrentNinode(id)
    nbloque = getCurrentNblock(id)
    # Se recorren los bloques del nodo de inicio
    for i in range(15):
        apuntador = inodopadre.i_block[i]
        if apuntador != -1:
        # Se lee el bloque
            bloque = Folder_block()
            Fread_displacement(Crrfile, Temp_suberB.block_start + apuntador * struct.calcsize(Folder_block().get_const()), bloque)
            # Se recorre el bloque
            for j in range(4):
                if (bloque.b_content[j].b_inodo == -1) or (bloque.b_content[j].b_inodo == -2):
                    #Se modifica el bloque actual con el nuevo inodo
                    bloque.b_content[j].set_inodo(ninodo)
                    bloque.b_content[j].set_name(nombre)
                    
                    # Se escribe el bloque
                    Fwrite_displacement(Crrfile, Temp_suberB.block_start + apuntador * struct.calcsize(Folder_block().get_const()), bloque)
                    
                    # Se crea el nuevo inodo que representa a la carpeta
                    inodo = Table_inode()
                    inodo.set_i_uid(ninodo)
                    inodo.set_i_gid(ninodo)
                    inodo.set_i_size(0)
                    inodo.set_i_atime(date)
                    inodo.set_i_ctime(date)
                    inodo.set_i_mtime(date)
                    inodo.set_i_type('1')
                    inodo.set_i_perm('664')
                    inodo.set_i_block(0, nbloque) #apunta a un bloque nuevo que indicara su contenido
                    
                    # Se escribe el inodo
                    Fwrite_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
                    
                    
                    # Se crea un nuevo bloque de archivos vacio
                    bloque = File_block()                    
                    # Se escribe el bloque
                    Fwrite_displacement(Crrfile, Temp_suberB.block_start + nbloque * struct.calcsize(File_block().get_const()), bloque)
                    
                                
                    # Se actualiza el numero de inodos en el super bloque
                    addBlocktoBitmap(id, nbloque)
                    addInodetoBitmap(id, ninodo)
                    Temp_suberB.Inode_Created()
                    Temp_suberB.Block_Created()
                    
                    # Se escribe el superbloque
                    Fwrite_displacement(Crrfile, WriteStart, Temp_suberB)
                    
                    # Se cierra el archivo
                    Crrfile.close()
                    
                    #Se modifica el contenido del bloque
                    if modifyFileContent(id, path, contenidofinal):              
                        return True
                    return False
        #Si no existe un espacio se crea un nuevo bloque
        else:
            inodopadre.i_block[i] = nbloque
            #Se escribe el inodo padre
            Fwrite_displacement(Crrfile, inicioInodo + ninodopadre * struct.calcsize(Table_inode().get_const()), inodopadre)
            
            #Se crea un nuevo bloque vacio
            bloque = Folder_block()
            #Se llena el contenido de 0
            bloque.b_content[0].set_inodo(ninodo)
            bloque.b_content[0].set_name(nombre)
            
            #Se escribe el bloque
            Fwrite_displacement(Crrfile, Temp_suberB.block_start + nbloque * struct.calcsize(Folder_block().get_const()), bloque)
            
            #Se crea el nuevo inodo que representa a la carpeta
            inodo = Table_inode()
            inodo.set_i_uid(ninodo)
            inodo.set_i_gid(ninodo)
            inodo.set_i_size(0)
            inodo.set_i_atime(date)
            inodo.set_i_ctime(date)
            inodo.set_i_mtime(date)
            inodo.set_i_type('1')
            inodo.set_i_perm('664')
            inodo.set_i_block(0, nbloque) #apunta a un bloque nuevo que indicara su contenido
            
            #Se escribe el inodo
            Fwrite_displacement(Crrfile, inicioInodo + ninodo * struct.calcsize(Table_inode().get_const()), inodo)
            
            #Se crea un nuevo bloque de archivo vacio
            bloque = File_block()
            #Se escribe el bloque
            Fwrite_displacement(Crrfile, Temp_suberB.block_start + nbloque * struct.calcsize(File_block().get_const()), bloque)
            
            #Se actualizan los valores del super bloque
            addInodetoBitmap(id, ninodo)
            Temp_suberB.Inode_Created()
            
            addBlocktoBitmap(id, nbloque)
            Temp_suberB.Block_Created()
            
            
            #Se escribe el superbloque
            Fwrite_displacement(Crrfile, WriteStart, Temp_suberB)
            
            #Se cierra el archivo
            Crrfile.close()
            
            #Se modifica el contenido del bloque
            if modifyFileContent(id, path, contenidofinal):
                return True
            return False
    return False

#FUNCION PARA REMOVER FOLDER CON LA RUTA COMPLETA ----------------------------------------------

def removeFolderFile(id, pathpadre, nombre):
    #se busca la particion
    mPartition = buscar_particion(id)
    
    if mPartition is None:
        printError("\t Error>>> No existe la particion\n")
        return False
    
    #Se obtiene el numero del inodo de la carpeta padre
    if (pathpadre == ''):
        ninodopadre = 0
    else:
        ninodopadre = getInodeNumberFromPath(id, pathpadre)
        
    if (ninodopadre == -1):
        printError("\t Error>>> No existe la carpeta padre\n")
        return False
    
    # Se verifica que ya este formateada la particion a traves del super bloque
    
    # Se crea el super bloque temporal
    Temp_suberB = Super_block()
    
    # Se abre el archivo
    Crrfile = open(mPartition.path, 'rb+')
    
    WriteStart = mPartition.partition.part_start
    
    # Si es una particion extendida se suma el ebr
    if (mPartition.islogic):
        WriteStart += struct.calcsize(Ebr().get_const())
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    if (Temp_suberB.filesystem_type == 3):
        content = ContentJ()
        content.set_operation("remove")
        content.set_path(pathpadre + '/' + nombre)
        content.set_content('')
        content.set_date(datetime.now().strftime("%d/%m/%Y"))
        n = 0
        for i in range(50):
            ContenidoJ = ContentJ()
            Fread_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + (i * struct.calcsize(ContentJ().get_const())), ContenidoJ)
            #si la fecha es vacia se termina
            if ContenidoJ.operation == b'':
                n = i
                break
        
        
        #Se escribe el journaling
        Fwrite_displacement(Crrfile, WriteStart + struct.calcsize(Super_block().get_const()) + n * struct.calcsize(ContentJ().get_const()), content)
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodopadre = Table_inode()
    Fread_displacement(Crrfile, inicioInodo + ninodopadre * struct.calcsize(Table_inode().get_const()), inodopadre)
    
    # Se busca entre sus apuntadores de bloque el inodo que se desea eliminar
    # Se recorren los bloques del nodo de inicio
    for i in range(15):
        apuntador = inodopadre.i_block[i]
        if apuntador != -1:
        # Se lee el bloque
            bloque = Folder_block()
            Fread_displacement(Crrfile, Temp_suberB.block_start + apuntador * struct.calcsize(Folder_block().get_const()), bloque)
            # Se recorre el bloque
            for j in range(4):
                if (bloque.b_content[j].b_inodo != -1):
                    if (bloque.b_content[j].b_name.decode() == nombre):
                        #Se modifica el bloque actual con el nuevo inodo
                        bloque.b_content[j].set_inodo(-2)
                        bloque.b_content[j].set_name('')
                                                
                        # Se escribe el bloque
                        Fwrite_displacement(Crrfile, Temp_suberB.block_start + apuntador * struct.calcsize(Folder_block().get_const()), bloque)
                                                                        
                        # Se cierra el archivo
                        Crrfile.close()
                        
                        return True
        #Si no existe un espacio se crea un nuevo bloque
        else:
            break
            
    pass

#FUNCION PARA OBTENER EL NUMERO DEL INODO CON LA RUTA COMPLETA-------------------------------------------------------------
def getInodeNumberFromPath(id, path):
    
    #Se divide la ruta en carpetas
    carpetas = [elemento for elemento in path.split('/') if elemento]
    
    #Se busca la particion
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
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodo = Table_inode()
    Fread_displacement(Crrfile, inicioInodo, inodo)
    
    # Se recorren los bloques del nodo de inicio
    i = 0 #indice para leer cada apuntador del inodo
    j = 0 #indice para recorrer las carpetas
    while True:            
        encontrado = False       
        if (inodo.i_block[i] == -1):
            break
        readfolderbloq = inodo.i_block[i]
        # Se lee el bloque
        bloque = Folder_block()
        Fread_displacement(Crrfile, Temp_suberB.block_start + readfolderbloq * struct.calcsize(Folder_block().get_const()), bloque)
                
        # Se recorre el bloque
        for k in range(4):
            if(bloque.b_content[k].b_inodo == -1):
                break
            if (bloque.b_content[k].b_name.decode() == carpetas[j]):
                # Si concuerda el nombre se obtiene el inodo
                inodo2 = Table_inode()
                Fread_displacement(Crrfile, inicioInodo + bloque.b_content[k].b_inodo * struct.calcsize(Table_inode().get_const()), inodo2)
                        
                #Se verifica si es el ultimo
                if (j == len(carpetas) - 1):
                    #Se cierra el archivo
                    Crrfile.close()
                    return bloque.b_content[k].b_inodo
                else:  
                    inodo = inodo2    
                    encontrado = True
                    j += 1
                    break
        if (encontrado):
            i = 0
            continue
        i += 1
    
    #Se cierra el archivo
    Crrfile.close()
    return -1

#FUNCION PARA OBTENER EL CONTENIDO DE UN ARCHIVO CON LA RUTA COMPLETA------------------------------------------------------------------------------
def getFileContentFromPath(id, path):
    #Se divide la ruta en carpetas
    carpetas = [elemento for elemento in path.split('/') if elemento]
    
    #Se busca la particion
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
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodo = Table_inode()
    Fread_displacement(Crrfile, inicioInodo, inodo)
    contenidoArch = []
    # Se recorren los bloques del nodo de inicio
    i = 0 #indice para leer cada apuntador del inodo
    j = 0 #indice para recorrer las carpetas
    while True:            
        encontrado = False       
        if (inodo.i_block[i] == -1):
            break
        readfolderbloq = inodo.i_block[i]
        # Se lee el bloque
        bloque = Folder_block()
        Fread_displacement(Crrfile, Temp_suberB.block_start + readfolderbloq * struct.calcsize(Folder_block().get_const()), bloque)
                
        # Se recorre el bloque
        for k in range(4):
            if(bloque.b_content[k].b_inodo == -1):
                break
            if (bloque.b_content[k].b_name.decode() == carpetas[j]):
                # Si concuerda el nombre se obtiene el inodo
                inodo2 = Table_inode()
                Fread_displacement(Crrfile, inicioInodo + bloque.b_content[k].b_inodo * struct.calcsize(Table_inode().get_const()), inodo2)
                        
                #Se verifica si es el ultimo
                if (j == len(carpetas) - 1):
                    for w in range(15):
                        if (inodo2.i_block[w] == -1):
                            break
                        bloqueUser = File_block()
                        Fread_displacement(Crrfile, Temp_suberB.block_start + inodo2.i_block[w] * struct.calcsize(File_block().get_const()), bloqueUser)
                        temp = [bloqueUser.b_content.decode(), inodo2.i_block[w]]
                        contenidoArch.append(temp)                        
                else:  
                    inodo = inodo2    
                    encontrado = True
                    j += 1
                    break
        if (encontrado):
            i = 0
            continue
        i += 1
    
    #Se cierra el archivo
    Crrfile.close() 
    
    return contenidoArch

#FUNCION PARA AGREGAR BLOQUE AL BITMAP DE BLOQUES---------------------------------------------------------------------------------
def addBlocktoBitmap(id, n):
    #funcion que agrega un bloque al bitmap de bloques
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
        
    #       
    #se modifica el bitmap
    arraybytes = list(bitmap)
    arraybytes[n] = 1
    bitmap = bytes(arraybytes)
    
    #se escribe el bitmap
    Fwrite_displacement_normal(Crrfile, inicioBitmapBloques, bitmap)
    
    #se cierra el archivo
    Crrfile.close()
    
#FUNCION PARA AGREGAR INODO AL BITMAP DE INODOS---------------------------------------------------------------------------------
def addInodetoBitmap(id, n):
    #funcion que agrega un inodo al bitmap de inodos
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
        
    #       
    #se modifica el bitmap
    arraybytes = list(bitmap)
    arraybytes[n] = 1
    bitmap = bytes(arraybytes)
    
    #se escribe el bitmap
    Fwrite_displacement_normal(Crrfile, inicioBitmapInodos, bitmap)
    
    #se cierra el archivo
    Crrfile.close()
    
    
#FUNCION PARA COPIAR UN ARCHIVO O CARPETA A UNA CARPETA CON LA RUTA COMPLETA
def copyFolderFile(id, path, dest, date):
    pass

#FUNCION PARA RECORRER LOS INODOS Y BLOQUES Y GENERAR UN REPORTE DE LA PARTICION
def reporteTree(id):
    
    #Se busca la particion
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
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    #Se crea una variable para concatenar los reportes
    reporte = ''
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodoinicial = Table_inode()
    Fread_displacement(Crrfile, inicioInodo, inodoinicial)
    
    #Se agrega al reporte el inodo raiz
    reporte += reporteInodoHijos(inodoinicial, Crrfile, Temp_suberB)
    
    #Se cierra el archivo
    Crrfile.close()
    
    return reporte

def reporteInodoHijos(inodo, Crrfile, Temp_suberB):
    
    reporte = ''
    
    #Se agrega el inodo al reporte
    reporte += inodo.generarInodoRep()
    
    #Se recorren todos los apuntadores de inodoinicio
    
    i = 0 #indice para leer cada apuntador del inodo
    
    while True:
        if (inodo.i_block[i] == -1):
            break
        readfolderbloq = inodo.i_block[i]
        # Se lee el bloque
        bloquefold = Folder_block()
        bloquearch = File_block()
        Fread_displacement(Crrfile, Temp_suberB.block_start + readfolderbloq * struct.calcsize(Folder_block().get_const()), bloquefold)
        Fread_displacement(Crrfile, Temp_suberB.block_start + readfolderbloq * struct.calcsize(File_block().get_const()), bloquearch)
                
        #if(bloquefold.b_content[0].b_name.decode() == '.'):    
        
        if(inodo.i_type == b'0'):
            reporte += reporteBloquesHijos(bloquefold, Crrfile, Temp_suberB, inodo.i_block[i])
        else:
            reporte += reporteBloquesHijos(bloquearch, Crrfile, Temp_suberB, inodo.i_block[i])
        reporte += "Inodo" + str(inodo.i_uid) + ":" +str(i+1) + " -> " + "Bloque" + str(inodo.i_block[i])+":0;" + " "
        i += 1
    
    return reporte

def reporteBloquesHijos(bloque, Crrfile, Temb_suberB, n):    
    reporte = ''
    
    #Se verifica si es un bloque de carpetas o de archivos
    if (not isinstance(bloque.b_content,(list,tuple))):
        reporte += bloque.generar_reporte(n)
        
    #Se recorre el bloque
    else:
        reporte += bloque.generarBloqueRep(n)
        for k in range(4):
            if(bloque.b_content[k].b_inodo == -1 or bloque.b_content[k].b_inodo == -2):
                continue
            if(bloque.b_content[k].b_name.decode() == '.' or bloque.b_content[k].b_name.decode() == '..'):
                continue
            inodo = Table_inode()
            Fread_displacement(Crrfile, Temb_suberB.inode_start + bloque.b_content[k].b_inodo * struct.calcsize(Table_inode().get_const()), inodo)
            reporte += reporteInodoHijos(inodo, Crrfile, Temb_suberB)
            reporte += "Bloque" + str(n) + ":" +str(k+1) + " -> " + "Inodo" + str(bloque.b_content[k].b_inodo) +":0;" + " "
        
    return reporte
        
    
    
#FUNCION PARA REPORTES DE LOS BLOQUES
def reporteBlock(id):
    
    #Se busca la particion
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
        Fread_displacement(Crrfile, mPartition.partition.part_start + struct.calcsize(Ebr().get_const()), Temp_suberB)
    else:
        Fread_displacement(Crrfile, mPartition.partition.part_start, Temp_suberB)
        
    # Temp_suberB.display_info()
    
    #Se crea una variable para concatenar los reportes
    reporte = ''
    
    # Se obtiene el inicio de inodos
    inicioInodo = Temp_suberB.inode_start
    
    # Se lee el inodo que se mando
    inodoinicial = Table_inode()
    Fread_displacement(Crrfile, inicioInodo, inodoinicial)
    
    #Se agrega al reporte el inodo raiz
    reporte += bbreporteInodoHijos(inodoinicial, Crrfile, Temp_suberB)
    
    #Se cierra el archivo
    Crrfile.close()
    
    return reporte

def bbreporteInodoHijos(inodo, Crrfile, Temp_suberB):
    
    reporte = ''
    
    #Se agrega el inodo al reporte
    #reporte += inodo.generarInodoRep()
    
    #Se recorren todos los apuntadores de inodoinicio
    
    i = 0 #indice para leer cada apuntador del inodo
    
    while True:
        if (inodo.i_block[i] == -1):
            break
        readfolderbloq = inodo.i_block[i]
        # Se lee el bloque
        bloquefold = Folder_block()
        bloquearch = File_block()
        Fread_displacement(Crrfile, Temp_suberB.block_start + readfolderbloq * struct.calcsize(Folder_block().get_const()), bloquefold)
        Fread_displacement(Crrfile, Temp_suberB.block_start + readfolderbloq * struct.calcsize(File_block().get_const()), bloquearch)
                
        #if(bloquefold.b_content[0].b_name.decode() == '.'):    
        
        if(inodo.i_type == b'0'):
            reporte += bbreporteBloquesHijos(bloquefold, Crrfile, Temp_suberB, inodo.i_block[i])
        else:
            reporte += bbreporteBloquesHijos(bloquearch, Crrfile, Temp_suberB, inodo.i_block[i])
        i += 1
    
    return reporte

def bbreporteBloquesHijos(bloque, Crrfile, Temb_suberB, n):    
    reporte = ''
    
    #Se verifica si es un bloque de carpetas o de archivos
    if (not isinstance(bloque.b_content,(list,tuple))):
        reporte += bloque.generar_reporte(n)
        
    #Se recorre el bloque
    else:
        reporte += bloque.generarBloqueRep(n)
        for k in range(4):
            if(bloque.b_content[k].b_inodo == -1 or bloque.b_content[k].b_inodo == -2):
                continue
            if(bloque.b_content[k].b_name.decode() == '.' or bloque.b_content[k].b_name.decode() == '..'):
                continue
            inodo = Table_inode()
            Fread_displacement(Crrfile, Temb_suberB.inode_start + bloque.b_content[k].b_inodo * struct.calcsize(Table_inode().get_const()), inodo)
            reporte += bbreporteInodoHijos(inodo, Crrfile, Temb_suberB)
        
    return reporte


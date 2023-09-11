from copy import deepcopy
import os
from .Estructura.Mbr import *
from .Estructura.Ebr import *
from .Estructura.Load import *
from .Estructura.Partition import *


class FDisk:
    #Constructor---------------------------------------------------------------
    
    def __init__(self):
        self.size = 0
        self.path = ''
        self.name = ''
        self.unit = ''
        self.type = ''
        self.fit = ''
        self.delete = ''
        self.add = ''
        
    #Setters-------------------------------------------------------------------
    
    def set_size(self, size): #Definir el tamaño
        try:
            size = int(size)
            if size > 0:
                if(self.unit == 'B'):
                    size = size * 1
                elif(self.unit == 'K'):
                    size = size * 1024
                elif(self.unit == 'M'):
                    size = size * 1024 * 1024
                else:
                    print("\t Fdisk>>> Ocurrio un error al definir el tamaño")
                    return False
            else:
                print("\t Fdisk>>> El tamaño debe ser mayor a 0")
                return False
            
            #Se guarda el tamaño en bytes
            self.size = size
            return True
        except Exception as e:
            print("\t Fdisk>>> El tamaño debe ser un numero entero")
            return False
    
    def set_path(self, path): #Definir el path
        if(not os.path.exists(path)):
            print("\t Fdisk>>> El path no existe")
            return False
        
        if(not path.endswith('.dsk')):
            print("\t Fdisk>>> El path no tiene la extension .dsk")
            return False
        #Se guarda el path
        self.path = path
        return True
    
    def set_name(self, name): #Definir el nombre
        if name == None:
            print("\t Fdisk>>> Falta el nombre de la particion")
            return False
        self.name = name
        return True
    
    def set_unit(self, unit): #Definir el unit
        if unit == None:
            self.unit = "K"
            return True
        elif unit.lower() == 'b' or 'k' or 'm' :
            self.unit = unit[0].upper()
            return True
        print("\t Fdisk>>> El unit no es valido")
        return False
    
    def set_type(self, type): #Definir el type
        if type == None:
            self.type = "P"
            return True
        elif type.lower() == 'p' or 'e' or 'l' :
            self.type = type[0].upper()
            return True
        print("\t Fdisk>>> El type no es valido")
        return False
    
    def set_fit(self, fit): #Definir el fit
        if fit == None:
            self.fit = 'W'
            return True
        elif fit.lower() == 'bf' or 'ff' or 'wf' :
            self.fit = fit[0].upper()
            return True
        print("\t Fdisk>>> El fit no es valido")
        return False
    
    def set_delete(self, delete): #Definir el delete
        if delete == None:
            self.delete = None
            return False
        elif delete.lower() == 'full' :
            self.delete = delete.lower()
            return True
        print("\t Fdisk>>> El valor del delete no es valido")
        return False
    
    
    def set_add(self, add): #Definir el add
        try:
            if add == None:
                self.add = None
                return False
            else:
                add = int(add)
                if(self.unit == 'B'):
                    add = add * 1
                elif(self.unit == 'K'):
                    add = add * 1024
                elif(self.unit == 'M'):
                    add = add * 1024 * 1024
                #Se guarda el tamaño en bytes del add
                self.add = add
                return True
        except Exception as e:
            print("\t Fdisk>>> El valor del add no es valido")
            return False
        
    #Definir el FDISK----------------------------------------------------------
    
    def run(self, size, path, name, unit, type, fit, delete, add):
        if(delete != None and add != None):
            print("\t Fdisk>>> No se puede modificar el tamaño y eliminar una particion a la vez")
            return False
        
        #Se hace el unit de primero si viene un parametro add
        if(add != None):
            if(not self.set_unit(unit)): return False
            
        if(self.set_delete(delete)):
            if(not self.set_path(path)): return False
            if(not self.set_name(name)): return False
            if(self.delete_partitions()):
                print("\t Fdisk>> Se elimino la particion")
                return True
            return False
        elif(self.set_add(add)):
            if(not self.set_path(path)): return False
            if(not self.set_name(name)): return False
            if(self.change_space()):
                print("\t Fdisk>>> Se cambio el tamaño de la particion")
                return True
            return False
        else:
            if(not self.set_unit(unit)): return False
            if(not self.set_size(size)): return False
            if(not self.set_path(path)): return False
            if(not self.set_name(name)): return False
            if(not self.set_type(type)): return False
            if(not self.set_fit(fit)): return False
            
        if(self.create_partition()):
            print("\t Fdisk>>> Se creo la particion")
            return True
        return False
    
    #Crear una particion-------------------------------------------------------
    
    def create_partition(self):
        try:
            #Se crea el MBR temporal
            crr_mbr = Mbr()
            file = open(self.path, "rb+")
            
            #Se lee el objeto MBR y se igual al temporal
            Fread_displacement(file,0,crr_mbr)
            
            #se verifica si existe una particion con el mismo nombre
            if(crr_mbr.exist_partition(self.name)):
                print("\t Fdisk>>> Ya existe una particion con ese nombre")
                return False
            
            #Se valida que si viene una particion tipo E, no haya otra particion tipo E
            if(self.type == 'E'):
                for partition in crr_mbr.mbr_partition:
                    if(partition.part_type == b'E'):
                        print("\t Fdisk>>> Ya existe una particion extendida")
                        return False
            
            #Se valida que si viene un particion tipo L, ya haya una particion tipo E
            if(self.type == 'L'):
                partitionextendida = None
                existE = False
                for partition in crr_mbr.mbr_partition:
                    if(partition.part_type == b'E'):
                        partitionextendida = partition
                        existE = True
                        break
                if(not existE):
                    print("\t Fdisk>>> No existe una particion extendida para crear una particion logica")
                    return False
                              
                startp = partitionextendida.part_start               
                #Se verifica si es la primera particion logica
                aux_ebr = Ebr()
                Fread_displacement(file,startp,aux_ebr)
                if(aux_ebr.part_status == b'\0'):
                    if(self.size > partitionextendida.part_size):
                        print("\t Fdisk>>> No hay espacio suficiente para crear una particion logica")
                        return False
                    nuevo_ebr = Ebr()
                    nuevo_ebr.set_ebr('1', self.fit, startp, self.size, 0, self.name)
                    Fwrite_displacement(file,startp,nuevo_ebr)
                    file.close()
                    return True
                
                #Se verifican los ebr de la particion extendida
                lista_ebr = []
                tamaño_ocupado = 0
                while(startp != 0):
                    ebr = Ebr()
                    Fread_displacement(file,startp,ebr)
                    lista_ebr.append(ebr)
                    if(ebr.part_name.decode() == self.name):
                        print("\t Fdisk>>> Ya existe una particion con ese nombre")
                        return False
                    tamaño_ocupado += ebr.part_size
                    startp = ebr.part_next
                
                
                #Se verifica que todavia quede tamaño en la particion extendida
                if(tamaño_ocupado + self.size > partitionextendida.part_size):
                    print("\t Fdisk>>> No hay espacio suficiente para crear una particion logica")
                    return False
                
                #De aqui en adelante se agregan las condiciones para agregar una particion logica
                #Dependiendo del fit
                ebr_temp = Ebr()                
                diferencias = ebr_temp.get_freespace(lista_ebr, partitionextendida.part_size)
                indexplogica = 0
                espacioentrep = False
                if(partitionextendida.part_fit == b'F'):
                    for diferencia in diferencias:
                        if(diferencia >= self.size):
                            espacioentrep = True
                            break
                        indexplogica += 1
                elif(partitionextendida.part_fit == b'B'):
                    lista_min = []
                    for diferencia in diferencias:
                        if(diferencia >= self.size):
                            espacioentrep = True
                            lista_min.append(diferencia)
                    #Se obtiene el minimo de la lista
                    minimo = min(lista_min)
                    #Se obtiene el index del minimo
                    indexplogica = diferencias.index(minimo)
                elif(partitionextendida.part_fit == b'W'):
                    lista_max = []
                    for diferencia in diferencias:
                        if(diferencia >= self.size):
                            espacioentrep = True
                            lista_max.append(diferencia)
                    #Se obtiene el maximo de la lista
                    maximo = max(lista_max)
                    #Se obtiene el index del maximo
                    indexplogica = diferencias.index(maximo)
                
                if(espacioentrep == False):
                    print("\t Fdisk>>> No hay espacio suficiente para crear una particion logica")
                    return False
                #Se obtiene el ultimo ebr agregado al vector
                aux_ebr = lista_ebr[indexplogica]
                #Se crea el nuevo ebr
                nuevo_ebr = Ebr()
                #Se verifica si el indice encontrado es el ultimo ebr
                if(indexplogica == len(lista_ebr)-1):
                    nuevo_ebr.set_ebr('1', self.fit, aux_ebr.part_start + aux_ebr.part_size, self.size, 0, self.name)
                    lista_ebr.append(nuevo_ebr)
                else:
                    nuevo_ebr.set_ebr('1', self.fit, aux_ebr.part_start + aux_ebr.part_size, self.size, aux_ebr.part_next, self.name)
                    lista_ebr.insert(indexplogica+1, nuevo_ebr)
                #Se iguala el siguiente ebr al nuevo ebr
                lista_ebr[indexplogica].part_next = nuevo_ebr.part_start
                
                #Se escriben todos los ebr en el disco
                for ebr in lista_ebr:
                    Fwrite_displacement(file,ebr.part_start,ebr)
                
                file.close()
                return True
                        
                
            #Se determina el comienzo de las particiones            
            startp = len(Mbr().doSerialize())
            start = deepcopy(startp)
            size_particiones = 0
            indexp = 0
            
            for partition in crr_mbr.mbr_partition:
                if(partition.part_status == b'\0'):
                    break
                indexp += 1
                start = partition.part_start + partition.part_size
                size_particiones += partition.part_size
            if(indexp > 3):
                print("\t Fdisk>>> No se pueden crear mas particiones")
                return False
            
            #Se verifica que el tamaño de la particion sea menor al tamaño del disco
            if(size_particiones + self.size > crr_mbr.mbr_tamano):
                print("\t Fdisk>>> No queda espacio suficiente en el disco para almacenar la particion")
                return False
            
            #Se crea la nueva particion y se escribe en el disco
            new_partition = Partition()
            new_partition.set_partition('1', self.type, self.fit, start, self.size, self.name)
            crr_mbr.set_mbr_partition(new_partition, indexp)
            Fwrite_displacement(file,0,crr_mbr)
            if(new_partition.part_type == b'E'):
                #Se crea el EBR
                ebr = Ebr()
                Fwrite_displacement(file,new_partition.part_start,ebr)
                file.close()
                
            crr_mbr.display_info()
            file.close()
            return True
            
        except Exception as e:
            print(f"\t Fdisk>>> Error al crear la particion:{e}")
            return False
    
    def delete_partitions(self):
        #Se crea el MBR temporal
        crr_mbr = Mbr()
        file = open(self.path, "rb+")
        
        #Se lee el objeto MBR y se igual al temporal
        Fread_displacement(file,0,crr_mbr)
        
        #Se verifica si existe una particion con el mismo nombre
        existeP = False
        existePext = False
        particion_eliminar = None
        particion_extendida = None
        indexP_eliminar = 0
        #Se evalua si coincide alguna particion Extendida o Primaria
        for partition in crr_mbr.mbr_partition:
            if(partition.part_type.decode() == 'E'):
                existePext = True
                particion_extendida = partition
            if(partition.part_name.decode() == self.name):
                existeP = True
                particion_eliminar = partition
                break
            indexP_eliminar += 1
            
        #Si no encuentra coincidencia con el nombre, puede ser una particion logica        
        if(not existeP):
            if(not existePext):
                print("\t Fdisk>>> No existen coincidencias con el nombre de la particion")
                return False
            
            #Si hay una particion extendida se verifica que haya coincidencias con el nombre
            #Se verifican los ebr de la particion extendida
            startp = particion_extendida.part_start
            ebr = Ebr()
            lista_ebr = ebr.get_logic_partition(file, startp)
            indexp_logic = 0
            for cadaebr in lista_ebr:
                if cadaebr.part_name.decode() == self.name:
                    if(indexp_logic == 0):
                        print("\t Fdisk>>> No se puede eliminar el ebr inicial")
                        return False
                    
                    #Mensaje de confirmacion
                    confirm = input("\t Fdisk>>> Esta seguro que desea eliminar la particion? (Y/N): ")
                    if(confirm.lower() != 'y'): return False
                    
                    data = b'\0' * cadaebr.part_size
                    file.seek(cadaebr.part_start)
                    file.write(data)
                    if(indexp_logic > 0):
                        lista_ebr[indexp_logic-1].part_next = cadaebr.part_next
                        lista_ebr.remove(cadaebr)                        
                    break 
                indexp_logic += 1
            #Se escriben todos los ebr en el disco
            for ebr in lista_ebr:
                Fwrite_displacement(file,ebr.part_start,ebr)                
            file.close()
            return True
        
        if(particion_eliminar != None):
            if(particion_eliminar.part_type.decode() != 'L'):
                #Se elimina la particion  y se llena de \0 todo el espacio de la partición                
                startp = particion_eliminar.part_start
                
                #Mensaje de confirmacion
                confirm = input("\t Fdisk>>> Esta seguro que desea eliminar la particion? (Y/N): ")
                if(confirm.lower() != 'y'): return False
                
                #Data vacia
                data = b'\0' * particion_eliminar.part_size
                file.seek(startp)
                file.write(data)      
                
                particion_vacia = Partition()
                crr_mbr.set_mbr_partition(particion_vacia, indexP_eliminar)
                Fwrite_displacement(file,0,crr_mbr)
                file.close()
                return True
        return False
    
    def change_space(self):
        #Se crea el MBR temporal
        crr_mbr = Mbr()
        file = open(self.path, "rb+")
        
        #Se lee el objeto MBR y se igual al temporal
        Fread_displacement(file,0,crr_mbr)
        
        #Se verifica si existe una particion con el mismo nombre
        existeP = False
        existePext = False
        particion_cambiar = None
        particion_extendida = None
        indexP_cambiar = 0
        #Se evalua si coincide alguna particion Extendida o Primaria
        for partition in crr_mbr.mbr_partition:
            if(partition.part_type.decode() == 'E'):
                existePext = True
                particion_extendida = partition
            if(partition.part_name.decode() == self.name):
                existeP = True
                particion_cambiar = partition
                break
            indexP_cambiar += 1
            
        #Si no encuentra coincidencia con el nombre, puede ser una particion logica        
        if(not existeP):
            if(not existePext):
                print("\t Fdisk>>> No existen coincidencias con el nombre de la particion")
                return False
            #Primero se verifican conincidencias en el nombre
            startp = particion_extendida.part_start
            ebr = Ebr()
            lista_ebr = ebr.get_logic_partition(file, startp)
            indexp_logic = 0
            for cadaebr in lista_ebr:
                if cadaebr.part_name.decode() == self.name:
                    #Se verifica que al reducir espacio todavia quede
                    if(cadaebr.part_size + self.add <= 0):
                        print("\t Fdisk>>> No Hay sufienciente espacio para reducir la particion")
                        return False
                    #Se verifica que al agregar espacio no se pase a la siguiente particion
                    if(indexp_logic < len(lista_ebr)-1):
                        particion_siguiente = lista_ebr[indexp_logic+1]
                        if(cadaebr.part_start + cadaebr.part_size + self.add > particion_siguiente.part_start):
                            print("\t Fdisk>>> No se puede agregar espacio a la particion")
                            return False
                    
                    particion_nuevosize = Ebr()
                    particion_nuevosize.set_ebr(cadaebr.part_status.decode(), cadaebr.part_fit.decode(), cadaebr.part_start, cadaebr.part_size + self.add, cadaebr.part_next, cadaebr.part_name.decode())
                    
                    #Se sustituye el ebr en la lista de ebrs
                    lista_ebr[indexp_logic] = particion_nuevosize
                    break
                indexp_logic += 1
            #Se escriben todos los ebr en el disco
            for ebr in lista_ebr:
                Fwrite_displacement(file,ebr.part_start,ebr)
            file.close()
            return True
                    
            
        
        #Cuando es una particion Primaria o Extendida
        if(particion_cambiar != None):
            if(particion_cambiar.part_type.decode() != 'L'):
                if(particion_cambiar.part_size + self.add < 0):
                    print("\t Fdisk>>> No se puede reducir la particion")
                    return False
                
                #Se verifica que al agregar espacio no se pase a la siguiente particion
                if(indexP_cambiar < 3):
                    particion_siguiente = crr_mbr.mbr_partition[indexP_cambiar+1]
                    if(particion_cambiar.part_start + particion_cambiar.part_size + self.add > particion_siguiente.part_start):
                        print("\t Fdisk>>> No se puede agregar espacio a la particion")
                        return False
                
                particion_nuevosize = Partition()
                particion_nuevosize.set_partition('1', particion_cambiar.part_type, particion_cambiar.part_fit, particion_cambiar.part_start, particion_cambiar.part_size + self.add, particion_cambiar.part_name)
                
                #Se sustituye esa particion con el nuevo tamaño en el mbr
                crr_mbr.set_mbr_partition(particion_nuevosize, indexP_cambiar)
                Fwrite_displacement(file,0,crr_mbr)
                file.close()
        
            
            
        
        
                    
        
        
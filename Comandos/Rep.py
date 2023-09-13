#COMANDO REPORTE
import os
from .Estructura.Load import *
from .Estructura.Mbr import *
from .Estructura.Ebr import *
from .Estructura.Partition import *
from .Estructura.Super_block import *
from .Estructura.Table_inode import *
from .Estructura.Folder_block import *
from .Estructura.File_block import *
from Utilities.Utilities import *
from Global.Global import *

class Rep():
    
    #Contructor --------------------------------------------------------------------------------------
    
    def __init__(self):
        self.name = None
        self.path = None
        self.id = None
        self.ruta = None
        
    #Setters-----------------------------------------------------------------------------------------
    
    def set_name(self, name):
        if name == None or name == '':
            printError("\t Rep>>> Falta el nombre del reporte\n")
            return False
        self.name = name
        return True

    def set_path(self, path):
        if path == None or path == '':
            printError("\t Rep>>> Falta el path del reporte\n")
            return False
        folder_path = os.path.dirname(path)
        os.makedirs(folder_path, exist_ok=True)
        self.path = path
        return True
    
    def set_id(self, id):
        if id == None or id == '':
            printError("\t Rep>>> Falta el id de la particion\n")
            return False
        self.id = id
        return True
    
    def set_ruta(self, ruta):
        self.ruta = ruta
        return True
    
    #Definir el REP--------------------------------------------------------------------------------
    
    def run(self, name, path, id, ruta):
        if(not self.set_name(name)): return False
        if(not self.set_path(path)): return False
        if(not self.set_id(id)): return False
        if(not self.set_ruta(ruta)): return False
        
        if(self.crear_reporte()):
            printText("\t Rep>>> Reporte creado con exito\n")
            return True
        return False
    
    #Crear un reporte-----------------------------------------------------------------------------------
    
    def crear_reporte(self):
        #Se verifica que exista la particion
        crrpartition = buscar_particion(self.id)
        
        if crrpartition == None:
            printError("\t Rep>>> No existe la particion\n")
            return False
        
        #Se hace un switch para saber que reporte se va a crear
        match self.name.lower():
            case 'mbr':
                if self.reporte_mbr(crrpartition):
                    return True
                return False
            case 'disk':
                if self.reporte_disk(crrpartition):
                    return True
                return False
            case 'inode':
                if self.reporte_inode(crrpartition):
                    return True
                return False
            case 'journaling':
                if self.reporte_journaling(crrpartition):
                    return True
                return False
            case 'block':
                if self.reporte_block(crrpartition):
                    return True
                return False
            case 'bm_inode':
                if self.reporte_bm_inode(crrpartition):
                    return True
                return False
            case 'bm_block':
                if self.reporte_bm_block(crrpartition):
                    return True
                return False
            case 'tree':
                if self.reporte_tree(crrpartition):
                    return True
                return False
            case 'sb':
                if self.reporte_sb(crrpartition):
                    return True
                return False
            case 'file':
                if self.reporte_file(crrpartition):
                    return True
                return False
            case 'ls':
                if self.reporte_ls(crrpartition):
                    return True
                return False
            case _:
                printError("\t Rep>>> No existe el reporte\n")
                return False

    #Reporte MBR --------------------------------------------------------------------------------------
    def reporte_mbr(self, mtpartition):
        try:
            #Se abre el archivo con el path donde esta ubicado el Disco
            file = open(mtpartition.path, "rb+")
            crr_mbr = Mbr()
            
            #Se lee el Mbr
            Fread_displacement(file, 0, crr_mbr)
            
            #Se crea el reporte
            reporte = "digraph G{ rankdir=TB  node [shape=plaintext]"
            #Se crea la tabla
            reporte += "tabla[label = <<table border='0' cellborder='1' cellspacing='0'>"
            #Se crea el encabezado
            reporte += "<tr><td colspan='2' bgcolor='#5004a4'><font color='white'><b>REPORTE DEL MBR</b></font></td></tr>"
            
            reporte += crr_mbr.generar_reporte(mtpartition.path)
            
            #Se cierra la tabla
            reporte += "</table>>];}"
            
            
            #Se cierra el archivo
            file.close()
            
            if self.CreateGraph(reporte):
                return True
            
            return False
        except Exception as e:
            printError("\t Rep>>> Error al crear el reporte MBR\n")
            print(e)
            return False
    
    #Reporte DISK --------------------------------------------------------------------------------------
    def reporte_disk(self, mtpartition):
        try :
            #Se abre el archivo con el path donde esta ubicado el Disco
            file = open(mtpartition.path, "rb+")
            crr_mbr = Mbr()
            
            #Se lee el Mbr
            Fread_displacement(file, 0, crr_mbr)
            
            #Se crea el reporte
            reporte = "digraph G{ rankdir=TB  node [shape=plaintext]"
            #Se crea la tabla
            reporte += "tabla[label = <<table border='1' cellborder='1' cellspacing='0'>"

            completesize = crr_mbr.mbr_tamano
            
            #porcetaje del mbr
            
            #Se crea el bloque MBR
            reporte += "<tr><td rowspan='2' ><b>MBR</b></td>"
            
            #se recorren las particiones
            seek = 133
            for partition in crr_mbr.mbr_partition:
                if(partition.part_status.decode() == '0'):
                    porcentaje = ((partition.part_start - seek) * 100) / completesize
                    reporte += "<td rowspan='2' width='" + str(porcentaje) + "%'><b>Libre " + str(porcentaje) +"%" +" del disco</b></td>"
                    seek = partition.part_start + partition.part_size
                    continue
                #Se calcula el porcentaje de la particion
                porcentaje = (partition.part_size * 100) / completesize
                
                if partition.part_type.decode().lower() != 'e':
                    #Se crea el bloque de la particion
                    reporte += "<td rowspan='2' width='" + str(porcentaje) + "%'><b> Primaria " + str(porcentaje) + "%" +" del disco</b></td>"
                    seek = partition.part_start + partition.part_size
                    continue
                
                startp = partition.part_start
                cont = 0
                while (startp != -1):
                    if(startp > seek):
                        porcentaje = ((startp - seek) * 100) / completesize
                        reporte += "<td width='" + str(porcentaje) + "%'><b>Libre " + str(porcentaje) +"%" +" del disco</b></td>"
                        seek = startp
                        cont += 1
                        continue
                    ebr = Ebr()
                    Fread_displacement(file, startp, ebr)                    
                    porcentaje = (ebr.part_size * 100) / completesize
                    #Se crea el bloque de la particion
                    reporte += "<td>EBR</td><td width='" + str(porcentaje) + "%'><b> Logica " + str(porcentaje) + "%"+" del disco</b></td>"
                    startp = ebr.part_next
                    seek = startp
                    cont += 2            
            reporte += "</tr>"
            reporte += "<tr>"                
            reporte += "<td colspan='" + str(cont) + "'><b>Extendida</b></td>"
            reporte += "</tr>"
            #Se cierra la tabla
            reporte += "</table>>];}"
            
            
            #Se cierra el archivo
            file.close()
            
            if self.CreateGraph(reporte):
                return True
            
            return False
            
        
        except Exception as e:
            printError("\t Rep>>> Error al crear el reporte MBR\n")
            print(e)
            return False
    
    #Funcion para crear la grafica con graphviz---------------------------------------------------------------------------
    
    def CreateGraph(self, reporte):
        try:
            # Obtener el nombre del archivo y la extensión
            nombre_archivo, extension = os.path.splitext(os.path.basename(self.path))
            #le quitamos el punto a la extension
            extension = extension[1:]           
            
            # ESCRIBO EL ARCHIVO TXT 
            folder_path = os.path.dirname(self.path)
            documento = folder_path + '/' + nombre_archivo + ".txt"

            with open(documento, 'w') as grafica:
                grafica.write(reporte)

            # GENERO LA IMAGEN
            
            os.system("dot -T" + extension + " " + documento + " -o " + self.path)
            
            return True
        except Exception as e:
            printError("\t Rep>>> Error al crear el reporte MBR\n")
            print(e)
            return False
    
        
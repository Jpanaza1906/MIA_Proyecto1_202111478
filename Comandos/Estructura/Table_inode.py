import ctypes
import struct
from .Load import *

const = "i i i 10s 10s 10s 15i 1s 3s"

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
        ('i_type', ctypes.c_char), # 0 = Carpeta, 1 = Archivo
        ('i_perm', ctypes.c_char * 3)
    ]
    
    #Constructor----------------------------------------------------------------
    
    def __init__(self):
        self.i_uid = -1
        self.i_gid = -1
        self.i_size = -1
        self.i_atime = b'\0'*10
        self.i_ctime = b'\0'*10
        self.i_mtime = b'\0'*10
        self.i_block = (ctypes.c_int * 15)(*[-1] * 15)
        self.i_type = b'\0'
        self.i_perm = b'\0'*3
        
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
        
    def set_i_block(self, index, block): # Definir un bloque especifico
        self.i_block[index] = block
        
    def set_i_type(self, type): # Definir el tipo
        self.i_type = coding_str(type, 1)
        
    def set_i_perm(self, perm): # Definir los permisos
        self.i_perm = coding_str(perm, 3)
        
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
        print("======================Inode Info=====================")
        print(f"i_uid: {self.i_uid}")
        print(f"i_gid: {self.i_gid}")
        print(f"i_size: {self.i_size}")
        print(f"i_atime: {self.i_atime.decode()}")
        print(f"i_ctime: {self.i_ctime.decode()}")
        print(f"i_mtime: {self.i_mtime.decode()}")
        print(f"i_block: {list(self.i_block)}")
        print(f"i_type: {self.i_type.decode()}")
        print(f"i_perm: {self.i_perm.decode()}")
        print("----------------------------------------------------")
        
    #Reportes-------------------------------------------------------------------
    
    def generar_reporte(self):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Inodo" + str(self.i_uid) + "[ label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\">Inodo " + str(self.i_uid) + "</td></tr>"
        reporte += "<tr><td>uid</td><td>" + str(self.i_uid) + "</td></tr>"
        reporte += "<tr><td>gid</td><td>" + str(self.i_gid) + "</td></tr>"
        reporte += "<tr><td>size</td><td>" + str(self.i_size) + "</td></tr>"
        reporte += "<tr><td>atime</td><td>" + self.i_atime.decode() + "</td></tr>"
        reporte += "<tr><td>ctime</td><td>" + self.i_ctime.decode() + "</td></tr>"
        reporte += "<tr><td>mtime</td><td>" + self.i_mtime.decode() + "</td></tr>"
        reporte += "<tr><td>block</td><td>" + str(list(self.i_block)) + "</td></tr>"
        reporte += "<tr><td>type</td><td>" + self.i_type.decode() + "</td></tr>"
        reporte += "<tr><td>perm</td><td>" + self.i_perm.decode() + "</td></tr>"
        reporte += "</table>>];"
        
        return reporte
    
    def generarInodoRep(self):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Inodo" + str(self.i_uid) + " [label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\" port=\"0\">Inodo " + str(self.i_uid) + "</td></tr>"
        for i in range(15):
            reporte += "<tr><td>AD" + str(i+1) + "</td><td port=\"" + str(i+1) + "\">" + str(self.i_block[i]) + "</td></tr>"
            
        reporte += "</table>>];"
        
        return reporte
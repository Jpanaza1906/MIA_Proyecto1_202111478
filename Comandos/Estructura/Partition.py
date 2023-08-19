import ctypes
import struct
from .Utilities import * 

# Estructura de una particion
const = "1s 1s 1s I I 16s"
class Partition(ctypes.Structure):
    _fields_ = [
        ('part_status', ctypes.c_char), # 1 byte
        ('part_type', ctypes.c_char), # 1 byte
        ('part_fit', ctypes.c_char), # 1 byte
        ('part_start', ctypes.c_int), # 4 bytes
        ('part_size', ctypes.c_int), # 4 bytes
        ('part_name', ctypes.c_char * 16) # 16 bytes
    ]
    #Constructor
    def __init__(self):
        self.part_status = b'\x00'
        self.part_type = b'\x00'
        self.part_fit = b'\x00'
        self.part_start = 0
        self.part_size = 0
        self.part_name = b'\x00'*16
    
    #Setters
    def set_part_status(self, status):
        self.part_status = coding_str(status, 1)
    
    def set_part_type(self, type):
        self.part_type = coding_str(type, 1)
    
    def set_part_fit(self, fit):
        self.part_fit = coding_str(fit, 1)
    
    def set_part_start(self, start):
        self.part_start = start
    
    def set_part_size(self, size):
        self.part_size = size
    
    def set_part_name(self, name):
        self.part_name = coding_str(name, 16)
        
    def set_partition(self, status, type, fit, start, size, name):
        self.set_part_status(status)
        self.set_part_type(type)
        self.set_part_fit(fit)
        self.set_part_start(start)
        self.set_part_size(size)
        self.set_part_name(name)
    
    #Get const
    def get_const(self):
        return const
    
    #Serialize
    def doSerialize(self):
        serialize = struct.pack(
            const,
            self.part_status,
            self.part_type,
            self.part_fit,
            self.part_start,
            self.part_size,
            self.part_name
        )
        return serialize
    
    def doDeseralize(self, data):
        unpacked = struct.unpack(const, data)
        self.part_status = unpacked[0]
        self.part_type = unpacked[1]
        self.part_fit = unpacked[2]
        self.part_start = unpacked[3]
        self.part_size = unpacked[4]
        self.part_name = unpacked[5]
    
    def display_info(self):
        print("Status: ", self.part_status)
        print("Type: ", self.part_type)
        print("Fit: ", self.part_fit)
        print("Start: ", self.part_start)
        print("Size: ", self.part_size)
        print("Name: ", self.part_name)
        print("")
    
    
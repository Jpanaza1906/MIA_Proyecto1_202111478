#Se excribe el archivo en la particion y disco seleccionado
def Fwrite_displacement(file, displacement, obj):
    data = obj.doSerialize()
    file.seek(displacement)
    file.write(data)
    
def Fread_displacement(file, displacement, obj):
    try:
        file.seek(displacement)
        data = file.read(len(obj.doSerialize()))
        obj.doDeserialize(data)
    except Exception as e:
        #print(f"Error:{e} while reading in: ", displacement)
        pass

def Fcreate_file(file_name):
    try:
        fileOpen = open(file_name, "wb")
        fileOpen.close()
        return False
    except Exception as e:
        print(f"Error:{e} while creating file")
        return True

def Winit_size(file, size):
    buffer = b'\0' * 1024 #un kilobyte
    size = int(size/1024) #se deja en la unidad
    
    for _ in range(size):
        file.write(buffer)

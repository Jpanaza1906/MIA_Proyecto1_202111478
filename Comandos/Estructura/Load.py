# Funciones para escribir y leer en un archivo binario--------------------------------

def Fwrite_displacement(file, displacement, obj): #Escribir en un archivo binario
    data = obj.doSerialize()
    file.seek(displacement)
    file.write(data)
    
def Fread_displacement(file, displacement, obj): #Leer en un archivo binario
    try:
        file.seek(displacement)
        data = file.read(len(obj.doSerialize()))
        obj.doDeserialize(data)
    except Exception as e:
        #print(f"Error:{e} while reading in: ", displacement)
        pass

def Fcreate_file(file_name): #Crear un archivo binario
    try:
        fileOpen = open(file_name, "wb")
        fileOpen.close()
        return False
    except Exception as e:
        print(f"Error:{e} while creating file")
        return True

def Winit_size(file, size): #inicializar el tamaño del archivo
    buffer = b'\0' * 1024 #un kilobyte
    size = int(size/1024) #se deja en la unidad
    
    for _ in range(size):
        file.write(buffer)

# Utilidades-----------------------------------------------------

def coding_str(string, size): #Codificar un string a un archivo binario
    return string.encode('utf-8')[:size].ljust(size, b'\x00')

# ------------------------------------------MOUNTED PARTITIONS------------------------------------------#
# [id, particion, path, islogic, journaling]
mounted_partitions = []


class MountedPartition():
    # Constructor----------------------------------------------------------------
    def __init__(self, id, partition, path, islogic, journaling):
        self.id = id
        self.partition = partition
        self.path = path
        self.islogic = islogic
        self.journaling = journaling


def buscar_particion(id):
    for data in mounted_partitions:
        if (data.id == id):
            return data
    return None


# ------------------------------------------USER SESSION------------------------------------------#
# Se guarda la sesion del usuario
user_session = []

class UserActive():
    # Constructor----------------------------------------------------------------
    def __init__(self, num, tipo, grupo, user, contraseña,fblock, partitionId):
        self.num = num
        self.tipo = tipo
        self.gruporupo = grupo
        self.user = user
        self.contraseña = contraseña
        self.numfblock = fblock
        self.partitionId = partitionId
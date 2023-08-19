#COMANDO EXECUTE

import os


class Execute():
    def __init__(self, path):
        self.path = path
    
    def existe_archivo(self):
        if not os.path.exists(self.path):
            print("No existe el archivo")
            return False
        else:
            return True
    

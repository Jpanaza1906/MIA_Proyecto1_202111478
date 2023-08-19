from Analizador.lexico import *
from Analizador.sintactico import *
from Comandos.Mkdisk import *
from Comandos.Execute import *

mkglobal = None
def exe_command(result):
    global mkglobal
    if('command' in result):
        if(result['command'] == 'execute'):
            if('path' in result):
                exe = Execute(result['path'])
                if(exe.existe_archivo()):
                    with open(exe.path, "r") as file:
                        lines = file.readlines()
                        for line in lines:
                            print(line)
                            if(line.strip().lower() == 'rep'):                                
                                if(mkglobal != None):
                                    mkglobal.leer_disco()
                            else:
                                result = parser.parse(line)
                                exe_command(result)
        elif(result['command'] == 'mkdisk'):
            if('size' in result and 'path' in result):
                size = result['size']
                path = result['path']
                fit = None
                unit = None
                if('fit' in result):
                    fit = result['fit']
                if('unit' in result):
                    unit = result['unit']
                mk = Mkdisk()
                mk.set_mkdisk(size, path, fit, unit)
                mk.crear_disco()
                mkglobal = mk
           
if __name__ == '__main__':
    lex = lex.lex()
    parser = yacc.yacc()
    while True:
        try:
            s = input('josep-ubu@Leon-Ubuntu: ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        exe_command(result)   
                
                    
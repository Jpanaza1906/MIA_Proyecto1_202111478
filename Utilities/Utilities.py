def printConsole(text): print("\033[36m{}\033[00m" .format(text))

def printError(error): print("\033[91m{}\033[00m" .format(error))

def printSuccess(success): print("\033[1;32m{}\033[00m" .format(success))

def printWarning(warning): print("\033[93m{}\033[00m" .format(warning))

def printTitle(title): print("\033[1;33m{}\033[00m" .format(title))

def printSubtitle(subtitle): print("\033[1;34m{}\033[00m" .format(subtitle))

def printComment(comment): print("\033[1;35m{}\033[00m" .format(comment))

def printInfo(info): print("\033[1;36m{}\033[00m" .format(info))

def printHelp(help): print("\033[1;37m{}\033[00m" .format(help))

def printText(text): print("\033[1;38m{}\033[00m" .format(text))

#inputs con color
def inputConsole(text): return input("\033[1;34m{}\033[00m" .format(text))

def inputWarning(text): return input("\033[93m{}\033[00m" .format(text))

from os import system, name

def limparTerminal():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
import re

arq = open("calc.c", "r")
tokens = []
operadores = ["+", "-", "*", "/"]
reserva = ["const", "while", "While", "WHILE","if","IF","iF","If", "#include", "<stdio.h>",
            "return", "int", "float", ";"]
compara = [">","<", "<=",">=","==","!="]
literal = ["''"]
atribui = ["="]
delimita = ["{", "}", "[", "]"]

#divide inicialmente os tokens

for x in arq:
    x = x.strip()
    lista = x.split()
    for y in lista:
        y = y.strip()
        if(";" in y):
            y = y.split(";")
            tokens.append(y[0])
            tokens.append(";")
        else:
            tokens.append(y)

#mostrará a partir de que tipo são

for z in tokens:
    if z in operadores: 
        print(z +"      - operador")
    elif z in reserva: 
        print(z +"      - reservada")
    elif z in compara:
        print(z +"      - comparação")
    elif (re.findall(r'\d', z)) != [] :
        print(z +"      - número")
    elif (re.findall(r'"[a-z]"',z)) != []:
        print(z +"      - literal")
    elif z in atribui:
        print(z + "     - atribuição")
    elif z in delimita:
        print(z + "     - delimitador")
    else:
        print(z + "     - variável ou função")





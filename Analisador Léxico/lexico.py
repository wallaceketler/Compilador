import re

arq = open("Código 1.txt", "r")
tokens = []
operadores = ["+", "-", "*", "/"]
reserva = ["const", "while", "While", "WHILE","if","IF","iF","If", "#include", "<stdio.h>",
            "return", "int", "float", ";", ","]
compara = [">","<", "<=",">=","==","!="]
literal = ["''"]
atribui = ["="]
delimita = ["{", "}", "[", "]", "(", ")"]

#divide inicialmente os tokens

for x in arq:
    x = x.strip()
    lista = x.split()
    for y in lista:
        y = y.strip()
        if(";" in y):
            if("(") in y:
                if(",") in y: 
                    aux = 1
                y = y.split("(")                #separa string em antes do '(' e depois do '('
                tokens.append(y[0])             #adiciono o antes do '('
                tokens.append("(")              #adiciono o '('
                y[1] = y[1].strip()             #tiro o lixo do depois do '('
                y[1] = y[1].split(";")          #divido o depois do '(' em antes do ';' e depois do ';'
                w = y[1][0].split(")")          #tiro o lixo do antes do ';'
                if aux == 1:                    #se tiver ',' em y
                    z = w[0].split(",")         #divido antes do ',' em antes e depois do ','        
                    tokens.append(z[0])         #adiciono o antes do ','
                    tokens.append(",")          #adiciono o ','
                    tokens.append(z[1])         #adiciono o antes do ')'
                else:                           #se não tiver ',' em y
                    tokens.append(w[0])         #adiciono o antes do ';'
                tokens.append(")")
                tokens.append(";")                      
            else:
                y = y.split(";")
                tokens.append(y[0])
                tokens.append(";")
            aux = 0                  
        elif("(" in y):                                      #main()    
            y = y.split("(")                        
            tokens.append(y[0])
            tokens.append("(")
            tokens.append(")")
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
    elif ((re.findall(r'\d', z)) != []):
        print(z +"      - número")
    elif (re.match('".*"',z)):
        print(z +"      - literal")
    elif z in atribui:
        print(z + "     - atribuição")
    elif z in delimita:
        print(z + "     - delimitador")
    else:
        print(z + "     - variável ou função")

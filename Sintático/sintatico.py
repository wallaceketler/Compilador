#Analisador léxico:

import re

arq = open("calc.c", "r")
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
    lista = x.split()                         #aqui está dividindo quando acha espaço branco
    for y in lista:
        y = y.strip()
        if(";" in y):   #caso em que temos ; na linha
            if("(") in y:   #caso em que temos ( ) na linha
                if(",") in y:   #caso em que temos , na linha
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
        elif("(" in y):  #main()    
            y = y.split("(")                        
            tokens.append(y[0])
            tokens.append("(")
            tokens.append(")")
        else:
            tokens.append(y)

#Analisador sintático:
    #O analisador sintático deve ser capaz de reconhecer se a ordem com que o código está montado
    #está correta, por exemplo, depois do #include deve obrigatoriamente vir uma biblioteca.
    #Não é papel dele ver se a biblioteca está correta...
print(" ")
print("Análise Sintática: ")
print(" ")
tam = 0
conta_chave_abre = 0
conta_chave_fecha = 0
conta_uso_chave = 0
fim_linha = ''          #usado para determinar fim de linha quando atribuição tem virgula
fim_virgula = ''        #usado para verificarmos se chegarmos em vírgula em atribuições
item_atual_linha = 0;   #usado para determina item atual da linha de atribuição c/ virgula
verifica_falha = 0;


for i in range(0,len(tokens)):

        verifica_variavel = 0
        verifica_falha = 0
        item_atual_linha = 0
        fim_linha = ''
        #inclusão de bibliotecas
        if(tokens[i] == "#include"):
            tam = len(tokens[i+1])
            if(tokens[i+1][0]) == '<' and (tokens[i+1][tam-1] == '>'):
                print("Linha ok")
                print(tokens[i] + " " + tokens[i+1])    
            else:    
                print("ERRO SINTÁTICO - inclusão de bibliotecas")
        #########################
        #começo com int
        if(tokens[i] == "int"): 
            #pode ser main
            if(tokens[i+1] == "main" and tokens[i+2] == "(" and tokens[i+3] == ")" and tokens[i+4] == '{'):
                print("Linha ok")
                print(tokens[i]+ " "  + tokens[i+1]+ " "  + tokens[i+2]+ " "  + tokens[i+3])
                conta_uso_chave  = conta_uso_chave + 1
                verifica_variavel = 1
                continue
                ##falta verificar se abriu e fechou chaves do main
            #pode ser variável
            elif(re.match('.*',tokens[i+1]) and tokens[i+1] != "main" and tokens[i+2] != '(') :
                #pode estar apenas com o valor e ponto e vírgula
                if(tokens[i+2] == ';'):
                    print("Linha ok")
                    print(tokens[i]+ " "  + tokens[i+1]+ " "  + tokens[i+2])
                    verifica_variavel = 1
                    continue
                #pode estar atribuindo valor na declaração
                elif(tokens[i+2] == '='):
                    ##pode estar com apenas um valor
                    if(re.match('.*',tokens[i+3]) or re.match('\d',tokens[i+3])):
                        ##pode estar com apenas um valor
                        if(tokens[i+4] == ';'):
                            print("Linha ok")
                            print(tokens[i]+ " "  + tokens[i+1]+ " "  + tokens[i+2]+ " "  + tokens[i+3]+ " "  + tokens[i+4])
                            verifica_variavel = 1
                            continue
                        ##pode ter operação simples
                        if(tokens[i+4] in operadores):
                            if(re.match('.*',tokens[i+5]) or re.match('\d',tokens[i+5])):
                                if(tokens[i+6] == ';'):
                                    print("Linha ok")
                                    print(tokens[i]+ " "  + tokens[i+1]+ " "  + tokens[i+2]+ " "  + tokens[i+3]+ " "  + tokens[i+4]+ " " 
                                          +tokens[i+5]+ " "  + tokens[i+6])
                                    verifica_variavel = 1
                                    continue
                        ##pode ter operação tripla
                        if(tokens[i+4] in operadores):
                            if(re.match('.*',tokens[i+5]) or re.match('\d',tokens[i+5])):
                                if(tokens[i+6] in operadores):
                                    if(re.match('.*',tokens[i+7]) or re.match('\d',tokens[i+7])):
                                        if(tokens[i+8] == ';'):
                                            print("Linha ok")
                                            print(tokens[i]+ " "  + tokens[i+1]+ " "  + tokens[i+2]+ " "  + tokens[i+3]+ " "  + tokens[i+4]+ " " 
                                                +tokens[i+5]+ " "  + tokens[i+6]+ " "  + tokens[i+7]+ " "  + tokens[i+8])
                                            verifica_variavel = 1
                                            continue
                        ##pode ter declarações com vírgula
                        if(tokens[i+4] == ','):
                            while(fim_linha != ';'):
                                if((re.match('.*',tokens[i+1+item_atual_linha]) or re.match('\d',tokens[i+1+item_atual_linha])) and 
                                (tokens[i+2+item_atual_linha] == '=') and 
                                (re.match('.*',tokens[i+3+item_atual_linha]) or re.match('\d',tokens[i+3+item_atual_linha])) and
                                (tokens[i+4+item_atual_linha] == ',' or tokens[i+4+item_atual_linha == ';'])):
                                    fim_linha = tokens[i+item_atual_linha+4]
                                    item_atual_linha = item_atual_linha+4
                                else:
                                    verifica_falha = 1;
                                    break
                            if(verifica_falha == 1):
                                print("ERRO SINTÁTICO - declaração de variável ou função")
                                continue
                            else:
                                verifica_variavel = 1
                                print("Linha ok")
                                for y in range(0,item_atual_linha+1):
                                    print(tokens[i+y] +' ', end="")  
                                print()
            if(verifica_variavel == 0):
                print("ERRO SINTÁTICO - declaração de variável ou função")                                                            
        #pode começar com variável qualquer
        if(re.match('.*',tokens[i]) and tokens[i-1] == ';' and tokens[i]!='}' and tokens[i]!='return'):
            #print("->" +tokens[i]+tokens[i+3])
            while(fim_linha != ';'):
                if((re.match('.*',tokens[i+2+item_atual_linha]) or re.match('\d',tokens[i+2+item_atual_linha])) and (tokens[i+3+item_atual_linha] in operadores or tokens[i+3+item_atual_linha] == ';')):
                    fim_linha = tokens[i+item_atual_linha+3]
                    item_atual_linha = item_atual_linha+2
                else:
                    verifica_falha = 1
                    break
            if(verifica_falha == 1):
                print("ERRO SINTÁTICO - atribuição errada")
                continue
            else:
                verifica_variavel = 1 #caso em que deu certo  
                print("Linha OK")                  
                for y in range(0,item_atual_linha+3):
                    print(tokens[i+y] +' ', end="")
                    if(tokens[i+y] == ';'):
                        break
                print()
        
        #########################
        #começo com return
        if(tokens[i] == "return"):
            #pode ser valor
            if(re.match('\d',tokens[i+1]) and tokens[i+2] == ';'):
                print("Linha ok")
                print(tokens[i]+ " "  + tokens[i+1]+ " "  + tokens[i+2])
            else:
                print("ERRO SINTÁTICO - retorno de função ausente ou mal declarado")
        #chaves
        if(tokens[i] == "{"):
            conta_chave_abre = conta_chave_abre + 1
        if(tokens[i] == "}"):
            conta_chave_fecha = conta_chave_fecha + 1

if((conta_chave_abre+conta_chave_fecha)%2 == 0 and (conta_chave_abre == conta_uso_chave)):
    print("chaves ok")
else:
    print("ERRO SINTÁTICO - Chaves mal colocadas")
#########################



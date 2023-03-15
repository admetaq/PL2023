import re
import json
import math

def media (lista):
    return sum(lista) / len(lista)

def unique(items):
    result = []
    for x in items:
        if x not in result:
            result.append(x)
        
    return result

def summarize(numbers):
    if not numbers:
        return {}
    mean = media(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    std_dev = variance ** 0.5
    return {"variance": variance, "median": sorted(numbers)[len(numbers)//2], "std_dev": std_dev}



def is_aggregate_function(string):
    valid_aggregate_functions = ["sum", "min", "max", "media","len", "sorted", "reversed", "summarize", "unique","prod"]
    if string in valid_aggregate_functions:
        return True
    return False

def applyFunction(funcName, value):
    if funcName == "media":
        return media(value)
    elif funcName == "summarize":
        return summarize(value)
    elif funcName == "unique":
        return unique(value)
    elif funcName == "prod":
        return math.prod(value)
    
    if funcName in  ["sum", "min", "max", "len", "sorted", "reversed"]:
        function = getattr(__builtins__, funcName)
        return function(value)
   



ficheiro = input("Insira o nome do ficheiro: ")
ficheiro = re.sub(r"\s","",ficheiro)
if not re.search(r"\.csv$",ficheiro):
    print("Erro: Programa válido apenas para ficheiros csv.")
    exit(1)

nomeSemCsv = re.sub(r"\.csv","", ficheiro)

try:
    f = open(ficheiro,"r")
except IOError: 
    print ("Erro: Ficheiro não existe.")
    exit(1)

dict = {}
dict[nomeSemCsv] = []

linha = f.readline()

if not linha:
    print("Erro: Ficheiro sem cabeçalho.")
    exit(1)
    
cabecalho = re.split(r",(?![^{]*\})",linha)

er1 = re.compile(r"^(?P<campo>\w+)({(?P<li>\d+),?(?P<ls>\d+)?})?(::(?P<funcao>[a-z]+))?$")


num_listas = 0

i = 0

cabecalho[len(cabecalho)-1] = re.sub(r"\n","",cabecalho[len(cabecalho)-1])

while i < len(cabecalho):  
    match = er1.match(cabecalho[i])
    if not match:
        print("Erro: Cabeçalho Inválido - Formato Inválido")
        exit(1)
    else:
        if match.group("li"):
            skip = int(match.group("li"))
            if skip <= 0:
                print("Erro: Cabeçalho Inválido - Lista com tamanho não positivo")
                exit(1)
            if match.group("ls"):
                ls = int(match.group("ls"))
                if skip >= ls:
                    print("Erro: Cabeçalho Inválido - Lista com limite superior menor ou igual a limite inferior")
                    exit(1)
                skip = ls
            if i + skip >= len(cabecalho):
                print("Erro: Cabeçalho Inválido - Colunas Insuficientes Depois De Uma Lista")
                exit(1)
            else:
                reservados = cabecalho[i+1:i+skip+1]
        
                for r in reservados:
                    if not re.match(r"(^$|\s)",r):
                        print("Erro: Cabeçalho Inválido - Colunas Insuficientes Depois De Uma Lista")
                        exit(1)
                i+=skip
            if match.group("funcao"):
                if not is_aggregate_function(match.group("funcao")):
                    print("Erro: Cabeçalho Inválido - Função Inválida")
                    exit(1)     
            num_listas+=1
    i+=1
 
num_linha = 2       
linha = f.readline() 

if not linha:
    print("Erro: Ficheiro sem linhas.")
    exit(1)

while linha:
    campos_linha = re.split(",",linha)
    campos_linha[len(campos_linha)-1] = re.sub(r"\n","",campos_linha[len(campos_linha)-1])
    
    if len(campos_linha) + num_listas == len(cabecalho):
        valid = True
        listas_linha = 0
        linhaDict = {}
        cab_j = 0
        li_j = 0
        while cab_j < len(cabecalho):
            matchL = er1.match(cabecalho[cab_j])
            if matchL.group("li"):
                listaNum = []
                
                lim = int(matchL.group("li"))
                
                if matchL.group("ls"):
                    lim = int(matchL.group("ls"))
                  
                if not matchL.group("funcao"):  
                    z = 0
                   
                    while z < lim:
                        if not re.match("^$",campos_linha[z+li_j]):
                            listaNum.append(float(campos_linha[z+li_j]))
                        z+=1
                    
                    if len(listaNum)<int(matchL.group("li")):
                        print("Linha " +str(num_linha)+" ignorada. Minimo de valores exigidos no campo " +matchL.group("campo")+" é " + matchL.group("li") +" e foram lidos apenas " + str(len(listaNum)) +".")
                        valid = False
                        break
                    
                    linhaDict[matchL.group("campo")] = listaNum
                    
                else:
                    funcao = matchL.group("funcao")
                    z = 0
                    while z < lim:
                        if re.match(r"(\+|-)?\d+(\.\d+)?",campos_linha[z+li_j]):
                            listaNum.append(float(campos_linha[z+li_j]))
                        z+=1
                    
                    if len(listaNum)<int(matchL.group("li")):
                        print("Linha " + str(num_linha)+" ignorada. Função de agregação '" +matchL.group("funcao")+ "' necessita de " + matchL.group("li") +" valores numéricos e tem apenas " + str(len(listaNum))+".")
                        valid = False
                        break
                    
                    result = applyFunction(funcao,listaNum)
                    linhaDict[matchL.group("campo")+"_" + matchL.group("funcao")] = result
            
                cab_j+=lim
                li_j+=lim-1
            else:
                linhaDict[cabecalho[cab_j]] = campos_linha[li_j]
                
            li_j+=1
            cab_j+=1

        if valid:
            dict[nomeSemCsv].append(linhaDict)
    else:
        print("Linha " +str(num_linha)+" ignorada. Número de valores da linha não corresponde aos exigidos pelo cabeçalho.")
        
    linha = f.readline()
    num_linha+=1
    
ficheirojson = open(nomeSemCsv+".json","w")
json.dump(dict,ficheirojson, indent=4, ensure_ascii=False)
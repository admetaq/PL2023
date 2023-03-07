import re 
import menu

f = open ("processos.txt", "r")

linha = f.readline()

er = re.compile(r"::(\d{4})-\d{2}-\d{2}::")

dist = {}

while linha:
    match = re.search(er, linha)
    if match:
        ano = match.group(1)
        if ano in dist:
            dist[ano] += 1
        else:
            dist[ano] = 1

      
    linha = f.readline()
    
menu.printDistribuicao(dist,"Processos por ano", False)

    
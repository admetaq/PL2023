import re 
import menu

f = open ("processos.txt", "r")

linha = f.readline()

er = re.compile(r",(?P<relacao>[A-Z][a-z]+(\s[A-Z][a-z]+)*)[^\.,]*\. P")

dist = {}
i=1
while linha:
    match = re.search(er, linha)
    if match:
        allMatch = re.finditer(er, linha)
        for match1 in allMatch:
            relacao = match1['relacao']
            if relacao in dist:
                dist[relacao] += 1
            else:
                dist[relacao] = 1

    linha = f.readline()
    i+=1
   
menu.printDistribuicao(dist,"Distribuição de relações",False) 



import re 
import menu

f = open ("processos.txt", "r")

linha = f.readline()

erNome = re.compile(r"(?P<primeiroNome>[A-Z][a-z]+) ([A-Z][a-z]+\s)*(?P<apelido>[A-Z][a-z]+)(::|,| e)")
erSeculo = re.compile(r"::((?P<seculo>\d{2})\d{2}-\d{2}-\d{2})")

dist = {}

linhaNr = 1



while linha:
    match1 = re.search(erSeculo, linha)
    if match1:
        seculo = str(int(match1.group('seculo'))+1)
        match2 = re.search(erNome, linha)
        if match2:
            if seculo not in dist:
                dist[seculo] = {}
                dist[seculo]['apelidos'] = {}
                dist[seculo]['nomes'] = {}
                
            allMatch = re.finditer(erNome, linha)
            
            for match in allMatch:
                primeiroNome = match['primeiroNome']
                apelido = match['apelido']
    
                if apelido in dist[seculo]['apelidos']:
                    dist[seculo]['apelidos'][apelido] += 1
                else:
                    dist[seculo]['apelidos'][apelido] = 1
                    
                if primeiroNome in dist[seculo]['nomes']:
                    dist[seculo]['nomes'][primeiroNome] += 1
                else:
                    dist[seculo]['nomes'][primeiroNome] = 1
            
    linhaNr+=1
    linha = f.readline()

f.close()


seculos = list(dist.keys())
seculos.sort(key= lambda x: int(x))
    
for seculo in seculos:
    nomesOrd = sorted(dist[seculo]['nomes'].items(), key= lambda x: x[1], reverse=True)
    apelidosOrd = sorted(dist[seculo]['apelidos'].items(), key= lambda x: x[1], reverse=True)
    distNTop5 = nomesOrd[:5]
    distATop5 = apelidosOrd[:5]
    menu.printPlot(dict(distNTop5),"Século " + seculo,"Primeiros Nomes","Nomes","Quantidade", False)
    menu.printPlot(dict(distATop5), "Século " + seculo,"Apelidos", "Nomes","Quantidade", False)
    input("Pressione enter para continuar...")
    menu.clear()
        


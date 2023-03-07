import re 
import json

f = open ("processos.txt", "r")

procJson = open("processos.json","w")
linha = f.readline()



dictJSON = {}
dictJSON["processos"] = []
er1 = re.compile(r"(?P<caixa>\d+)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>[^:]+)::(?P<pai>[^:]+)::(?P<mae>[^:]+)")
er2 = re.compile(r"(:|\s)(?P<nome>[A-Z][a-z]+( [A-Z][a-z]+)*),(?P<relacao>[^\.]+)\. Proc.(?P<idProc>\d+)\.")

i=1
while linha and i<=20:
    entry = {}
    match1 = er1.search(linha)
    if match1:
        entry["caixa"] = match1['caixa']
        entry["data"]  = match1['data']
        entry["nome"] = match1['nome']
        entry["pai"] = match1['pai']
        entry["mae"] = match1['mae']
        
        observacoes = []
        match2 = re.finditer(er2,linha)
        for match in match2:
            observacao = {}
            observacao["nome"] = match['nome']
            observacao["relacao"] = match['relacao']
            observacao["idProc"] = match['idProc']
            observacoes.append(observacao)
            
        if len(observacoes)>0:
            entry["observacoes"] = observacoes
        
        dictJSON["processos"].append(entry)
            
    linha = f.readline()
    i+=1
    
json.dump(dictJSON, procJson, indent=-1)

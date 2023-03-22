import re

estados = ['LEVANTAR','POUSAR','MOEDA','T','ABORTAR']
stack_estados = [-1]
l_transicao = 0
saldo = 0.0

def printSaldo():
    global saldo
    saldo_formatado = "{:.2f}".format(saldo)
    euros, centimos = str(saldo_formatado).split('.')
    return euros+"e"+centimos+"c"

def printTroco():
    global saldo
    if saldo == 0:
        return "0e0c"
    moedas = {}
    saldoAux = saldo
    while saldoAux > 0:
        if saldoAux >=2:
            saldoAux -=2.0
            moedas["2e"] = 1 if "2e" not in moedas else moedas["2e"] + 1
        elif saldoAux >=1:
            saldoAux -=1.0
            moedas["1e"] = 1 if "1e" not in moedas else moedas["1e"] + 1
        elif saldoAux >=0.5:
            saldoAux -=0.5
            moedas["50c"] = 1 if "50c" not in moedas else moedas["50c"] + 1
        elif saldoAux >=0.2:
            saldoAux -=0.2
            moedas["20c"] = 1 if "20c" not in moedas else moedas["20c"] + 1
        elif saldoAux >=0.1:
            saldoAux -=0.1
            moedas["10c"] = 1 if "10c" not in moedas else moedas["10c"] + 1
        elif saldoAux >=0.05:
            saldoAux -=0.05
            moedas["5c"] = 1 if "5c" not in moedas else moedas["5c"] + 1
        elif saldoAux >=0.02:
            saldoAux -=0.02
            moedas["2c"] = 1 if "2c" not in moedas else moedas["2c"] + 1
        elif saldoAux >=0.01:
            saldoAux -=0.01
            moedas["1c"] = 1 if "1c" not in moedas else moedas["1c"] + 1
        else:
            saldoAux = 0
    
    ret = ""        
    for moeda in moedas:
        ret += str(moedas[moeda])+"x"+moeda+", "
    return ret[:-2]
    
def ac_levantar():
    print('maq: "Introduza moedas."')
    
def ac_pousar():
    print('maq: "troco='+printTroco()+'; Volte sempre!"')
    
def ac_moeda(linha):
    global saldo
    moedaDict = {"1c":0.01,"2c":0.02,"5c":0.05, "10c" : 0.1, "20c" :0.2, "50c":0.5, "1e":1, "2e":2}
    match_linha = re.match(r"^\s*MOEDA\b(?P<moedas>.+)$", linha)
    if match_linha:
        print("maq: ", end = "")
        moedas = list(map(lambda moeda: re.sub(r"\.|\s|;","",moeda), re.split(r",",match_linha.group("moedas"))))
        for moeda in moedas:
            if moeda in moedaDict:
                saldo += moedaDict[moeda]
            else:
                print(moeda +" - moeda inválida; ",end="")
        print('"saldo = ' + printSaldo()+'"')
    else:
        print('maq: "Não foram inseridas quaisqueres moedas."')
        
def ac_t(linha):
    global saldo
    global stack_estados
    global l_transicao
    match_linha = re.match(r"^\s*T=\s*(?P<numero>\d{9,})$", linha)
    if match_linha:
        ntelef = match_linha.group("numero")
        if re.match(r"^00",ntelef):
                if saldo >= 1.5:
                    l_transicao = 1.5
                    saldo -= 1.5
                    print('maq: "saldo = ' +printSaldo()+'"')
                else:
                    stack_estados.pop()
                    print('maq: "Necessita de 1e50c para efetuar uma chamada para o número inserido e neste momento tem '+printSaldo()+'"')
        elif len(ntelef) == 9:
            if re.match(r"^601|641",ntelef):
                print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
            elif re.match(r"^2",ntelef):
                if saldo >= 0.25:
                    l_transicao = 0.25
                    saldo -= 0.25
                    print('maq: "saldo = ' +printSaldo()+'"')
                else:
                    stack_estados.pop()
                    print('maq: "Necessita de 25c para efetuar uma chamada para o número inserido e neste momento tem '+printSaldo()+'"')
            elif re.match(r"^800",ntelef):
                    l_transicao = 0
                    print('maq: "saldo = ' +printSaldo()+'"')
            elif re.match(r"^808",ntelef):
                l_transicao = 0.1
                if saldo >= 0.1:
                    saldo -= 0.1
                    print('maq: "saldo = ' +printSaldo()+'"')
                else:
                    stack_estados.pop()
                    print('maq: "Necessita de 10c para efetuar uma chamada para o número inserido e neste momento tem '+printSaldo()+'"')
        else:
             print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')        
    else:
        print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
        
def ac_abortar():
    global saldo
    global l_transicao
    saldo += l_transicao
    print('maq: "troco='+printTroco()+'; Volte sempre!"')



er_levantar = re.compile(r"^\s*LEVANTAR\s*$")
er_pousar = re.compile(r"^\s*POUSAR\s*$")
er_moeda = re.compile(r"^\s*MOEDA\b")
er_t = re.compile(r"^\s*T=")
er_abortar = re.compile(r"^\s*ABORTAR\s*$")


    
    

linha = input()

estado = -1

while linha and estado != 1 and estado != 4:
    
    estado = stack_estados[len(stack_estados)-1]
    
    if estado == -1:
        if er_levantar.match(linha):
            stack_estados.append(0)
            ac_levantar()
        else:
            print('maq: "Para realizar uma ação tem de levantar o telemóvel primeiro."')
            
            
    elif estado == 0: 
        if er_levantar.match(linha):
            print('maq: "Já levantou o telefone."')
        elif er_pousar.match(linha):
            estado = 1
            ac_pousar()
        elif er_moeda.match(linha):
            stack_estados.append(2)
            ac_moeda(linha)
        elif er_t.match(linha):
            stack_estados.append(3)
            ac_t(linha)
        else:
            print('maq: "'+linha+' não é uma operação válida no estado ' +estados[estado]+'"')
    
             
    elif estado == 2:
        if er_levantar.match(linha):
            print('maq: "Já levantou o telefone."')
            ac_levantar()
        elif er_pousar.match(linha):
            estado = 1
            ac_pousar()
        elif er_moeda.match(linha):
            ac_moeda(linha)
        elif er_t.match(linha):
            stack_estados.append(3)
            ac_t(linha)
        else:
            print('maq: "'+linha+' não é uma operação válida no estado ' + estados[estado]+'"')
            
            
    elif estado == 3: 
        if er_levantar.match(linha):
            print('maq: "Já levantou o telefone."')
            ac_levantar()
        elif er_pousar.match(linha):
            estado =1
            ac_pousar()
        elif er_moeda.match(linha):
            stack_estados.append(2)
            ac_moeda(linha)
        elif er_t.match(linha):
            ac_t(linha)
        elif er_abortar.match(linha):
            estado = 4
            ac_abortar()
        else:
            print('maq: "'+linha+' não é uma operação válida no estado ' + estados[estado]+'"')
            
    if estado != 1 and estado !=4:
        linha = input()
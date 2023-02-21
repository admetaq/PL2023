import os
import sys
import matplotlib.pyplot as plt

def parse_csv():
    """
    Lê um arquivo CSV que contém informações sobre pacientes e cria um dicionário com essas informações.


    Returns:
        dicionarioPacientes: dict 
        Um dicionário com as informações dos pacientes. As chaves são "True" e "False", 
        que indicam se o paciente está doente ou não. Os valores são listas de tuplos que contêm
        as restantes informações do paciente.
    """
    
    mhf = open("myheart.csv","r")

    linha = mhf.readline()

    dicionarioPacientes = {}

    dicionarioPacientes[True] = []
    dicionarioPacientes[False] = []

    i=0

    while linha:
        if i>0:
            linhaSep = linha.split(",") 
            idade = int(linhaSep[0])
            sexo = linhaSep[1]
            tensao = int(linhaSep[2])
            colesterol = int(linhaSep[3])
            batimento = int(linhaSep[4])
            doente = False if int(linhaSep[5]) == 0 else True
            paciente = (idade,sexo,tensao,colesterol,batimento)
            dicionarioPacientes[doente].append(paciente)
        linha = mhf.readline()
        i+=1

    return dicionarioPacientes
    

def distribuicaoDoencaPSexo(dicionarioPacientes):
    """
    Conta a quantidade de pacientes doentes, separando por género. Percorre os pacientes doentes 
    no dicionário de pacientes recebido, e incrementa o valor do género correspondente no dicionário 
    de distribuição de doenças.

    Args:
        dicionarioPacientes : dict 
        Dicionário com os dados do csv.

    Returns:
        dicionarioDist : dict 
        Dicionário onde as chaves "M" e "F" representam o género masculino e feminino, respectivamente, e os valores 
        correspondem à quantidade de pacientes com a doença por género.
    """
    dicionarioDist = dict()
    dicionarioDist["M"] = 0
    dicionarioDist["F"] = 0
    
    for paciente in dicionarioPacientes[True]:
        dicionarioDist[paciente[1]] += 1
    
    return dicionarioDist


def distribuicaoDoencaPFaixaEtaria(dicionarioPacientes):
    """
    Conta a quantidade de pacientes doentes, separando por faixa etária. 
    Percorre os pacientes doentes no dicionário de pacientes recebido, calcula a sua faixa etária e incrementa 
    o seu valor no dicionário.

    Args:
        dicionarioPacientes : dict 
        Dicionário com os dados do csv.

    Returns:
        dicionarioDist : dict
        Um dicionário com as faixas etárias como chaves e a quantidade de pacientes doentes em cada faixa como valores.
    """
    
    dicionarioDist = dict()
    
    for paciente in dicionarioPacientes[True]:
        indice = int(paciente[0]/5)
        chave = str(indice*5)+"-"+str((((indice+1)*5)-1))
        if chave not in dicionarioDist:
            dicionarioDist[chave] = 1
        else: 
            dicionarioDist[chave]+=1            
        
    return dicionarioDist


def minMaxColesterol(dicionarioPacientes):
    """
    Retorna o valor máximo e mínimo do colesterol dos pacientes doentes.

    Args:
        dicionarioPacientes: dict
        Dicionário com os dados do csv.

    Returns:
        tuple:
        Um tuplo com o valor máximo e mínimo do colesterol dos pacientes doentes.
    """
    minimo = sys.maxsize
    maximo = -sys.maxsize-1
    for paciente in dicionarioPacientes[True]:
        if paciente[3] > maximo:
            maximo = paciente[3]
        if paciente[3] < minimo:
            minimo = paciente[3]
    
    return (maximo,minimo)


def distribuicaoDoencaPColesterol(dicionarioPacientes):
    """
    Calcula a distribuição de pacientes doentes por nível de colesterol. 
    Percorre os pacientes doentes no dicionário de pacientes recebido, 
    calcula o nivel de colesterol a que pertencem e incrementa o valor do 
    dicionário para esse nível. A função também cria as chaves para os niveis
    que não tenham pacientes e inicia-os com valor 0.

    Args:
        dicionarioPacientes : dict 
            Dicionário com os dados do csv.

    Returns:
        dicionarioDist : dict
            Dicionário com os níveis de colesterol como chaves e a quantidade 
            de pacientes doentes em cada nível como valores.
    """
    dicionarioDist = dict()
    
    tuploMixMax = minMaxColesterol(dicionarioPacientes)
    
    minimo = tuploMixMax[1]
    maximo = tuploMixMax[0]
    
    aux = minimo
    
    while aux < maximo:
        chave = str(aux)+"-"+str(aux+9)
        dicionarioDist[chave] = 0
        aux +=10
        
    for paciente in dicionarioPacientes[True]:
        indice = int((paciente[3]-minimo)/10)
        chave = str(indice*10+minimo)+"-"+str((((indice+1)*10)-1+minimo))
        dicionarioDist[chave]+=1            
        
    return dicionarioDist


def printDistribuicao(dist,titulo):
    """
    Imprime uma tabela com a distribuição de frequências de uma dada distribuição.

    Args:
        dist : dict
            Um dicionário com os valores como chaves e as quantidades como valores.
        titulo : str
            O título a ser exibido no início da tabela.
    """
    print(titulo+"\n")
    total = sum(dist.values())
    print("{:15s} {:>10s} {:>10s}".format("Valor", "Quantidade", "Frequência"))
    
    chaves = sorted(list(dist.keys()))
    for chave in chaves:
        quantidade = dist[chave]
        print("{:15s} {:10d} {:10.2f}%".format(chave, quantidade, (quantidade/total)*100))
        
def printDistribuicaoIntervalo(dist, titulo):
    """
    Imprime uma tabela com a distribuição de frequências de uma dada distribuição com intervalos de valores.

    Args:
        dist : dict
            Um dicionário com os intervalos como chaves e as quantidades como valores.
        titulo : str
            O título a ser exibido no início da tabela.
    """
    print(titulo+"\n")
    total = sum(dist.values())
    print("{:15s} {:>10s} {:>10s}".format("Valor", "Quantidade", "Frequência"))
    
    elementos = sorted(dist.items(), key=lambda x: int(x[0].split("-")[0]))
    for chave, valor in elementos:
        print("{:15s} {:10d} {:10.2f}%".format(chave, valor, (valor/total)*100))

       
def printPlot(dist,titulo,x,y):
    """
    Gera um gráfico de barras a partir de um dicionário.

    Args:
        dist: dict
            Um dicionário cujas chaves são as categorias e os valores são as quantidades.
        titulo: str
            O título do gráfico.
        x: str
            A descrição do eixo X.
        y: str
            A descrição do eixo Y.
            
    Returns:
        None
    """
    elementos = sorted(dist.items(), key = lambda x: x[0])
    chaves = []
    valores = []
    for chave, valor in elementos:
        chaves.append(chave)
        valores.append(valor)
    plt.title(titulo)
    plt.bar(chaves, valores)
    plt.xlabel(x)
    plt.ylabel(y)
    
    plt.show()

def printPlotIntervalo(dist, titulo, x, y):    
    """
    Gera um gráfico de barras para dados distribuídos em intervalos.

    Args:
        dist: dict
            Um dicionário cujas chaves são os intervalos e os valores são as quantidades.
        titulo: str
            O título do gráfico.
        x: str
            A descrição do eixo X.
        y: str
            A descrição do eixo Y.

    Returns:
        None
    """
    elementos = sorted(dist.items(), key=lambda x: int(x[0].split("-")[0]))
    chaves = []
    valores = []
    for chave, valor in elementos:
        chaves.append(chave)
        valores.append(valor)
        
    plt.title(titulo)
    plt.bar(chaves, valores)
    plt.xlabel(x)
    if(len(chaves)>10):
        plt.xticks(rotation=45)
    plt.ylabel(y)
    
    plt.show()
    
def main_menu():
    """
    Menu principal da interface.
    """
    print("Distruibuições da doença")
    print("1. Gráfico de distribuição da doença por sexo")
    print("2. Gráfico de distribuição da doença por faixa etária")
    print("3. Gráfico de distribuição da doença por nível de colesterol")
    print("4. Distribuição da doença por sexo")
    print("5. Distribuição da doença por faixa etária")
    print("6. Distribuição da doença por nível de colesterol")
    print("7. Sair")

def ui(distDS, distDFE, distDC):
    """
    Interface do utilizador.

    Args:
        distDS : dict
            Distruibuição da doença por sexo.
        distDFE : dict 
            Distribuição da doença por faixa etária.
        distDC : dict
            Distribuição da doença por nível de colesterol.
        
    Returns:
        None 
    """
    main_menu()

    opcao = 0
    while(opcao!=7):
        opcao = input("Escolha a opção: ")

        os.system('cls' if os.name == 'nt' else 'clear')
        if opcao == "1":
            printPlot(distDS,"Gráfico de distribuição da doença por sexo", "Sexo", "Quantidade")
        elif opcao == "2":
            printPlotIntervalo(distDFE,"Gráfico de distribuição da doença por faixa etária","Idade","Quantidade")
        elif opcao == "3":
            printPlotIntervalo(distDC,"Gráfico de distribuição da doença por nível de colesterol","Colesterol", "Quantidade")
        elif opcao == "4":
            printDistribuicao(distDS,"Distribuição da doença por sexo")
        elif opcao == "5":
            printDistribuicaoIntervalo(distDFE,"Distribuição da doença por faixa etária") 
        elif opcao == "6":
            printDistribuicaoIntervalo(distDC,"Distribuição da doença por nível de colesterol")
        elif opcao == "7":
            print("Adeus!")
            quit()
        else:
            print("Opção inválida. Tente de novo.")
        enter = input("Pressione enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main_menu() 
    

def main():
    dicionarioPacientes = parse_csv()

    distDS = distribuicaoDoencaPSexo(dicionarioPacientes)
    distDFE = distribuicaoDoencaPFaixaEtaria(dicionarioPacientes)
    distDC = distribuicaoDoencaPColesterol(dicionarioPacientes)
    
    ui(distDS, distDFE, distDC)



if __name__ == "__main__":
    main()
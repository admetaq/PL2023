import matplotlib.pyplot as plt
import os

    
def printDistribuicao(dist,titulo, modo):
    """
    Imprime uma tabela com a distribuição de frequências de uma dada distribuição.

    Args:
        dist : dict
            Um dicionário com os valores como chaves e as quantidades como valores.
        titulo : str
            O título a ser exibido no início da tabela.
    """
    elementos = sorted(dist.items(), key = lambda x: x[0 if modo == True else 1], reverse= not modo)
    print(titulo+"\n")
    total = sum(dist.values())
    print("{:25s} {:>15s} {:>15s}".format("Valor", "Quantidade", "Frequência"))
    
    chaves = sorted(list(dist.keys()))
    for chave,quantidade in elementos:
        print("{:25s} {:15d} {:15.4f}%".format(chave, quantidade, (quantidade/total)*100))
        

    
def printPlot(dist,nome_graf,titulo,x,y,modo):
    """
    Gera um gráfico de barras a partir de um dicionário.

    Args:
        dist: dict
            Um dicionário cujas chaves são as categorias e os valores são as quantidades.
        nome_graf:
            Nome do gráfico.
        titulo: str
            O título do gráfico.
        x: str
            A descrição do eixo X.
        y: str
            A descrição do eixo Y.
        modo: bool
            True se quiser ordenar em relação ao eixo dos "x". False, caso queira ordenar em relação ao eixo dos "y".
            
    Returns:
        None
    """

    elementos = sorted(dist.items(), key = lambda x: x[0 if modo == True else 1], reverse= not modo)
       
     
    chaves = []
    valores = []
    for chave, valor in elementos:
        chaves.append(chave)
        valores.append(valor)
  
    plt.figure(num=nome_graf)
    plt.title(titulo)
    plt.bar(chaves, valores)
    plt.xlabel(x)
    if(len(chaves)>10):
        plt.xticks(rotation=45, fontsize = 5)
    plt.ylabel(y)
   
    plt.show()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
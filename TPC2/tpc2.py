import sys

def parse(line):
    """
    Analisa uma string e filtra todos os operadores com relevância para uma lista de operadores.

    Args:
        line (str): a string a ser analisada.

    Returns:
        list: uma lista de operadores.

    Examples:
        >>> parse("auhahg=ao10OfFpaha5masksd=plONmepd2emg=")
        ['=', '10', 'off', '5', '=', 'on', '2', '=']
    """
    
    operadores = []
    tamanho = len(line)
    i = 0
    
    while i < tamanho:
        caracter = line[i]
        if caracter.isdigit():
            inicio = i
            while i < tamanho and line[i].isdigit():
                i += 1
            operadores.append(line[inicio:i])
            i-=1
            
        elif caracter.lower() == "o":
            if i + 2 <= tamanho - 1:
                aux1 = line[i:i+2]
                if aux1.lower() == 'on':
                    i+=1
                    operadores.append('on')
                elif i+3<= tamanho - 1:
                    aux2 = line[i:i+3]
                    if aux2.lower() == 'off':
                        i+=2
                        operadores.append('off')
        elif caracter.lower() == "=":
            operadores.append('=')
                    
        i += 1
        
    return operadores

def func_final(operadores):
    """
    Recebe uma lista de operadores e executa as operações nela contidas. Começa com o contador ligado 
    e comporta-se da seguinte forma:
        Quando o operador é:
            - 'on' : Muda o estado do contador para ligado;
            - 'off' : Muda o estado do contador para desligado;
            - Sequência de digitos : Se o contador estiver ligado, soma o valor correspondente ao mesmo;
            - '=' : Imprime o valor atual do contador no stdout;

    Args:
        operadores (list): uma lista de strings que contém os operadores a serem executados.

    Returns:
        None.

    Examples:
        >>> func_final(['=', '10', 'off', '5', '=', 'on', '2', '='])
        start: = 0 + 10 off + 5 = 10 on + 2 = 12 :end
    """

    print("")
    on = True
    count = 0
    
    print("start", end = ": ")
    
    for s in operadores:
        if s == "on":
            if not on:
                print("on", end = " ")
            on = True
        elif s == "off":
            if on:
                print("off", end = " ")
            on = False
        elif s == '=':
            print("=", end = " ")
            print(str(count), end = " ")
        elif s.isdigit():
            print("+ " + s, end =" ")
            if on:
                count += int(s)
    print(":end", end = "")            
    print("\n")



def main():        
    
    operadores = []
    
    # Lê o input do utilizador linha a linha,até o utilizador não inserir mais texto,
    # e filtra os operadores em cada uma delas, adicionando-os a uma lista
    for line in sys.stdin:  
        operadores += parse(line)
        

    func_final(operadores) # Analisa os operadores escritos pelo utilizador e imprime no stdout todas as operações efetuadas pelo mesmo
        
if __name__ == "__main__":
    main()
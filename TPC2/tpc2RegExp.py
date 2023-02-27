import re
import sys

def func_finalRegExp(operadores):
    """
    Recebe uma lista de operadores e executa as operações nela contida. Começa com o contador ligado 
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
        >>> func_final(['=', '10', 'OfF', '5', '=', 'on', '2', '='])
        start: = 0 + 10 off + 5 = 10 on + 2 = 12 :end
    """
    print("")
    on = True
    count = 0
    
    print("start", end = ": ")
    
    for s in operadores:
        if re.match("(?i)on",s):
            if not on:
                print("on", end = " ")
            on = True
        elif re.match("(?i)off",s):
            if on:
                print("off", end = " ")
            on = False
        elif s == '=':
            print("=", end = " ")
            print(str(count), end = " ")
        elif re.match("\d+",s):
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
        operadores += re.findall("(?i)([0-9]+|on|off|=)", line)
        
    func_finalRegExp(operadores) # Analisa os operadores escritos pelo utilizador e imprime no stdout todas as operações efetuadas pelo mesmo

if __name__ == "__main__":
    main()


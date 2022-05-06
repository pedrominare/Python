import math

print("# Bem Vindo ao projeto de REMA!\n\nInsira os valores conforme indicado abaixo!\nLembre-se de substituir a vírgula por ponto se houver decimais !\n")

#Definindo os valores das variaveis e validando os valores

P = 100   # Carga concentrada
L = 2  # Tamanho (comprimento) das barras
b = 3    # Distancia b (entre AB)
c = 5    # Distancia c (entre CD)
lim = 10 # Limite de Escoamento
E = 38 # Modulo de elasticidade em GigaPascal
D = 20 # Diametro das barras cilindricas
pos = 3 # posicao da carga P concentrada
##
# Funcao para receber os dados:
def recebeValor(variavel, msg):
  while True:
    variavel = float(input(msg))
    if variavel < 0:
      print("Valor inválido! Tente novamente.")
    else:
      print("Valor inserido: ", variavel)
      return False

recebeValor(P, "Entre com o valor da carga concentrada P em N: ")
recebeValor(L, "Entre com o comprimento da barra em m: ")
recebeValor(b, "Entre com o valor da distancia \"b\": ")
recebeValor(c, "Entre com o valor da distancia \"c\": ")
recebeValor(lim, "Entre com o valor do limite de escoamento: ")
recebeValor(E, "Entre com o valor do modulo de elasticidade em GigaPascal: ")
recebeValor(D, "Entre com o diâmetro da barra em m: ")
recebeValor(pos, "Entre com a posicao da carga P concentrada: ")

# Funcoes para calcular as reacoes

# Funcao que calcula a reacaoD: ((P*(b+y)*b)-P*(b-a)*(b+2*y))/(2*(b^2+y^2+b*y))
def reacaoD(P, b, c, pos):
  # fazer isso: (P*(b+c)*b) - (P*(b - pos)*(b + (2*c)) / (2*((b**2) + (c**2) + (b*c))))
  first = P*(b+c)*b
  second = P*(b - pos)*(b + (2*c))
  third = 2*((b**2) + (c**2) + (b*c))
  result = first - (second / third)
  return result

reacaoD = reacaoD(P, b, c, pos)

# Funcao que calcula a reacaoA: (P*(b-a)+(reacaoD*y))/b -> (P*(b - pos) + (reacaoD*c))/b
def reacaoA(P, b, c, pos, reacaoD):
  first = P*(b - pos)
  second = reacaoD*c
  result = (first + second)/b
  return result

reacaoA = reacaoA(P, b, c, pos, reacaoD)

# Funcao que calcula a reacaoC -> ((reacaoA*c)+(reacaoD*b))/(b+c)
def reacaoC(reacaoA, c, reacaoD, b):
  first = reacaoA*c
  second = reacaoD*b
  result = (first + second)/(b + c)
  return result

reacaoC = reacaoC(reacaoA, c, reacaoD, b)

# Funcao que calcula o deslocamento em A, C e D -> (reacao*L)/(E*(3,14*D*D/4))
def deslocamento(reacao):
  first = reacao*L
  second = E*((math.pi*D*D) / 4)
  result = first / second
  return result

deslocamentoD = deslocamento(reacaoD)
deslocamentoA = deslocamento(reacaoA)
deslocamentoC = deslocamento(reacaoC)

# Funcao que calcula as deformacoes em A, C e D -> G11/x
def deformacao(deslocamento):
  result = deslocamento / L
  return result

deformacaoD = deformacao(deslocamentoD)
deformacaoA = deformacao(deslocamentoA)
deformacaoC = deformacao(deslocamentoC)

# Funcao para calcular as Tensoes Axiais
def axial(reacao):
  result = reacao / ((math.pi*D*D) / 4)
  return result

axialD = axial(reacaoD)
axialA = axial(reacaoA)
axialC = axial(reacaoC)

# Funcao para calcular os alongamentos
def alongamento(deslocamento):
  result = L + deslocamento
  return result

alongamentoD = alongamento(deslocamentoD)
alongamentoA = alongamento(deslocamentoA)
alongamentoC = alongamento(deslocamentoC)

# Funcao para verificar se houve ou nao ruptura
def ruptura(deslocamento):
  if deslocamento >= lim:
    return print("Houve ruptura!")
  else:
    return print("Não houve ruptura!")

# Exibindo os resultados
def exibindoResultados(var, reacao, deslocamento, deformacao, axial, alongamento):
  print("\n\n# Exibição dos resultados ##\n\n")
  print(f'Reações em {var}: {reacao:.06f}')
  print(f'\nDeslocamento em {var}: {deslocamento:.06f}')
  print(f'\nDeformação em {var}: {deformacao:.06f}')
  print(f'\nTensão Axial em {var}: {axial:.06f}')
  print(f'\nAlongamento em {var}: {alongamento:.06f}\n')

exibindoResultados("A", reacaoA, deslocamentoA, deformacaoA, axialA, alongamentoA)
rupturaA = ruptura(deslocamentoA)
exibindoResultados("C", reacaoC, deslocamentoC, deformacaoC, axialC, alongamentoC)
rupturaC = ruptura(deslocamentoC)
exibindoResultados("D", reacaoD, deslocamentoD, deformacaoD, axialD, alongamentoD)
rupturaD = ruptura(deslocamentoD)
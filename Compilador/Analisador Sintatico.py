# Mgol Compiler #
'''
	By Pedro Augusto Gomes Minare and Sergio Castro
	Built using Python.
'''
from library_beta import *
import sys #utilizar a funcao de interromper o código quando encontrar erro critico

'''*********************** ETAPA 1: ANALISADOR LÉXICO ************************'''
def Analisador_Sintatico():
	
	me_retorna_um_token = Analisador_Lexico()#Token retornado pelo Lexico
	
	while(True): 
		estado_topo_da_pilha = pilha.items[len(pilha.items)-1] # Pega o estado do topo da pilha
		print(pilha.items) # Imprime os elementos armazenados na pilha
		print('\n')
						 #linha       #coluna   da tabela sintatica
		estado_lido = Tabela_Sintatica[estado_topo_da_pilha][terminais(me_retorna_um_token)] # Acessa uma posição da tabela sintatica de acordo com o estado e o terminal lido
		
		# Agora, vamos descobrir qual é a letra que temos na informação que tem na variável 'estado_lido' quando 
		# armazenamos nela o conteúdo da linha e coluna da tabela sintatica que acessamos no passo anterior.
		letra_SRE = estado_lido[:1] # Pega apenas a letra que configura um tipo de ação (S = Shift, R = Reduce, E = Error)

		if letra_SRE == 'S' or letra_SRE == 'R' or letra_SRE == 'E':
			numero_estado = int(estado_lido[1:]) # Pega o numero referente ao estado/regra gramatical/erro de estado
		
		if letra_SRE == 'S':			
			pilha.push(me_retorna_um_token) # empilha o token retornado pelo lexico e guardado na variável 'me_retorna_um_token'
			pilha.push(numero_estado) # empilha o estado de transição que encontramos ao acessar a tabela sintatica e guardamos na variável 'estado_lido'
			# Chamamos o lexico novamente para nos retornar o próximo token do código fonte.
			me_retorna_um_token = Analisador_Lexico()
			#print('\n\nretorno do lexico: ' + a + '\n\n')
			#print('valor do s: {}\n\n' .format(s))
			#print('valor do a: {}\n\n' .format(a))
		
		# Se for 'R' o conteúdo que temos em 'aux', então será realizado uma redução.
		elif letra_SRE == 'R':
			producao_gerada = producao[numero_estado-1] # Retorna a producao gerada
			# É preciso guardar essa informação do número que representa a regra de produção, porque iremos precisar dela
			# depois e porque vamos atualizar nossa 'numero_estado', por isso a linha abaixo.
			linha_regra_de_producao = numero_estado-1
			
			for i in range(qt_de_elementos[numero_estado-1]):
				pilha.pop() # desempilhar
				pilha.pop()
			
			numero_estado = pilha.items[len(pilha.items)-1] # Retorna o estado para posterior desvio
			
			# Quardado a informação do desvio, agora podemos empilhar o simbolo não terminal referente 
			# a redução da regra de produção que encontramos e guardamos em 'producao_gerada'
			pilha.push(producao_gerada) # Empilha o nao terminal referente a producao 
			pilha.push(Tabela_Sintatica[numero_estado][naoTerminais(producao_gerada)]) # Empilha a linha do estado referente ao desvio
			
			# Aqui usamos a variável 'linha_regra_de_producao' apenas para consultar o índice do vetor onde tem a regra de produção da gramática
			# que aplicamos a redução.
			# Imprime a producao gerada pela gramatica
			print('\nPRODUÇÃO GERADA: ' + gramatica[linha_regra_de_producao]+'\n')
		
		elif letra_SRE == 'A':
			# Apenas faço a impressão da ultima regra regramatical que no caso tem que ser :
			# 'P0 -> P'
			print('\nPRODUÇÃO FINAL: ' + gramatica[numero_estado]+'\n')

			# Eu desempilho ela da pilha
			for i in range(qt_de_elementos[numero_estado-1]):
				pilha.pop()
				pilha.pop()

			# Aqui eu apenas imprimo a pilha para mostrar que tem nela o número 0
			# que é exatamente o ponto inicial de onde começamos
			print(pilha.items)
			print('\nLINGUAGEM ACEITA COM SUCESSO !!\n')

			return # não retorno nada
		
		elif letra_SRE == 'E':
			print('ERRO SINATICO ENCONTRADO !!\n')
			errorSyntactic(numero_estado) # Eu passo esse número para minha função errorSyntactic e ele retorna qual é
			return # novamente não retorno nada 
	
# Declaração da minha estrutura do tipo pilha, é uma classe Stack
# com seus métodos.
class Stack:
	def __init__(self):
		self.items = []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def isEmpty(self):
		return (self.items == [])

pilha = Stack() # Eu instaNcio um objeto pilha da classe Stack
pilha.push(0) # Inicializo nossa pilha com o número 0 nela, que representa nosso estado inicial
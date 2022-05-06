# Aluno: Pedro Augusto Gomes Minare
# Matricula: 201306424
#######################################################
# Biblioteca de funcoes utilizadas no Analisador Lexico
#######################################################
import sys #utilizar a funcao de interromper o código quando encontrar erro critico
import string # utilizar as funcoes isdigit e isalpha
### TABELA DE SIMBOLOS CONTENDO AS PALAVRAS RESERVADAS DA LINGUAGEM ###
# Foi utilizado este recurso de dicionario da linguagem para armazenar as palavras reservadas da linguagem como: Lexema - Token - Tipo conforme orientado em sala.
# Cada linha dessa matriz representa um estado do automato e as 
# colunas representam os símbolos de entrada que a linguagem aceita.
# Cada posição da matriz indica o próximo estado que devemos ir 
# dado que se está na linha X (linha = estados do automato) processando 
# o símbolo de entrada Y (símbolos = colunas da matriz) vamos para o próximo estado do automato
# que é indicado pelo conteúdo da posição da matriz linha X coluna Y.
# Exemplo: linha da matriz = 0 e coluna da matriz = 8
#			
#			Significa que você está no estado 0 processando o símbolo que é referente a coluna 8
# 			que é o símbolo ">" (símbolo maior), o conteúdo da matriz cuja linha é 0 e coluna é 8
#			é o número 19, esse número indica que ao processar o símbolo ">" estando no estado 0 
#			você vai para o estado 19 no automato, ou seja, para a linha 19 da matriz.
#			Logo continuando o processo, você irá saltar para a linha 19 da matriz que é o estado que você
#			atingiu no processo anterior quando leu o símbolo ">" estando no estado 0.
#			Na linha 19 da matriz, o único estado que você consegue alcançar é o estado 20
#			quando você lê da variável "arquivo" um símbolo do tipo "=" que é representado na matriz como 
#			sendo a coluna 9, qualquer símbolo diferente desse estando nesse estado 19 (ou linha 19 da matriz)
#			vai te levar para um estado inválido (-1), ou para estado que não existe se você quiser pensar assim.
#			Agora você está no estado 20, isto é, na linha 20 da matriz e como pode ser visto 
#			qualquer processamento de qualquer símbolo quando se está nesse estado não te leva a nenhum estado,
#			portanto o que foi copiado para a variável [bufferInsert] é o que será analisado para descobrir 
#			qual símbolo de fato o analisador lexico detectou, que nesse caso desse exemplo dado é o símbolo ">=".

#			Ao processar lá embaixo no código ele retorna essa reposta informando que o símbolo encontrado é 
#			um Token = OPR (que significa todos os operadores relacionais), o Lexema e 
#			o tipo será o próprio símbolo ">=".
#			O código então pára o processamento na posição em que ele chegou na variável "arquivo" depois 
#			que retornou a resposta do exemplo acima. O analisador lexico é chamado novamente para 
#			continuar o processamento a partir do estado 0 novamente mas a variável "arquivo", será continuado 
#			a leitura dos caracteres a partir de onde parou no processo anterior do exemplo acima.
#			O processamento do restante dos caracteres da variável "arquivo" então continua 
#			a partir do ponto onde ele parou quando encontrou o símbolo ">=".
#			Essa ideia segue para todos os outros símbolos de entrada até que o "arquivo" (ou seja, todos os caracteres da variável arquivo)
#			inteiro seja processado.
#			Ou seja, para cada token encontrado pelo léxico ele para o processamento,  retorna o resultado do
#			que ele analisou de acordo com o que está dentro da variável bufferInsert que foi preenchida através do que era lido posição por posição da variável "arquivo"
#			Em seguida o lexico é chamado novamente para dar continuidade ao processamento de encontrar os 
#			outros Tokens da linguagem até que se chegue no fim do arquivo e então o lexico 
#			para definitivamente de ser chamado.
symbolTable = {} # Declara um dicionario - recebe uma chave que esta vinculada a um valor ou mais. (Lexema, Token, Tipo).
symbolTable ['inicio'] = 'inicio', 'inicio', 'Delimitador'
symbolTable ['varinicio'] = 'varinicio', 'varinicio', 'Delimitador'
symbolTable ['varfim'] = 'varfim', 'varfim', 'Delimitador'
symbolTable ['escreva'] = 'escreva', 'escreva', 'Função'
symbolTable ['leia'] = 'leia', 'leia', 'Função'
symbolTable ['se'] = 'se', 'se', 'Condicional'
symbolTable ['entao'] = 'entao', 'entao', 'Condicional'
symbolTable ['senao'] = 'senao', 'senao', 'Condicional'
symbolTable ['fimse'] = 'fimse', 'fimse', 'Delimitador'
symbolTable ['fim'] = 'fim', 'fim', 'Delimitador'
symbolTable ['inteiro'] = 'inteiro', 'int', 'Numerico'
symbolTable ['literal'] = 'literal', 'lit', 'Literal'
symbolTable ['real'] = 'real', 'real', 'Numerico'

### TABELA DE TRANSIÇÃO DO AUTOMATO FINITO DETERMINISTICO ###
# Legendas dos símbolos (Melhor representado no Excel)
	
# D (numeros) : coluna 0
# L (letras) : coluna 1
# " (aspas) : coluna 2
# { (abre Chaves) : coluna 3
# } (fecha Chaves) : coluna 4
# ' ' (blank space) : coluna 5
# EOF (end of file) : coluna 6
# < (sinal <) : coluna 7
# > (sinal >) : coluna 8
# = (sinal =) : coluna 9
# - (sinal -) : coluna 10
# + (sinal +) : coluna 11
# * (sinal *) : coluna 12
# / (sinal /) : coluna 13
# . (ponto) : coluna 14
# ( (abre parenteses) : coluna 15
# ) (fecha parenteses) : coluna 16
# ; (sinal delimitador) : coluna 17
# ERRO (sinal de erro para qualquer caracter que não pertenca a linguagem): coluna 18
# e (notação científica) : coluna 19
# E (notação científica) : coluna 20
# _ (underline) : coluna 21
# /n (pula linha) : coluna 5
# /t (tabulação) : coluna 5
# Esta representacao está mais compreensível no Excel, pois possui as legendas que facilitam muito na organização.
tableTrasition = [ # horizontal = estados | vertical = as entradas
	#  0   1   2   3   4   5   6   7  8   9   10  11  12  13  14  15  16  17  18  19  20  21
	[  1, 12, 13, 15, -1,  0, 21, 16, 19, 10,  7,  7,  7,  7,  0,  8,  9, 11, 22, 12, 12, -1],
	[  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  2, -1, -1, -1, -1,  4,  4, -1],
	[  3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[  3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  4,  4, -1],
	[  6, -1, -1, -1, -1, -1, -1, -1, -1, -1,  5,  5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[  6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[  6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ 12, 12, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 12, 12, 12],
	[ 13, 13, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ 15, 15, 15, 15,  0, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
	[ -1, -1, -1, -1, -1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 18],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]

## Retorna o número correspondente ao símbolo ##
# Em outras palavras a função symbol recebe como parâmetro o caracter atual que está sendo lido da variável "arquivo"
# e de acordo com esse caracter retorna um número que corresponde a posição na coluna da matriz (ou tabela de transição)
# que se refere ao símbolo lido.
# NOTA que símbolo é qualquer coisa : letras, números, sinais (+, -, *, \, >, <, >=, <=, =, <-), {}, "", etc.
def read_symbols(character_now, state_before):
	if character_now.isdigit(): # recurso do python responsável por identificar um numero
		return 0 # numero
	elif character_now == 'e' and state_before == 1 or character_now == 'e' and state_before == 3: # Notação Científica (e)
		return 19
	elif character_now == 'E' and state_before == 1 or character_now == 'E' and state_before == 3: # Notação Científica (E)
		return 20
	elif character_now.isalpha() : #recurso do python responsável por identificar uma letra
		return 1 #letra
	elif character_now == '"':
		return 2
	elif character_now == '{':
		return 3
	elif character_now == '}':
		return 4
	elif character_now == ' ' or character_now == '\n' or character_now == '\t':
		return 5
	elif character_now == 'EOF':
		return 6
	elif character_now == '<':
		return 7
	elif character_now == '>':
		return 8
	elif character_now == '=':
		return 9
	elif character_now == '-':
		return 10
	elif character_now == '+':
		return 11
	elif character_now == '*':
		return 12
	elif character_now == '/':
		return 13
	elif character_now == '.':
		return 14
	elif character_now == '(':
		return 15
	elif character_now == ')':
		return 16
	elif character_now == ';':
		return 17
	elif character_now == '_':
		return 21
	else:
		return 18  # Qualquer caracter que nao pertenca a linguagem [ERRO] !!
#############################################################################
# Retorna o token correspondente ao símbolo 
# Esta função é reponsável por nos dizer qual é o tipo do token quando se alcançou um estado
# ou no caso da nossa tabela de transição (ou matriz lá em cima) seria a linha em que você se encontra no 
# momento da análise do que está sendo processado.
# Então os números em que é comparado abaixo - o parâmetro finalState - são os números dos estados do nosso automato
# que representam estados (ou linhas da matriz) finais e portanto se eu estou em um deles significa que eu estou 
# num "token".
# Portanto, se pegarmos o exemplo dado lá em cima do símbolo ">=" que foi processado e que você parou na linha 15
# significa que você está no estado 15 do automato e portanto o token referente a esse estado é o OPR (operado relacional)
# Esse OPR então é retornado da função token().
# Isto é, dado que finalState = 15, pois é a linha em que você parou quando estava processando o '>=',
# teremos então: token(15) e seu retorno será uma string 'OPR'.
def token(finalState):
		if finalState == 1 or finalState == 3 or finalState == 6:
			return 'num' # Constante Numerica

		elif finalState == 14:
			return 'literal' # Constante Literal ou parte escrita do printf a ser apresentada no programa. 

		elif finalState == 12:
			return 'id' # Identificador

		elif finalState == 21:
			return 'EOF' # end of file

		elif finalState == 10 or finalState == 16 or finalState == 17 or finalState == 19 or finalState == 20:
			return 'OPR' # Operador relacional

		elif finalState == 18: # < e - que sao <-
			return 'RCB' # Atribuição

		elif finalState == 7:
			return 'OPM' # Operador aritmético

		elif finalState == 8:
			return 'AB_P' # Abre parênteses

		elif finalState == 9:
			return 'FC_P' # Fecha parênteses
		
		elif finalState == 11:
			return 'PT_V' # Ponto e vírgula

		elif finalState == 22:
			return 'ERRO' # um erro foi encontrado

#############################################################################################
# Verifica se o estado atual é um estado final
# Está função analisa se estado (ou linha da matriz) em que você se econtra são alguns desses números abaixo
# caso seja significa que você está num estado de aceitação ou estado final.
# Esta função é importante na hora em que precisamos saber se durante o "caminho" na matriz que fizemos 
# paramos numa linha que representa um estado final no automato. 
def Final_States_Checker(state):
	# String contendo todos os estados finais da tabela de transição
	finalState = [1, 3, 6, 7, 8,  9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22]
	size = len(finalState)
	i = 0
	while i < size:
		if state == finalState[i]:
			return True
		i += 1
	return False
#############################################################################################
### FUNCOES DO ANALISADOR SINTATICO ####
tableSyntax = [ 
	#inicio 	varinicio 	varfim	id 		int 	real 	lit 	leia 	escreva literal	num 	rcb 	se 		(		)		entao 	opr 	fimse 	fim 	$ 		opm 	; 		P 		V 		LV 		D 		TIPO 	A 		ES 		ARG 	CMD 	LD 		OPRD 	COND 	CABEÇALHO	EXP_R	CORPO		
	['S1',		'E0',		'E0',	'E0',	'E0',	'E0',	'E0',	'E0', 	'E0', 	'E0',	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0', 	'E0',	57,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E1', 		'S2', 		'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1',	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	'E1', 	-1, 	15, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E2', 		'E2', 		'S7', 	'S9', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2',	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	'E2', 	-1, 	-1, 	 3, 	 4, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E3', 		'E3', 		'E3', 	'R3', 	'E3', 	'E3', 	'E3', 	'R3', 	'R3',	'E3',	'E3', 	'E3', 	'R3', 	'E3', 	'E3', 	'E3', 	'E3', 	'E3', 	'R3', 	'E3', 	'E3', 	'E3', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E4', 		'E4', 		'S7', 	'S9',	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4',	'E4',	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	'E4', 	-1, 	-1, 	 5,		 4,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E5', 		'E5', 		'E5', 	'R4', 	'E5', 	'E5', 	'E5', 	'R4', 	'R4', 	'E5',	'E5', 	'E5', 	'R4', 	'E5', 	'E5', 	'E5', 	'E5', 	'E5', 	'R4', 	'E5', 	'E5',	'E5', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E6', 		'E6', 		'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6',	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'E6', 	'R22', 	'E6', 	'E6', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E7', 		'E7', 		'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7',	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'E7', 	'S8', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E8', 		'E8', 		'E8', 	'R5', 	'E8', 	'E8', 	'E8', 	'R5', 	'R5', 	'E8',	'E8', 	'E8', 	'R5', 	'E8', 	'E8', 	'E8', 	'E8', 	'E8', 	'R5', 	'E8', 	'E8', 	'E8', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E9', 		'E9', 		'E9', 	'E9', 	'S12', 	'S13', 	'S14', 	'E9', 	'E9', 	'E9',	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	'E9', 	-1, 	-1, 	-1, 	-1, 	10,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E10', 	'E10', 		'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10',	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'E10', 	'S11', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,  	-1, 	-1, 	-1, 	 	-1,	 	-1 ],
	['E11', 	'E11', 		'R6', 	'R6', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11',	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	'E11', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E12', 	'E12', 		'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12',	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'E12', 	'R7', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,	 	-1 ],
	['E13', 	'E13', 		'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13',  'E13',	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'E13', 	'R8', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E14', 	'E14', 		'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14',	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'E14', 	'R9', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,		-1 ],
	['E15', 	'E15', 		'E15', 	'S31', 	'E15', 	'E15', 	'E15', 	'S22', 	'S25', 	'E15',	'E15', 	'E15', 	'S40', 	'E15', 	'E15', 	'E15', 	'E15', 	'E15', 	'S21', 	'E15', 	'E15', 	'E15', 	-1, 	-1, 	-1, 	-1, 	-1, 	58, 	16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E16', 	'E16', 		'E16', 	'S31', 	'E16', 	'E16', 	'E16', 	'S22', 	'S25', 	'E16',	'E16', 	'E16', 	'S40', 	'E16', 	'E16', 	'E16', 	'E16', 	'E16', 	'S21', 	'E16', 	'E16', 	'E16', 	-1, 	-1, 	-1, 	-1, 	-1, 	17, 	16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E17', 	'E17', 		'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'E17',	'E17', 	'E17', 	'E17', 	'E17', 	'E17', 	'17', 	'E17', 	'E17', 	'E17', 	'R10', 	'E17', 	'E17', 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E18', 	'E18', 		'E18', 	'S31', 	'E18', 	'E18', 	'E18', 	'S22', 	'S25', 	'E18',	'E18', 	'E18', 	'S40', 	'E18', 	'E18', 	'E18', 	'E18', 	'E18', 	'S21', 	'E18', 	'E18', 	'E18', 	-1, 	-1, 	-1, 	-1, 	-1,	 	19, 	16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E19', 	'E19', 		'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19',	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'E19', 	'R16', 	'E19', 	'E19',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,			-1, 	-1 ],
	['E20', 	'E20', 		'E20', 	'S31', 	'E20', 	'E20', 	'E20', 	'S22', 	'S25', 	'E20',	'E20', 	'E20', 	'S40', 	'E20', 	'E20', 	'E20', 	'E20', 	'E20', 	'S21', 	'E20', 	'E20', 	'E20', 	-1, 	-1, 	-1, 	-1, 	-1,	 	 6,		16, 	-1, 	18, 	-1, 	-1, 	20, 	48, 		-1, 	-1 ],
	['E21', 	'E21', 		'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21',	'E21', 	'E21',	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'E21', 	'R30', 	'E21', 	'E21', 	-1,		-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,	 	-1 ],
	['E22', 	'E22', 		'E22', 	'S23', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22',	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	'E22', 	-1, 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E23', 	'E23', 		'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23',	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'E23', 	'S24', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,	 	-1 ],
	['E24', 	'E24', 		'E24', 	'R11', 	'E24', 	'E24', 	'E24', 	'R11', 	'R11', 	'E24',	'E24', 	'E24', 	'R11', 	'E24', 	'E24', 	'E24', 	'E24', 	'R11', 	'R11', 	'E24', 	'E24', 	'E24', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1,		-1 ],
	['E25', 	'E25', 		'E25', 	'S30', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'S28',	'S29', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	'E25', 	-1, 	-1,	 	-1,		-1, 	-1, 	-1, 	-1, 	26, 	-1, 	-1,	 	-1,		-1,	 	-1,	 	 	-1,		-1 ],
	['E26', 	'E26', 		'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26',	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'E26', 	'S27', 	-1, 	-1, 	-1, 	-1, 	-1,	 	-1,		-1,		-1, 	-1, 	-1, 	-1, 	-1,		-1, 		-1, 	-1 ],
	['E27', 	'E27', 		'E27', 	'R12', 	'E27', 	'E27', 	'E27', 	'R12', 	'R12', 	'E27',	'E27', 	'E27', 	'R12', 	'E27', 	'E27', 	'E27', 	'E27', 	'R12', 	'R12', 	'E27', 	'E27', 	'E27', 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E28', 	'E28', 		'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28',	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'E28', 	'R13', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E29', 	'E29', 		'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29',	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'E29', 	'R14', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E30', 	'E30', 		'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30',	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'E30', 	'R15', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E31', 	'E31', 		'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31',	'E31', 	'S32', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31', 	'E31',  'E31', 	'E31', 	'E31', 	'E31', 	-1, 	-1,	 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E32', 	'E32', 		'E32', 	'S35', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32',	'S36', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	'E32', 	-1, 	-1, 	-1, 	-1,	 	-1, 	-1, 	-1,	 	-1,		-1,	 	33, 	37, 	-1, 	-1, 		-1, 	-1 ],
	['E33', 	'E33', 		'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33',	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33', 	'E33',  'E33', 	'E33', 	'S34', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E34', 	'E34', 		'E34', 	'R17', 	'E34', 	'E34', 	'E34', 	'R17', 	'R17', 	'E34',	'E34', 	'E34', 	'R17', 	'E34', 	'E34', 	'E34', 	'E34', 	'R17', 	'R17', 	'E34', 	'E34', 	'E34', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E35', 	'E35', 		'E35', 	'E35', 	'E35', 	'E35', 	'E35', 	'E35', 	'E35', 	'E35',	'E35', 	'E35', 	'E35', 	'E35', 	'R20', 	'E35', 	'R20', 	'E35', 	'E35', 	'E35', 	'R20', 	'R20',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E36', 	'E36', 		'E36', 	'E36', 	'E36', 	'E36', 	'E36', 	'E36', 	'E36', 	'E36',	'E36', 	'E36', 	'E36', 	'E36', 	'R21', 	'E36', 	'R21', 	'E36', 	'E36', 	'E36', 	'R21', 	'R21',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E37', 	'E37', 		'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37',	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'E37', 	'S38', 	'R19',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E38', 	'E38', 		'E38', 	'S35', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38',	'S36', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	'E38', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1,	 	39, 	-1, 	-1, 		-1,		-1 ],
	['E39', 	'E39', 		'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39',	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'E39', 	'R18',  -1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E40', 	'E40', 		'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40',	'E40', 	'E40', 	'E40', 	'S41', 	'E40', 	'40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	'E40', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E41', 	'E41', 		'E41', 	'S35', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41',	'S36', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41',	'E41', 	'E41', 	'E41', 	'E41', 	'E41', 	'E41', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	42, 	-1, 	-1, 		45, 	-1 ],
	['E42', 	'E42', 		'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42',	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42',	'S43', 	'E42', 	'E42', 	'E42', 	'E42', 	'E42', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E43', 	'E43', 		'E43', 	'S35', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43',	'S36', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43',	'E43', 	'E43', 	'E43', 	'E43', 	'E43', 	'E43', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	44, 	-1, 	-1, 		-1, 	-1 ],
	['E44', 	'E44', 		'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44',	'E44', 	'E44', 	'E44', 	'E44', 	'R25', 	'E44',	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	'E44', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E45', 	'E45', 		'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45',	'E45', 	'E45', 	'E45', 	'E45', 	'S46', 	'E45',	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	'E45', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E46', 	'E46', 		'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46',	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'S47',	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	'E46', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E47', 	'E47', 		'E47', 	'R24', 	'E47', 	'E47', 	'E47', 	'R24', 	'R24', 	'E47',	'E47', 	'E47', 	'R24', 	'E47', 	'E47', 	'E47', 	'E47', 	'E47', 	'R24', 	'E47',  'E47', 	'E47', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E48', 	'E48', 		'E48', 	'S31', 	'E48', 	'E48', 	'E48', 	'S22', 	'S25', 	'E48',	'E48', 	'E48', 	'S40', 	'E48', 	'E48', 	'E48', 	'E48', 	'S55', 	'E48', 	'E48', 	'E48', 	'E48', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	49 ],
	['E49', 	'E49', 		'E49', 	'R23', 	'E49', 	'E49', 	'E49', 	'R23', 	'R23', 	'E49',	'E49', 	'E49', 	'R23', 	'E49', 	'E49', 	'E49', 	'E49', 	'R23', 	'R23', 	'E49', 	'E49', 	'E49', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E50', 	'E50', 		'E50', 	'S31', 	'E50', 	'E50', 	'E50', 	'S22', 	'S25', 	'E50',	'E50', 	'E50', 	'S40', 	'E50', 	'E50', 	'E50', 	'E50',	'S55', 	'E50', 	'E50', 	'E50', 	'E50', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	51 ],
	['E51', 	'E51', 		'E51', 	'R26', 	'E51', 	'E51', 	'E51', 	'R26', 	'R26', 	'E51',	'E51', 	'E51', 	'R26', 	'E51', 	'E51', 	'E51', 	'E51', 	'R26', 	'R26', 	'E51', 	'E51', 	'E51', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E52', 	'E52', 		'E52', 	'S31', 	'E52', 	'E52', 	'E52', 	'S22', 	'S25', 	'E52',	'E52', 	'E52', 	'S40', 	'E52', 	'E52', 	'E52', 	'E52',	'S55', 	'E52', 	'E52', 	'E52', 	'E52', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	56 ],
	['E53', 	'E53', 		'E53', 	'S31', 	'E53', 	'E53', 	'E53', 	'S22', 	'S25', 	'E53',	'E53', 	'E53', 	'S40', 	'E53', 	'E53', 	'E53', 	'E53',	'S55', 	'E53', 	'E53', 	'E53', 	'E53', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	50, 	-1, 	52,		-1, 	-1, 	53, 	48, 		-1, 	54 ],
	['E54', 	'E54', 		'E54', 	'R28', 	'E54', 	'E54', 	'E54', 	'R28', 	'R28', 	'E54',	'E54', 	'E54', 	'R28', 	'E54', 	'E54', 	'E54', 	'E54', 	'R28', 	'R28', 	'E54', 	'E54', 	'E54', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E55', 	'E55', 		'E55', 	'R29', 	'E55', 	'E55', 	'E55', 	'R29', 	'R29', 	'E55',	'E55', 	'E55', 	'R29', 	'E55', 	'E55', 	'E55', 	'E55', 	'R29', 	'R29', 	'E55', 	'E55', 	'E55', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E56', 	'E56', 		'E56', 	'R27', 	'E56', 	'E56', 	'E56', 	'R27', 	'R27', 	'E56',	'E56', 	'E56', 	'R27', 	'E56', 	'E56', 	'E56', 	'E56', 	'R27', 	'R27', 	'E56', 	'E56', 	'E56', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E57', 	'E57', 		'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57',	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'E57', 	'ACC', 	'E57', 	'E57', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ],
	['E58', 	'E58', 		'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58',	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'E58', 	'R2', 	'E58', 	'E58', 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1, 	-1,		-1, 	-1, 	-1, 	-1, 		-1, 	-1 ]
]

# Aqui eu simplesmente criei uma função que mapeia os simbolos terminais da gramática em um número.
# Então quando o lexico retorna um token desses aí, eu consulto essa função para saber qual é o número 
# que representa ele, apenas isso.
# Representa na Tabela Sintatica a coluna referente ao simbolo terminal
def terminais(a):
	if a == 'inicio':
		return 0 # o 0 representa a coluna da matriz sintatica
	elif a == 'varinicio':
		return 1
	elif a == 'varfim':
		return 2
	elif a == 'id':
		return 3
	elif a == 'int':
		return 4
	elif a == 'real':
		return 5
	elif a == 'lit':
		return 6
	elif a == 'leia':
		return 7
	elif a == 'escreva':
		return 8
	elif a == 'literal':
		return 9
	elif a == 'num':
		return 10
	elif a == 'rcb':
		return 11
	elif a == 'se':
		return 12
	elif a == 'AB_P': # representa o '('
		return 13
	elif a == 'FC_P': # representa o ')'
		return 14
	elif a == 'entao':
		return 15
	elif a == 'opr': # operadores relacionais: <, >, ==, <>, <=, >=
		return 16
	elif a == 'fimse':
		return 17
	elif a == 'fim':
		return 18
	elif a == 'EOF': # $
		return 19
	elif a == 'opm': # operadores matematicos : +, -, *, /
		return 20
	elif a == 'PT_V': # representa o ';'
		return 21

# Aqui a ideia é a msm da função acima, só que neste caso eu mapeio os símbolos não terminais da gramática.		
# Representa na tabela sintatica o número da coluna referente ao não terminal
def notTerminal(A):
	if A == 'P':
		return 22
	elif A == 'V':
		return 23
	elif A == 'LV':
		return 24
	elif A == 'D':
		return 25
	elif A == 'TIPO':
		return 26
	elif A == 'A':
		return 27
	elif A == 'ES':
		return 28
	elif A == 'ARG':
		return 29
	elif A == 'CMD':
		return 30
	elif A == 'LD':
		return 31
	elif A == 'OPRD':
		return 32
	elif A == 'COND':
		return 33
	elif A == 'CABECALHO':
		return 34
	elif A == 'EXP_R':
		return 35
	elif A == 'CORPO':
		return 36

def errorSyntactic(stateError):
	if stateError == 0:
		print('Esperava palavra reservada: "inicio"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 1:
		print('Esperava palavra reservada: "varinicio"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 2:
		print('Esperava id ou Fechamento varfim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 3:
		print('Esperava fechamento fim' +'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 4:
		print('Esperava "id" + "tipo": int / lit / real ou Fechamento varfim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 5:
		print('Esperava inicialização: id / leia / escreva / se ou Fechamento fim' +'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 6:
		print('Condicional incorreta'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 7:
		print('Esperava ";" após varfim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 8:
		print('Esperava inicialização: id / leia / escreva / se ou Fechamento fim' +'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 9:
		print('Esperava definição de tipo "int" / "lit" / "real"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 10:
		print('Esperava ";" após "TIPO"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 11:
		print('Declaração incorreta esperava fechamento "varfim" antes ";" ou "id" antes "TIPO"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 12 or stateError == 13 or stateError == 14:
		print('Esperava ";" após declaração de tipo'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 15 or stateError == 16 or stateError == 18 or stateError == 20:
		print('Esperava inicialização: id / leia / escreva / se ou Fechamento fim'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 17 or stateError == 19 or stateError == 21:
		print('Esperava fechamento'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 22:
		print('Esperava "id" após "leia"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 23:
		print('Esperava ";" após "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 25:
		print('Esperava argumento : "literal" / "num" / "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 26:
		print('Esperava ";" após argumento'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 28:
		print('Esperava ";"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 29:
		print('Esperava argumento "num"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 30:
		print('Esperava argumento "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 31:
		print('Esperava "(" após "se"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 32:
		print('Esperava ";" após atribuição'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 33:
		print('Esperava ";" após atribuição'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 34:
		print('Esperava inicialização de: "id" / "leia" / "escreva" / "se" ou Fechamento "fimse" / "fim"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 35 or stateError == 36:
		print('Esperava ";" ou ")"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 37:
		print('Esperava operador matemático : "+" / "-" / "*" / "/" após "num" ou operador : "+" após "id"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 38:
		print('Esperava "id" ou "num" após operador matematico'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 39:
		print('Esperava ";" após operação matemática ou concatenação'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 40:
		print('Esperava abertura de parênteses'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 41:
		print('Esperava "id" ou "num"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 42:
		print('Esperava operador relacional : ">" / "<" / "<>" / "=" / "<=" / ">="'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 43:
		print('Esperava "id" ou "num"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 44 or stateError == 45:
		print('Esperava fechamento de parênteses'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 46:
		print('Esperava palavra reservada "entao"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 47:
		print('Esperava declaração da condicional'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 48 or stateError == 53 or stateError == 52:
		print('Esperava inicialização: "se" / "leia" / "escreva" ... ou Fechamento "fim" ou "fimse"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 49:
		print('Esperava fechamento: "se" / "leia" / "escreva" ... ou Fechamento "fim" ou "fimse"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 50:
		print('Esperava inicialização: "se" / "leia" / "escreva" ... ou Fechamento "fim" ou "fimse"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 51:
		print('Esperava CORPO para expressao'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 54:
		print('Condicional sem CORPO'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 55: 
		print('Esperava palavra reserva "fimse" após CORPO'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 56:
		print('CMD sem CORPO'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 57:
		print('Sintaxe incorreta'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))
	elif stateError == 58:
		print('Esperava fechamento "fim" de "inicio"'+'\n'+'Linha : {} | Coluna : {}'.format(line, position-2))


# Este vetor representa minha gramática livre de contexto (ou GLC), são todas as regras de produções da 
# minha gramática. Cada índice do vetor indica qual a regra, por isso no exemplo que dei na explica da tabela 
# sintatica lá em cima quando eu disse que a regra de produção 'P -> inicio V A' era a regra 2, na verdade no vetor
# ela é a 1. É importante manter a informação das regras de produção da gramática, porque quando ocorre uma Redução
# você consulta por meio do índice essa regra pra imprimir na tela ela, apenas isso.
# Produçoes da gramatica
grammar = [
'P0 -> P',
'P -> inicio V A',
'V -> varinicio LV',
'LV -> D LV',
'LV -> varfim;',
'D -> id TIPO;',
'TIPO -> int',
'TIPO -> real',
'TIPO -> lit',
'A -> ES A',
'ES -> leia id;',
'ES -> escreva ARG;',
'ARG -> literal',
'ARG -> num',
'ARG -> id',
'A -> CMD A',
'CMD -> id rcb LD;',
'LD -> OPRD opm OPRD',
'LD -> OPRD',
'OPRD -> id',
'OPRD -> num',
'A -> COND A',
'COND -> CABECALHO CORPO',
'CABECALHO -> se (EXP_R) entao',
'EXP_R -> OPRD opr OPRD',
'CORPO -> ES CORPO',
'CORPO -> CMD CORPO',
'CORPO -> COND CORPO',
'CORPO -> fimse',
'A -> fim'
]

# Eu poderia ter aproveitado o vetor acima para saber qual é a variável da gramática quando uma redução ocorreu,
# mas eu preferi criar outro vetor colocando apenas essas variáveis, ou seja, apenas pegando o lado esquerdo 
# da regra de produção e mantive a msm sequência da de cima.
# Indica para qual não terminal a produção deve ser reduzida
production = [
	'P0',
	'P',  
	'V', 
	'LV', 
	'LV', 
	'D',
	'TIPO',
	'TIPO',
	'TIPO',
	'A',
	'ES',
	'ES',
	'ARG',
	'ARG',
	'ARG',
	'A',
	'CMD',
	'LD',
	'LD',
	'OPRD',
	'OPRD',
	'A',
	'COND',
	'CABECALHO',
	'EXP_R',
	'CORPO',
	'CORPO',
	'CORPO',
	'CORPO',
	'A'
]

# Este vetor informa a quantidade de elementos que uma regra de produção possui. Por exemplo:
# a primeira regra de produção 'P0 -> P', produz um elemento, por isso no vetor abaixo temos aquele 1 no índice 0
# outro exemplo 'D -> id TIPO;', temos 3 elementos, 'id' é um, 'TIPO' é outro, ';' é o terceiro, por isso no índice
# 5 do vetor abaixo temos 3. Essa ideia segue para as demais regras de produção. Ou seja, cada elemento desse vetor
# informa a quantidade de eleementos de uma regra de produção do vetor grammar, índice(vetor grammar) a índice (vetor syzeProction).
# Indica a quantidade de elementos gerados por uma producao	
syzeProduction = [1,  3,  2,  2,  2,  3,  1,  1,  1,  2,  3,  3,  1,  1,  1,  2,  4,  3,  1,  1,  1,  2,  2,  5,  3,  2,  2,  2,  1,  1]

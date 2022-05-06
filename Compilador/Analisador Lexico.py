# Mgol Compiler #
'''
	By Pedro Augusto Gomes Minare and Sergio Castro
	Built using Python.
'''
from library import *

'''*********************** ETAPA 1: ANALISADOR LÉXICO ************************'''
# Inicio do programa
# Faz a analise lexica e retorna o token correspondente
def Analisador_Lexico():
	# variavel 'global' -> declarada tambem fora do escopo da função.
	global file # Variável do tipo vetor que recebe todo o conteúdo do arquivo texto.txt lido.
	global cursor # Indica a posição exata do caracter que está sendo lido no vetor "file".
	global Number_of_Characters # Mantém a quantidade de caracteres que o arquivo contém, ou seja, o "tamanho" da variável arquivo.
	
	global line # Indica qual linha você se econtra no arquivo.
	global position # Representa a posição anterior do caracter já lido da variável "file".

	token_unless_id = {} # Dicionario usado para auxiliar quando for armazenar tokens de outros tipos que nao seja um tipo "id".

	if cursor == Number_of_Characters: # Verifica se a variável cursor está exatamente na última posição do vetor file, ou seja, se meu vetor file tem 300 posições e meu cursor estiver na posição 299 significa que eu cheguei na posição final do arquivo
		bufferInsert = '' # Como chegou-se no fim do arquivo então limpamos o bufferInsert
		token_unless_id[bufferInsert] = [bufferInsert, 'EOF', 'Fim de arquivo'] # Atribui os valores na variável token_unless_id (neste caso a variavel running la embaixo vai identificar que sua segunda posicao "running[1] == 'EOF' e aí para o programa.
		return token_unless_id[bufferInsert] # Retornamos esses valores atribuidos. A ideia aqui é que como a função lexico retorna um vetor com 3 "valores" que são lexema, token e tipo, eu crio a variável token_unless_id faço ela receber nesse caso aí, 3 valores que representam o fim do arquivo e retorno essa variável token_unless_id com 3 valores 

	State_Now = 0 # Indica sempre o estado (ou linha da matriz) atual que vc se econtra
	State_Before = 0 # Indica o estado (ou linha) anterior do qual vc veio para ir pro estado atual. Esta variável é importante para mater o controle de que estado (ou linha da matriz) vc veio e saber se vai dar algum erro ou não
	bufferInsert = '' # Variável que recebe os caracteres lidos da variável "file" que é do tipo vetor
	character_selected = file[cursor] # Atribui o caracter que o cursor está indicando do vetor "file"
	Flag_to_end = 0 # Responsável para sinalizar quando vc chegou no fim do vetor file, enquanto for = 0, não chegou no fim.

	# A variável State_Next receberá o próximo estado (ou linha da matriz) para leitura. 
	# Isso acontece por meio da matriz tableTrasition.
	# A ideia aqui é acessar a linha e coluna da matriz de acordo com o estado que vc está e o caracter que está sendo lido.
	# Para isso passamos a variável "State_Now" no primeiro colchete para indicar o estado que vc se encontra no momento e
	# no outro colchete chamamos a função "read_symbols" passando como parâmetro o caracter lido do arquivo anteriormente
	# e o estado anterior que vc estava, a função "read_symbols" retornará a coluna de acordo com o caracter que está sendo lido no momento
	# Ok, uma vez que temos o próximo estado (ou linha da matriz) segue:
	State_Next = tableTrasition[State_Now][read_symbols(character_selected, State_Before)]
	
	while State_Next != -1: # Aqui verificamos se a posição da matriz que acessamos o conteúdo retornado foi diferente de -1, isso implica que se for então temos um proximo estado a ir
		# Quando sabemos que temos um proximo estado a ir, então atualizamos nosso estado atual para indicar que agora estamos nesse proximo estado
		State_Now = State_Next # Atualiza o estado atual
	
		# Esta verificação fazemos para manter o controle das nossas variáveis line e position atualizadas
		# Ou seja, no vetor "file" quando a variável "cursor" aponta para uma posição do vetor que contem '\n'
		# indica que é uma quebra de linha e portanto significa que os proximos caracteres a serem lidos 
		# estão na linha de baixo (por isso o incremento +1 em line)
		# e position recebe o valor 1 porque passamos para a linha de baixo e portanto voltamos para a coluna 1 do
		# arquivo propriamente dito (ou seja nosso arquivo texto.txt)
		if character_selected == '\n':
			line += 1 # Indica a quebra de linha do arquivo.
			position = 1 
	
		# Esta verificação é importante pois durante a leitura de caracteres do nosso vetor "file" apontado pela
		# variável "cursor" não queremos processar quebra de linha (isto é, '\n'), tabulação (isto é, \t) nem espaço em branco (isto é, ' ')
		if character_selected != '\n' and character_selected != '\t' and character_selected != ' ': # Ignora quebra de linha, tabulação e espaço em branco
			# Certo! Uma vez garantido isso acima queremos processar todos os outros caracteres da string (ou vetor) "file" 
			bufferInsert += character_selected # Adiciona o caracter lido da string "file" no buffer de entrada . 
			#Note o sinal de +=. Isso significa que estamos concatenando o conteúdo que tem dentro do bufferInsert com o proximo caracter lido da string "file"
			# Ao inserir um caracter na variável bufferInsert precisamos certificar se um caracter do tipo abre chaves '{' foi adicionado:
			if '{' in bufferInsert: # Verifica se abre chaves foi adicionado no bufferInsert
				# Note que fazemos o mesmo para fecha chaves
				if '}' in bufferInsert: # Verifica se fecha chaves foi adicionado no bufferInsert
					bufferInsert = '' # Se os dois foram adicionados significa que o Analisador_Lexico está analisando um comentário, e este podemos ignorar, por isso limpamos o bufferInsert
		
		# Beleza! Agora que adicionamos um caracter ao nosso bufferInsert precisamos atualizar nossa variável "cursor"
		# para no proximo loop do while ele indicar a proxima posição do proximo caracter a ser lido
		# da mesma forma atualizamos nossa variável "position" que indica a "coluna" no arquivo texto.txt em que estamos agora:
		cursor += 1 # Atualiza a posição do cursor no arquivo
		position += 1 # Atualiza o valor da variável "position" no arquivo
	
		# Neste ponto verificamos se nosso "cursor" ainda possui um valor menor do que a quantidade de caracteres que nossa string "file" tem.
		# Em caso afirmativo então podemos prosseguir. Let's go!
		if cursor < Number_of_Characters: # Verfica se o cursor ainda não chegou no final do arquivo
			# Se não chegou no final do arquivo ou no nosso caso no final da string "file"
			# Então podemos ler o próximo caracter
			character_selected = file[cursor] # Pega o proximo caracter e atribui a variável "character_selected"
			# Aqui devemos atualizar nosso estado anterior para o estado atual
			# O motivo disso é que a variável State_Now irá receber o proximo estado (State_Next)
			# quando o loop rodar novamente, por isso temos que manter o controle do nosso estado anterior 
			# quando nossa variável State_Now passa a receber o proximo estado
			State_Before = State_Now # Atualiza o estado anterior
	
		# Esta condição é válida quando chegamos definitivamente no final do arquivo, isto é, o valor da nossa 
		# variável "cursor" passa a ter o mesmo valor da quantidade de caracteres que nossa string "file" tem
		# e portanto isso implica que estamos na última posição + 1 do vetor, ou seja, estamos uma posição fora 
		# da string "file"
		else:
			# Nossa variável Flag_to_end então passa a assumir valor 1 para indicar que chegamos no final do arquivo
			Flag_to_end = 1 # Sinaliza que chegou no final do arquivo 
	
		# Verificamos se chegamos no final do arquivo, como Flag_to_end ainda é 0 pois definimos ela lá em cima 
		# no começo dessa função Analisador_Lexico como 0, isso indica que ainda não chegamos no final da nossa 
		# string "file" e portanto podemos prosseguir caminhando pelos estados de nossa tabela de transição
		if Flag_to_end != 1:
			# Nosso estado atual (State_Now) foi atualizado
			# e nosso caracter lido foi atualizado
			# com isso temos o próximo estado que estamos por meio da nossa tabela de transição
			State_Next = tableTrasition[State_Now][read_symbols(character_selected, State_Before)] # Retorna proximo estado
		else:
			# Caso seja o último caracter lido da string "file" o cursor não estará apontando para 
			# a proxima posição dela, pois ela já terá sido ultrapassada, logo próximo 
			# estado recebe -1 para o loop parar, com isso garantimos que a análise
			# do que está no buffer de entrada seja feita
			State_Next = -1 # Atribuimos -1 à variável "State_Next" para terminarmos nosso loop quando chegamos no final do arquivo
	
	# Beleza! Agora vamos analisar como a função Analisador_Lexico retorna seus tokens
	# Primeiro verificamos se o estado em que paramos no processo anterior é um estado de aceitação ou estado final
	# Para isso consultamos nossa função definida como "Final_States_Checker" e passamos a variável "State_Now" como parâmetro
	# Em caso afirmativo desta condição então estamos em algum estado de aceitação e portanto podemos analizar qual token devemos retornar
	
	if Final_States_Checker(State_Now):
		# Aqui verificamos se o conteúdo que o bufferInsert possui nele é alguma chave do nosso dicionário "symbolTable"
		# se não for então verificamos se dado o estado atual que estamos (isto é, State_Now) 
		# como parâmetro da função token o resultado que ela retornará é igual a string 'id'? 
		# Se for então estamos diante de um identificador 
		# ou seja, um token do tipo id (identificador)
		if bufferInsert not in symbolTable and token(State_Now) == 'id':
			# Se a condição acima for verdade então queremos adicionar esse identificador no nosso dicionário
			# Para isso chamamos nosso dicionário e passamos como chave que queremos adicionar 
			# o conteúdo da variável bufferInsert e vinculamos essa chave aos valores definidos abaixo:
			# 'id', bufferInsert, ' ' , nessa ordem, pois dessa forma estamos mantendo o padrão de que
			# temos uma estrutura que quando consultado uma chave dela ela retorna 3 valores na sequência
			# token | lexema | tipo
			symbolTable[bufferInsert] = bufferInsert, 'id', ' ' # Adiciona o conteúdo de bufferInsert no dicionário vinculando ele aos valores token, lexema e tipo
									#	    ^          ^	 ^
									#	    |	       |     |
									#     Lexema     Token 	TIPO
			
			# Em seguida imprime a tabela de símbolos (symbolTable)
			# para mostrar que o identificador foi adicionado a ela
			print('\n\nTabela de simbolos sendo atualizada...\n')
			for x in symbolTable.items(): # Iteramos então sobre o dicionário symbolTable imprimindo cada elemento seu
				print(x) # imprime
	
			# Aqui finalmente retornamos o tipo do token que a função Analisador_Lexico identificou que neste caso é um identificador
			# Será retornado um vetor com 3 elementos que são: o token na posição 0 deste vetor, 
			# o lexema que é está na posição 1 deste vetor, 
			# e o tipo que está na na posição 2 deste vetor
			# Portanto será retornado esses 3 valores de uma vez só por meio de um vetor com 3 posições
			# Logo, consulta a tabela de simbolos (ou dicionário symbolTable) passando como chave o conteúdo do bufferInsert para retornar os valores referentes a essa chave
			return symbolTable[bufferInsert] # Aqui retorna os tokens do tipo identificador
			
		# Aqui é para quando caso o conteúdo da variável bufferInsert seja uma chave 
		# que o dicionário symbolTable contém, então implica que é uma palavra reservada
		# portanto basta retornarmos ela diretamente 
		elif bufferInsert in symbolTable:
			# Aqui acessamos o dicionário passando como chave essa palavra reservada que é o conteúdo que está dentro 
			# do bufferInsert , o symbolTable então retorna um vetor contendo 3 valores igual no caso acima do identificador
			# onde a posição 0 do vetor é o token, a posição 1 o lexema e a posição 2 o tipo
			return symbolTable[bufferInsert]  # Aqui retornar os tipos de tokens que são palavras reservadas
			
	
		# Nesta situação , caso o conteúdo do nosso bufferInsert não se trate de um identificador nem de uma palavra reservada
		# e ainda assim estamos num estado de aceitação, isso implica que podemos estar nos seguintes tipos de token abaixo:
		else:
			# Primeiro token analisado token tipo erro
			# Em nossa tabela de transição definimos um estado final que chegamos nele sempre que lemos um símbolo ou caracter
			# não válido para a nossa linguagem a partir do estado 0 e portanto chegamos nesse estado de "erro"
			# que indica como "token" (entre aspas msm, porque na verdade não é token) um token tipo erro (mais ou menos isso)
			# Quando a condição abaixo é verdadeira devemos então parar nosso analisador, pois significa 
			# que um caracter inválido foi lido e alcançamos então dessa maneira o estado final que representa esse erro
			# como esse estado não leva a lugar nenhum temos que parar nosso analisador e informar que 
			# um erro no código foi identificado
			################################################################################################################			
			if token(State_Now) == 'ERRO': # Caracter inválido lido
				print('\n\nUm erro foi encontrado. Line: {} | Position: {}'.format(line, position-2)) # aqui é só a sintaxe em python para imprimir uma linha num formato desejado no caso das {} será substituídas pelos valores "line" e "position" respectivamente. O position é subtraido por 2 porque queremos pegar a posição exata no texto.txt que o caracter inválido foi lido. Como o position inicializa com 1 e não como 0 então eu subtraio por 2 que caracteriza a posição anterior onde a variável "cursor" está localizada. Como dito como o cursor inicializa com 0 e position com 1 então position sempre estára um valor a mais que cursor por isso o -2. 
				print('Caracter "{}" não pertence a linguagem'.format(bufferInsert[len(bufferInsert)-1])) # aqui queremos pegar exatamente o caracter inválido que foi pego, então para isso eu chamo a fução len() do python que retorna o tamanho da string bufferInsert naquele momento e subtraio por -1 para pegar a posição do penultimo caracater da variável bufferInsert
				#sys.exit() # Função da biblioteca sys importada no inicio do deste código responsável por parar a execução do código
				return token(State_Now)
			#################################################################################################################
			# Beleza! Se o estado atual que estamos não é um em que paramos no estado dos tokens do tipo identificadores
			# ou dos "tokens" do tipo palavras reservadas 
			# ou do "token" que é do tipo erro
			# e ainda assim estamos em um estado final,
			# só podemos estar em um dos estados que nos leva para os tokens abaixo
			else:
				# Cada condicional aqui chamamos a função token e passamos como parâmetro 
				# o estado em que paramos na execução do loop
				# dessa forma, por meio do State_Now saberemos qual token devemos retornar
				# para a função Analisador_Lexico
				# A variável token_unless_id é um dicionário criado apenas 
				# para criarmos a estrutura chave vinculada a um vetor de 3 posições
				# que contem exatamente na sequência que definimos :
				# lexema, token e tipo
				if token(State_Now) == 'num':
					token_unless_id[bufferInsert] = [bufferInsert, 'num', bufferInsert]
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'literal':
					token_unless_id[bufferInsert] = [bufferInsert, 'literal', 'Constante Literal']
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'OPR':
					token_unless_id[bufferInsert] = [bufferInsert, 'opr', bufferInsert]
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'RCB':
					token_unless_id[bufferInsert] = [bufferInsert, 'rcb', '=']
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'OPM':
					token_unless_id[bufferInsert] = [bufferInsert, 'opm', bufferInsert]
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'AB_P':
					token_unless_id[bufferInsert] = [bufferInsert, 'AB_P', 'Abre Parenteses']
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'FC_P':
					token_unless_id[bufferInsert] = [bufferInsert, 'FC_P', 'Fecha Parenteses']
					return token_unless_id[bufferInsert]
				elif token(State_Now) == 'PT_V':
					token_unless_id[bufferInsert] = [bufferInsert, 'PT_V', 'Ponto e Virgula']
					return token_unless_id[bufferInsert]
	
	# Verifica a condição que gerou o erro
	# Aqui é no caso de durante o nosso loop não pararmos num estado de aceitação 
	# listado na função isFinalState
	# significa que paramos em algum estado que não é final e portanto 
	# implica que no nosso código Mgol alguma coisa ficou faltando para
	# gerar essa situação de pararmos num estado de não aceitação
	# por exemplo:
	# suponha que esteja sendo analizado o seguinte trecho:
	# A <- 2.;
	# nota que a variável (identificador) A está sendo atribuido a ela (por meio do sinal <-) o número
	# que poderia ser um número decimal porque como visto no exemplo ai, temos um número seguido de ponto
	# e o que nosso analisador está esperando pra ler em seguida depois do ponto? Um outro número né para 
	# identificar seu token como sendo do tipo 'num'.
	# Então não chegamos no estado final pois paramos no estado em que ele processou o ponto e em seguida 
	# veio um ";". Por isso paramos no que eu diria "no meio do caminho", não alcançamos um estado de 
	# aceitação.
	# A mesma ideia vale para os outros casos ai embaixo, e o que vamos fazer depois de reportar a posição 
	# do arquivo que o erro lexico foi encontrado? Analisamos
	# qual estado paramos e de acordo com ele imprimimos o tipo de erro e paramos nosso código com a função "sys.exit()" pois considero um erro critico e a leitura precisa ser interrompida.   
	# Verifica a condição que gerou o erro
	else:
		print('\n\nUm erro léxico foi identificado.')
		print('Line: {} | Position: {}'.format(line, position-2))
		
		if State_Now == 0 and character_selected == '}':
			print('ERROR CODE 1: chave fechada sem ter uma chave aberta.')
			sys.exit()
		elif State_Now == 2:
			print('ERROR CODE 2: esperava-se um numero apos o ponto.')
			sys.exit()
		elif State_Now == 4:
			print('ERROR CODE 3: estrutura de notação científica inválida.')
			sys.exit()
		elif State_Now == 5:
			print('ERROR CODE 4: um número é necessário na estrutura de uma notação científica.')
			sys.exit()
		elif State_Now == 13:
			print('ERROR CODE 5: Aspas precisam ser fechadas caso sejam abertas.')
			sys.exit()
		elif State_Now == 15:
			print('ERROR CODE 6: A chave aberta precisa ser fechada.')
			sys.exit()
		else:
			print('Erro não identificado -> Contate o desenvolvedor do programa.')
			sys.exit()
#############################################################################################

cursor = 0 # Indica a posição em que foi lido o último caracter
line = 1 # Indica a posição atual da linha do arquivo codigo Mgol
position = 1 # Indica a posição do erro encontrado no arquivo codigo Mgol

f = open("texto.txt", 'r') # abre o arquivo para leitura
file = f.read() # atribui o arquivo inteiro a uma variável do tipo string
Number_of_Characters = len(file) # conta a quantidade de caracteres do arquivo

f.close() # fecha o arquivo texto.txt

# Declaramos nossa variável auxiliar e definimos ela como o valor None 
running = None # Variável que nao aloca endereço de memoria e foi iniciada nula do tipo vetor auxiliar para imprimir os retornos da função Analisador_Lexico()

print('\n  LEXEMA   |   TOKEN   |   TIPO   ')

# A ideia aqui é chamar nossa função Analisador_Lexico 
# o que ela retornar será pego pela variável "running"
# Como nosso Analisador_Lexico retorna um vetor de 3 posições onde a posição 0 indica que é o lexema
# posição 1 indica que é o token e posição 2 indica que é o tipo

while True:
	running = Analisador_Lexico() # Variável auxiliar recebe o conteúdo que a função lexico retorna
	
	if running[1] == 'EOF':
		#print(running)
		print('\n\n ## Encerramento do Arquivo ##') 
		break; # Quebramos nosso loop para que ele pare neste momento
	
	print('======================================')
	print(running) # Aqui imprimimos o conteúdo que o Analisador_Lexico retornou caso não seja EOF
	
input("Pressione <enter> para encerrar o programa.")
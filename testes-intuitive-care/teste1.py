# Teste 1: WebScrapping
# Código desenvolvido para baixar os Anexos I ao IV referentes ao Teste 1 para processo seletivo da empresa Intuitive Care.
# Autor: Pedro Minaré, Data: 25/05/2022 | Link do código em funcionamento: https://youtu.be/jgvTafOmaIg

# Passo a passo da construção do código.
# O projeto foi criado no Visual Studio Code.
# O primeiro passo foi instalar o módulo "requests" por meio do comando "pip install requests" e logo em seguida adicionar o pip nas variáveis de ambiente: py -m pip install requests.

import requests, zipfile;

def baixar_arquivos(url, local):
    # o comando requests.get() realiza uma requisição ao servidor da url, passada como argumento da função.
    resposta = requests.get(url, stream = True) # contém o conteúdo da URL.
    if resposta.status_code == requests.codes.OK:
        with open(local, 'wb') as novo_arquivo: # abre o arquivo baixado e escreve (binário) o conteúdo de "resposta" em um novo arquivo.
            novo_arquivo.write(resposta.content)
        print("Download realizado! Arquivo salvo: {}".format(local))
    else: # em caso de link quebrado ou falha na requisição de dados:
        resposta.raise_for_status()

# lista de nomes dos arquivos a serem baixados do site 
# Anexo I - Lista completa de procedimentos (.pdf), 
# Anexo I - Lista completa de procedimentos (.xlsx), 
# Anexo II - Diretrizes de utilização (.pdf), 
# Anexo III - Diretrizes clínicas (.pdf), 
# Anexo IV - Protocolo de utilização (.pdf).
lista_de_arquivos = ['Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536.pdf', 'Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536.xlsx', 'Anexo_II_DUT_2021_RN_465.2021_tea.br_RN473_RN477_RN478_RN480_RN513_RN536.pdf', 'Anexo_III_DC_2021_RN_465.2021.v2.pdf', 'Anexo_IV_PROUT_2021_RN_465.2021.v2.pdf']

# URL BASE do diretório de todos os arquivos solicitados para download.
BASE_URL = 'https://www.gov.br/ans/pt-br/arquivos/assuntos/consumidor/o-que-seu-plano-deve-cobrir/{}'

# O objetivo é que o código baixe os arquivos solicitados utilizando o nome do arquivo como índice da lista.
# a biblioteca zipfile foi importada para que os arquivos baixados fossem agrupados num arquivo "Anexos_agrupados.zip", conforme solicitado no teste.
compactado = 'Anexos_agrupados.zip'
agrupar_arquivos = zipfile.ZipFile(compactado, 'w', zipfile.ZIP_DEFLATED)
# O for foi utilizado para varrer o vetor lista_de_arquivos a fim de concatenar o nome do arquivo contido nos elementos da lista com o conteúdo da variável BASE_URL, que contém o link para download.
for item in lista_de_arquivos:
    baixar_arquivos(BASE_URL.format(item), item)
    agrupar_arquivos.write(item)
    print("Arquivo {} agrupado em {}!".format(item, compactado))

agrupar_arquivos.close()
print("Fim.")




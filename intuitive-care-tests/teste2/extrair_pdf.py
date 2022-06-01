# Teste 2: Transformação de Dados
# Código desenvolvido para extrair os dados do PDF Anexo I do Teste 1 para processo seletivo da empresa Intuitive Care.
# Autor: Pedro Minaré, Data: 26/05/2022 | Link do código em funcionamento: https://youtu.be/SohGcuHu_Go

# Bibliotecas Utilizadas
from os import sep # Responsável por indicar um delimitador para o CSV.
import tabula as tb # Responsável por extrair tabelas de documentos no formato PDF.
import pandas as pd # Responsável por elaborar e organizar DataFrames em Python.
import zipfile, csv; # Responsável por compactar arquivos | manipular arquivos CSV.

# Passo a passo para a construção do código.
# O arquivo Anexo I tem seu diretório recebido na variável "file".
print("# Transformação de Dados #\n Autor: Pedro Minaré\n Data: 26/05/2022\n")
file = "https://www.gov.br/ans/pt-br/arquivos/assuntos/consumidor/o-que-seu-plano-deve-cobrir/Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536.pdf"

# A biblioteca tabula foi utilizada para realizar a leitura do documento PDF indicado.
# O documento possui tabelas a partir da página 3 até a última página (200).
# A ideia do código é unir as tabelas de todas as páginas de modo a construir um CSV com os dados das tabelas em apenas uma planilha.
tabela = tb.read_pdf(file, pages="3-200", multiple_tables=True, stream=True, lattice=True)
print("Os dados do PDF foram lidos. Páginas 3 a 200.\n")

# A biblioteca Pandas foi utilizada para concatenar as tabelas ignorando os índices criados no dataframe.
lista_tabelas = pd.concat(tabela, ignore_index=True)
print("A tabela foi concatenada.\n")

# Um dataframe foi criado e atribuído na variável "writer"
writer = pd.DataFrame(lista_tabelas)
print("O dataframe foi criado.\n")

# o documento "dados.csv" é criado e os dados são escritos, definindo um delimitador como sendo ";" a fim de que o preenchimento ocorra de forma organizada em suas devidas colunas.
nome = "dados.csv"
writer.to_csv(nome, index=False, sep=";", encoding='utf-8-sig')
print("O arquivo {} foi criado com todos os dados importados do PDF!\nGerando arquivo compactado...\n".format(nome))

# funcao para compactar
def compactar(arquivo, compactado):
    zipar = zipfile.ZipFile(compactado, 'w', zipfile.ZIP_DEFLATED)
    zipar.write(arquivo)
    print("Arquivo {} compactado em {}!\n".format(arquivo, compactado))
    zipar.close()

# zipando arquivo criado.
compactar(nome, "Teste_{Pedro_Minaré}.zip")
print("Fim da execução.")

README

#### Esboço para realização do teste 3
O documento final é o "Teste 3 - Banco de dados.pdf"

Acesso ao MySQL: mysql -u root -p password
exibir as databases: show databases;
selecionar a database: use nome_da_database;
exibir as tabelas: show tables;

Todos os documentos .csv foram convertidos para o encoding utf-8.

Para importar os arquivos de 2020: (os dados estavam entre aspas duplas e delimitados por ;)
LOAD DATA INFILE 'cadop/2020/1T2020.csv' INTO TABLE 1t2020 FIELDS TERMINATED BY ';' ENCLOSED BY '"' IGNORE 1 LINES;

para importar os arquivos de 2021, os dados estavam apenas delimitados por ;
LOAD DATA INFILE 'cadop/2021/1T2021.csv' INTO TABLE 1t2021 FIELDS TERMINATED BY ';' IGNORE 1 LINES;

Aumentar o limite de tamanho de arquivos para importacao:
set global net_buffer_length=1000000; 
set global max_allowed_packet=1000000000;

# desabilitar a verificação de chave estrangeira:
SET FOREIGN_KEY_CHECKS=0;

para importar após entrar no mysql via prompt: 
use database_name;
source filename.sql;

Teste 3 - Bancos de Dados

##
Tarefas de Preparação (podem ser feitas manualmente):

Baixar os arquivos dos últimos 2 anos no repositório público: http://ftp.dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/

Baixar csv anexo:
Relatorio_cadop(1) (esta em anexo no e-mail)

As tarefas abaixo devem ser executadas em código na linguagem SQL em um banco PostgreSQL ou MySQL

Criar queries para criar tabelas com as colunas necessárias para o arquivo csv.
Queries de load: criar as queries para carregar o conteúdo dos arquivos obtidos nas tarefas de preparação
Atenção ao encoding dos arquivos no momento da importação!
Montar uma query analítica que traga a resposta para as seguintes perguntas:
Quais as 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?
Quais as 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último ano?
##

O primeiro passo foi baixar e analisar os documentos.csv disponibilizados no site http://ftp.dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/

Assim que tive acesso aos documentos.csv, analisei como os dados estavam estruturados (colunas, delimitadores, tipos de dados, etc.)
Pude verificar que alguns documentos estavam com "encodings" diferentes entre si; 
assim, tomei a liberdade de converter TODOS os documentos (relatorio_cadop.csv e os arquivos dos últimos 2 anos no repositório público) para o formato "utf-8" utilizando o editor de textos "Notepad++".
Após convertidos, alguns documentos apresentaram o delimitador ";", e outros, além do delimitador, estavam contidos em aspas duplas, recurso comum entre os arquivos.csv.
Foi possível observar que, no Excel, os documentos apresentavam símbolos desconhecidos no lugar de letras com acento, "ç" e outros, em virtude da não-conversão do "encoding" para utf-8.
Utilizando o XAMPP, instalei o Apache, o MySQL, configurei o acesso, adicionei as variáveis de ambiente para operar também pelo Windows PowerShell e instalei também o PhpMyAdmin.
Criei o banco de dados "cadop", seguindo o padrão pelo nome do documento (relatorio_cadop.csv).
Criei 2 tabelas: relatorio, dados.

A tabela "relatorio" foi responsável por armazenar os dados do documento "relatorio_cadop.csv".
A tabela "dados" foi responsável por armazenar os dados de todos os documentos pertinentes aos últimos 2 anos do repositório público.
Os arquivos com os dados dos últimos 2 anos identificados são:

##
1T2020.csv
1T2021.csv
2T2020.csv
2T2021.csv
3T2020.csv
3T2021.csv
4T2020.csv
4T2021.csv
##

Estes documentos também passaram pela conversão de "encoding" para "utf-8".
O documento "dicionario_demonstracoes_contabeis.ods", encontrado no repositório público, apresenta algumas observações com relação aos tipos de dados e tamanho dos campos.
Me orientei em partes pelo conteúdo deste documento e tomei as decisões de tamanhos de campos e tipos de dados do banco de dados estipulando tamanhos de campo um pouco maiores.
Os tipos de dados dos campos do banco de dados foram levados em conta seguindo o documento "dicionario_demonstracoes_contabeis.ods".
Pude verificar que os dados dos últimos 2 anos tinham uma relação muito próxima com as especificações do documento "dicionario_demonstracoes_contabeis.ods".
Assim, tomei a liberdade de mesclar tais informações com a identificação mediante os dados apresentados nos documentos.csv.
É possível identificar que existe um dado em comum nas tabelas (o registro_ans na tabela relatorio e reg_ans na tabela dados).
Assim, decidi que a chave primária da tabela "relatorio" seria "registroans" (int (8)).
A chave estrangeira na tabela "dados" é, portanto, "reg_ans" (int (8)).
Assim foi possível relacionar as 2 tabelas.

O próximo passo foi criar as Queries para as solicitações do teste.
Para criar as queries tomei a liberdade de interpretar a solicitação mediante os dados que foram disponibilizados nos arquivos csv.
Para fins de organização e conferência dos resultados obtidos, estruturei a consulta SQL para exibir também:
Razao_Social
Registro_ANS
Quantidade de ocorrências da descrição solicitada por registro_ans
Data
Descrição
Soma de (Saldo Inicial) e (Saldo_Final) dos resultados obtidos pelo agrupamento de reg_ans,
Despesas (saldo_final - saldo_inicial)

Admitindo que as despesas sejam resultado da operação "saldo_final - saldo_inicial", decidi relacionar as 2 tabelas com JOIN,
pesquisando pela descrição "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR",
referentes ao último trimestre do ano em que houve registros (visto que os últimos registros são de 2021-10-01, considerei que a busca poderia ser entre as datas de 2021-12-31 e 2021-08-01), 
com saldo_final maior que 0 e exibindo os resultados do valor maior para o menor, limitando os primeiros 10 resultados.

Solicitação 1: Quais as 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último trimestre?

# Query com um nível de detalhamento razoável:
SELECT 
R.razaosocial as Razao_Social,
D.reg_ans as Registro_ANS_Dados,
count(D.reg_ans) as qt_regitros_na_tabela_dados,
D.data,
D.descricao as Descricao, 
SUM(D.vl_saldo_inicial) as Saldo_Inicial,
SUM(D.vl_saldo_final) as Saldo_Final,
(SUM(D.vl_saldo_final) - SUM(D.vl_saldo_inicial)) as Despesas
FROM relatorio R
JOIN dados as D ON R.registroans = D.reg_ans 
WHERE 
D.descricao = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"
AND
D.data BETWEEN '2021-08-01' AND '2021-12-31' 
AND
D.vl_saldo_final > 0 
GROUP BY D.reg_ans 
ORDER BY Despesas DESC 
LIMIT 10

# Query com menos detalhes:
SELECT 
R.razaosocial as Razao_Social, 
D.data, 
D.descricao as Descricao, 
(SUM(D.vl_saldo_final) - SUM(D.vl_saldo_inicial)) as Despesas 
FROM relatorio R 
JOIN dados as D ON R.registroans = D.reg_ans 
WHERE 
D.descricao = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" 
AND 
D.data BETWEEN '2021-08-01' AND '2021-12-31' 
AND 
D.vl_saldo_final > 0 
GROUP BY D.reg_ans 
ORDER BY Despesas DESC 
LIMIT 10

Solicitação 2: Quais as 10 operadoras que mais tiveram despesas com "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR" no último ano?

# Query com um nível de detalhamento razoável:
SELECT 
R.razaosocial as Razao_Social,
D.reg_ans as Registro_ANS_Dados,
count(D.reg_ans) as qt_regitros_na_tabela_dados,
D.data,
D.descricao as Descricao, 
SUM(D.vl_saldo_inicial) as Saldo_Inicial,
SUM(D.vl_saldo_final) as Saldo_Final,
(SUM(D.vl_saldo_final) - SUM(D.vl_saldo_inicial)) as Despesas
FROM relatorio R
JOIN dados as D ON R.registroans = D.reg_ans 
WHERE 
D.descricao = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"
AND
D.data BETWEEN '2021-01-01' AND '2021-12-31' 
AND
D.vl_saldo_final > 0 
GROUP BY D.reg_ans 
ORDER BY Despesas DESC 
LIMIT 10

# Query com menos detalhes:
SELECT 
R.razaosocial as Razao_Social,
D.data,
D.descricao as Descricao,
(SUM(D.vl_saldo_final) - SUM(D.vl_saldo_inicial)) as Despesas
FROM relatorio R
JOIN dados as D ON R.registroans = D.reg_ans 
WHERE 
D.descricao = "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"
AND
D.data BETWEEN '2021-01-01' AND '2021-12-31' 
AND
D.vl_saldo_final > 0 
GROUP BY D.reg_ans 
ORDER BY Despesas DESC 
LIMIT 10

####
# Quantidade de registros(linhas) por tabela considerando a primeira linha.

1T2020 - 679641
1T2021 - 688888
2T2020 - 672240
2T2021 - 723537
3T2020 - 686757
3T2021 - 742530
4T2020 - 865172
4T2021 - 907100
relatorio_cadop teste 3.csv - 1156 (total de registros ausentes: 1)

total de registros nas tabelas de dados: 5.965.865
total de registros no banco de dados: 5.965.857
Total de registros ausentes: 8
São 8 registros ausentes na tabela "dados" e 1 registro ausente na tabela "relatorio", portanto, a primeira linha de cada tabela não foi registrada.
###################################################################################################################################
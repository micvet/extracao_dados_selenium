# Projeto de Extração de Dados com Selenium
Este projeto utiliza Python e o framework Selenium para extrair dados diretamente do site do IBGE.

Para ambos os códigos, é necessário o download do arquivo "cidadesBRC.xlsx", no diretório arquivos. 

**1. Extração e Salvamento em Arquivo Excel (extract-data-save-as-xlxs)**
No diretório "extract-data-save-as-xlxs", você encontrará o código Python usado para extrair dados da página Cidades e Estados do IBGE. O código é organizado da seguinte forma:

1.1. Função regiao_br
Uma função que, com base no estado fornecido (UF), retorna a região a qual ele pertence.

1.2. Função extractData
Inicia o processo de extração. É necessário fornecer cidade (city) e estado (state). Esses dados são obtidos a partir do arquivo "cidadesBRC.xlsx", localizado no diretório "data". Os dados extraídos são salvos nas listas "linha" e "planilha".

1.3. Função main
Na função principal, informe o diretório do arquivo "cidadesBRC.xlsx". O arquivo é lido pelo Pandas, e cada linha e coluna são usadas como parâmetros para a função "extractData". Os dados são então transformados em um DataFrame e salvo como arquivo Excel.

![image](https://github.com/micvet/data-extraction-selenium-ibge/assets/86981990/bc56502d-1956-43fa-9cc0-cbbcfd877459)


**2. Extração e Salvamento em Banco de Dados PostgreSQL (extract-data-sql)**
No diretório "extract-data-sql", você encontrará o código Python usado para extrair dados do site do IBGE e salvá-los em um banco de dados PostgreSQL.

2.1. Criação e preparação do Banco de Dados
No diretório constam os arquivos com o código utilizado para construção do banco de dados, tabela, Function, bem como pela população dos dados das tabelas uf e regiao.
![image](https://github.com/micvet/data-extraction-selenium-ibge/assets/86981990/a2b6fd7b-f132-408b-b828-083e2ac08b66)

2.2. Funções SQL e Python
O código Python se inicia com a importação de bibliotecas necessárias. A função extractData inicia o processo de extração. A função obter_id_uf retorna o ID da UF correspondente ao banco de dados. A função processData organiza a execução das funções anteriores e retorna uma única linha com os dados necessários.

2.3. Função main
A função principal estabele conexão com o banco de dados, lê o arquivo xlxs com os dados das cidades e estados, necessário para iterar nas páginas do IBGE. Após a extração dos dados, usa-se a Function insere_dados para inserir os dados no banco de dados PostgreSQL.

![image](https://github.com/micvet/data-extraction-selenium-ibge/assets/86981990/1a42fb84-dffa-4544-8720-0ac8753e47be)


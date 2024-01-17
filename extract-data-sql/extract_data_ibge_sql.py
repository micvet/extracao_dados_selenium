from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import psycopg2 

options = Options() 
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)


def extractData (state,city):
    #Função para remover caracteres indesejáveis, remover vírgulas, ajustar os pontos finais e tranformar o resultado em float.
    def formatValue(numero, caracter=""):
        try:
            remove_caracter = (numero.split(caracter)[0])
            formata_numero = (remove_caracter.replace(".", "").replace(",", "."))
            dados_float = float(formata_numero)
            return dados_float
        except:
            dados_float = 0
            return dados_float

    driver.get(f"https://www.ibge.gov.br/cidades-e-estados/"+state+ "/"+city+".html")

    #Extraindo os dados do site:

    objeto_prefeito = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "ind-value")))
    prefeito = (objeto_prefeito.text).split("[")[0]
  
    dados_area_territorial = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[0].text
    area_territorial = formatValue(dados_area_territorial, "k")   
  
    dados_populacao = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[1].text
    populacao = formatValue(dados_populacao, "p")


    dados_densidade = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[2].text
    densidade = formatValue(dados_densidade, "h")


    dados_escolarizacao = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[3].text
    escolarizacao = formatValue(dados_escolarizacao, "%")

    dados_idhm = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[4].text
    idhm = formatValue(dados_idhm, " ")
  
    dados_mortalidade_infantil = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[5].text
    mortalidade_infantil = formatValue(dados_mortalidade_infantil, "ó")

    dados_receitas_realizadas = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[6].text
    receitas_realizadas = formatValue(dados_receitas_realizadas, "R")

    dados_despesas_empenhadas = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[7].text
    despesas_empenhadas = formatValue(dados_despesas_empenhadas, "R")
 
    dados_pib = driver.find_element(By.CLASS_NAME,"resultados-padrao").find_elements(By.CLASS_NAME, "ind-value")[8].text
    pib = formatValue(dados_pib, "R")

    return [prefeito, area_territorial, populacao, densidade, escolarizacao, idhm, mortalidade_infantil, receitas_realizadas, despesas_empenhadas, pib]


def obter_id_uf(uf):
    uf_id_map = {
        'AC': 1,
        'AL': 2,
        'AM': 3,
        'AP': 4,
        'BA': 5,
        'CE': 6,
        'DF': 7,
        'ES': 8,
        'GO': 9,
        'MA': 10,
        'MG': 11,
        'MS': 12,
        'MT': 13,
        'PA': 14,
        'PB': 15,
        'PE': 16,
        'PI': 17,
        'PR': 18,
        'RJ': 19,
        'RN': 20,
        'RO': 21,
        'RR': 22,
        'RS': 23,
        'SC': 24,
        'SE': 25,
        'SP': 26,
        'TO': 27,
    }
    return uf_id_map.get(uf)

def processData(row):
    cidade = row[1]
    uf_id = obter_id_uf(row[0])
    uf = row[0]
    dados = extractData(uf, cidade)
    return [uf_id, cidade] + dados

def main():
    
    caminho_df= input("Insira o caminho para o arquivo cidadesBRC.xlsx: ")
    

    db_params = {
    'host': 'localhost',
    'database': 'geo_ibge_data',
    'user': 'postgres',
    'password': '12345',
    }

    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
    except:
        print ("A conexão não pode ser estabelecida.")


    dataframe = (f"{caminho_df}")
    dados_excel = pd.read_excel(dataframe)

    planilha = []

    num = 1

    # Iterando entre as linhas do arquivo para realizar a busca:
    for row in dados_excel.itertuples(index=False):
        resultado = processData(row)
        planilha.append(resultado)
   
        cursor.callproc('insere_dados', (resultado[0], resultado[1], resultado[2],resultado[3],resultado[4],resultado[5],resultado[6],resultado[7],resultado[8],resultado[9],resultado[10],resultado[11]))

        # Commit no banco de dados
        conn.commit()
        
        cid = resultado[1]
        print (num, "-",cid)
        num = num+1

    
    # Fechando a conexão
    cursor.close()
    conn.close()
    # Fechando o WebDriver
    driver.quit()

# Chamando a função para iniciar
if __name__ == "__main__":
    main()



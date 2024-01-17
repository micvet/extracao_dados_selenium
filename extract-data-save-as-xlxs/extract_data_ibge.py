from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = Options() 
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

def brRegion(UF):

    if UF in ["AC", "AP", "AM", "PA", "RO", "RR", "TO"]:
        return "NORTE"
    elif UF in ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]:
        return "NORDESTE"
    elif UF in ["DF", "GO", "MT", "MS"]:
        return "CENTRO-OESTE"
    elif UF in ["ES", "MG", "RJ", "SP"]:
        return "SUDESTE"
    elif UF in ["PR", "RS", "SC"]:
        return "SUL"   

def extractData (state,city):
    #Função para remover caracteres indesejáveis, remover vírgulas, ajustar os pontos finais e tranformar o resultado em float.
    def formatValue(numero, caracter=""):
        try:
            remove_caracter = (numero.split(caracter)[0])
            formata_numero = (remove_caracter.replace(".", "").replace(",", "."))
            dados_float = float(formata_numero)
            return dados_float
        except:
            dados_float = "null"
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

def processData(row):
    uf, cidade = row[0], row[1]
    regiao = brRegion(uf)
    dados = extractData(uf, cidade)
    return [uf, cidade, regiao] + dados

def main():
    
    caminho_df= input("Insira o caminho para o arquivo cidadesBRC.xlsx: ")
    destino_xlxs = input("Insira a pasta de destino do arquivo gerado, no formato pasta\pasta\ :")

    dataframe = (f"{caminho_df}")
    dados_excel = pd.read_excel(dataframe)

    planilha = []

    num = 1

    # Iterando entre as linhas do arquivo para realizar a busca:
    for row in dados_excel.itertuples(index=False):
        resultado = processData(row)
        planilha.append(resultado)
        cid = resultado[1]
        print (num, "-",cid)
        num = num+1

    # Transformando a lista em dataframe
    df = pd.DataFrame(planilha, columns=['UF', 'Cidade', 'Região', 'Prefeito', 'Território (km² [2022])',
                                          'População (pessoas [2022])', "Densidade (hab/km² [2022])",
                                          "Escolarização (% [2010])", "IDHM [2010]",
                                          "Mortalidade Infantil (óbitos por mil nascidos vivos [2020])",
                                          "Receitas (R$ [2017] x 1000)", "Despesas (R$ [2017] x 1000)", "PIB per capta (R$ [2021])"])
    
    # Transformando o dataframe em arquivo xlsx.
    df.to_excel(f"{destino_xlxs}{"data_ibge"}.xlsx")

    # Fechando o WebDriver
    driver.quit()

# Chamando a função para iniciar
if __name__ == "__main__":
    main()

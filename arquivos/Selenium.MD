
O Selenium é uma ferramenta de automação que permite automatizar a interação com aplicativos da web em diferentes navegadores. 
Ele utiliza o WebDriver, uma API e protocolo que define uma maneira padronizada de controlar o comportamento dos navegadores. Cada navegador é suportado por um 
driver específico, responsável por facilitar a comunicação entre o Selenium e o navegador.

A separação entre o Selenium e os drivers visa incentivar os fabricantes de navegadores a assumirem a responsabilidade pela compatibilidade de seus 
próprios navegadores. 

O framework Selenium oferece uma interface que simplifica a automação testes e de web scraping em diferentes navegadores e plataformas. Isso possibilita a 
realização do trabalho de forma consistente e com confiabilidade dos resultados.

A configuração do Selenium é única, exigindo a instalação do navegador desejado e do driver correspondente antes de iniciar a escrita do código de automação. 
Essa preparação prévia é essencial para garantir um ambiente adequado para a execução do código.

Exemplos de comandos utilizados para automaçao com Selenium, com a linguagem Python:

* Abrir uma página web:

'''
driver.get("https://www.exemplo.com")
''' 

* Localizar um elemento por ID:

'''
elemento = driver.find_element_by_id("id_do_elemento")
'''

* Localizar um elemento por nome:

'''
elemento = driver.find_element_by_name("nome_do_elemento")
'''

* Localizar um elemento por classe:

'''
elemento = driver.find_element_by_class_name("nome_da_classe")
'''

Localizar um elemento por XPath:

'''
elemento = driver.find_element_by_xpath("caminho_para_o_elemento")
'''

* Clicar em um elemento:
'''
elemento.click()
'''

* Preencher um campo de texto:
'''
elemento.send_keys("texto_para_preencher")
'''

* Esperar um elemento estar visível:
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID,"id_do_elemento")))
'''

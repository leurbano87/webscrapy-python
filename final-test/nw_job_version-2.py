#ler arquivo do excel
import openpyxl
import pandas as pd

#automatizar o navegador
from selenium import webdriver #navegador
from selenium.webdriver.common.by import By #buscar os elementos
from selenium.webdriver.common.keys import Keys #digitar no teclado web

from bs4 import BeautifulSoup

from time import sleep

#campo de busca CEP ou Rua  = XPATH = //*[@id="endereco"]
#botao buscar               = XPATH = //*[@id="btn_pesquisar"]

# URL do site para busca do CEP ou Endereço
url = "https://buscacepinter.correios.com.br/app/endereco/index.php"

#Local da da Base de dados em excel
lista = "pasta_a\lista.xlsx"
#leitura do arquivo excel
dados = pd.read_excel(lista)

for index,row in dados.iterrows():
    navegador = webdriver.Chrome(executable_path='chromedriver.exe')
    navegador.get(url)
    sleep(2) #APOS ABRIR O NAVEGADOR IRA AGUARDAR 2 SEGUNDOS

    #NESTE PONTO PRECISO CRIAR UMA CONDICIONAL QUE LEIA A PLANILHA NA COLUNA CRITERIO
    #E DE ACORDO COM A CELULA VERIFICAR SE VAI PESQUISAR POR RUA OU CEP E CASO ESTIVER
    #A CELULA DE CRITERIO ESTIVER VAZIA RECUSAR A BUSCA 

    #caso deseje adicionar um Input para o usuário escolher o tipo pesquisa
    #var_pesquisa = input("Deseja pesquisar por cep("c") ou rua("r")? c/r: " )
    var_pesquisa = 'r'
    if var_pesquisa == 'r':
        #Realizando a buscar por RUA
        busca_cep = navegador.find_element(By.XPATH,'//*[@id="endereco"]')
        busca_cep.send_keys(row["rua"])
    else:
        #Realizando a buscar por CEP
        busca_cep = navegador.find_element(By.XPATH,'//*[@id="endereco"]')
        busca_cep.send_keys(row["cep"])

    #Clicar no botao Buscar
    bt_buscar = navegador.find_element(By.XPATH,"//*[@id='btn_pesquisar']")
    bt_buscar.click()
    sleep(2)

    #Acessando a tabela do resultado da busca
    tbResultado = navegador.find_element(By.ID, value="resultado")
    conteudo = tbResultado.get_attribute("outerHTML")

    #Extraindo a tabela do HTML
    soup = BeautifulSoup(conteudo,"html.parser")
    tb_final = soup.find(name="table")
    

    #NESSA PONTO PRECISO QUE ELE SALVE AS PESQUISAS EM UMA ÚNICA PLANILHA

    dados = pd.read_html(str(tb_final))[0]
    dados.to_csv("pasta_b\lista_saida.csv",encoding="UTF-8",sep=";", mode = 'a', header = False, index=True)

    navegador.quit()

 
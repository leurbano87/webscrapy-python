from attr import attr
import requests
from bs4 import BeautifulSoup

url = 'https://www.amazon.com.br/s?k=iphone&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2U0JE0YIC7SIU&sprefix=iphone%2Caps%2C478&ref=nb_sb_noss_1'


site = requests.get(url)
soup = BeautifulSoup(site.text, 'html.parser')
iphones = soup.find_all('div', class_='a-section a-spacing-base')

iphones_all = []

with open ('consulta_iphones.csv', 'a', newline='', encoding='UTF-8') as f:


        for lista in iphones:
                produto = soup.find('div', class_='a-section a-spacing-small puis-padding-left-small puis-padding-right-small')
                titulo = produto.find('span', class_='a-size-base-plus a-color-base a-text-normal').get_text() .strip()
                preco =  produto.find('span', class_='a-price-whole').get_text() .strip()
                num_preco = preco[:-1]
                link = produto.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')['href']
                iphones_all.append({
                        'Titulo': titulo,
                        'Preco': num_preco,
                        'Link': link,})

                linha = titulo + ';' + num_preco + ';' + 'http://amazon.com.br' + link + '\n'
                print(linha)
                f.write(linha)

print(iphones_all)



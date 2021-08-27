from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://myanimelist.net/topanime.php?limit={}'
links = []
##valor que cambia todo
a = 18 ##Con este valor se va iterando cada 20 paginas para retener los links de los 1000 animes que se encuentran en esas páginas
for i in range((a-1)*20,(a)*20):
	formato = i*50 ##Para avanzar en el link de la pagina
	page = requests.get(url.format(formato))
#print(page.text)
# se construye el objeto con el contenido de la página web
	soup = BeautifulSoup(page.content, 'html.parser')
#buscamos en esta seccion que contiene los hipervinculos de la pagina
	soup_info = soup.find_all('h3')
	links_pag = []
	for i in soup_info:
	#con esto extraemos el link de cada anime en la lista
		link = i.a['href']
	#nos aseguramos que sea un link hacia un anime y no otra cosa
		if "/anime/" in link:
		#print(link)
			links_pag.append(link)
	links = links+links_pag
#print(links)
data = {'Link': links}
df = pd.DataFrame(data, columns = ['Link'])
print(df)
##guardamos los links en diferentes archivos que luego se juntarán
df.to_csv ('links_myanimelist{}000.csv'.format(a), sep = ';', index  = False)

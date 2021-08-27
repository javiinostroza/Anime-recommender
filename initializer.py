from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_info(lista, elemento):
	if elemento == None:
		pass
	#https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
	#saque el usar un find para encontrar los elementos que queremos quitar
	elif elemento.string.find(',') == 1 or elemento.string.find(',') == 0 or (elemento.string.find(' ') == 0 and len(elemento) < 1) or elemento.string.find('\n') != -1:
		get_info(lista,elemento.next_sibling)
	elif elemento.string.find('add some') != -1: #Si no tiene la info
		lista.append(None)
		get_info(lista,elemento.next_sibling)
	else:
		if elemento.string == ' ':
			get_info(lista,elemento.next_sibling)
		else:
			lista.append(elemento.string.strip())
			get_info(lista,elemento.next_sibling)

def get_genre(lista, elemento):
	##https://living-sun.com/es/python/708999-get-itemprop-with-beautifulsoup-python-beautifulsoup.html
	for i in elemento:
		lista.append(i.string)
	if len(elemento) == 0:
		lista.append(None)

def get_string(elemento):
	if elemento == None:
		pass
	else:
		return elemento.string.strip()

def get_type (soup):
	Tipo = soup.find('span', string = 'Type:').next_element.next_element
	if Tipo == '\n':
		Tipo = sopita.find('span', string = 'Type:').next_element.next_element.next_element.string.strip()
	else:
		Tipo = Tipo.strip()
	return Tipo

def get_voiceactors(lista,elementos):
	for i in range(len(elementos)):
		elemento = elementos[i].next_sibling.next_sibling.small
		nombre = None
		if elemento == None: pass
		elif elemento.string == 'Main':
			siguiente = elemento.next_sibling
			while siguiente == '\n':
				##https://www.kite.com/python/examples/1742/BeautifulSoup-find-the-next-element-after-a-tag
				##de aqui saque la función next_element
				siguiente = siguiente.next_element
			if siguiente.a == None: pass
			else:
				nombre = siguiente.a.string
			lista.append(nombre)
	if len(lista) == 0:
		lista.append(None)

def get_everything(soup):
	Genre = []
	Studios = []
	Producers = []
	Licensors = []
	Voice_Actors = []
	#https://www.programiz.com/python-programming/methods/string/strip#:~:text=The%20strip()%20method%20returns,of%20characters%20to%20be%20removed).
	##Para poder remover los espacios desde cada lado del string se usa strip()
	Name = soup.title.string.strip()
	Name = Name[:Name.find(' - MyAnime')]
	Type = get_type(sopita)
	Aired = get_string(sopita.find('span', string = 'Aired:').next_sibling)
	Episodes = get_string(sopita.find('span', string = 'Episodes:').next_sibling)
	Rating = get_string(sopita.find('span', itemprop = 'ratingValue'))
	get_genre(Genre, sopita.find_all('span', itemprop = 'genre'))
	get_info(Studios, sopita.find('span', string = 'Studios:').next_sibling)
	get_info(Producers, sopita.find('span', string = 'Producers:').next_sibling)
	get_info(Licensors, sopita.find('span', string = 'Licensors:').next_sibling)
	get_voiceactors(Voice_Actors,sopita.find_all('h3'))
	return [Name, Rating, Type, Aired, Episodes, Genre, Studios, Producers, Licensors, Voice_Actors]

def get_ID(link):
	ID = link[link.find('anime/')+6:]
	ID = ID[:ID.find('/')]
	return ID

##Toda la información detallada se encuentra en el archivo scraping de a poco, este caso es solo para iniciar el scraping
initializer = 0
links  = pd.read_csv('links_myanimelist.csv', sep = ';')
for i in range(0,5):##(a-1)*1000
	print(links['Link'][i])
	paginita = requests.get(links['Link'][i])
	sopita = BeautifulSoup(paginita.content, 'html.parser')
	datos = get_everything(sopita)
	print(datos)
	ID = get_ID(links['Link'][i])
	new_row = {
			'ID': ID,
			'Name': [datos[0]],
			'Rating': [datos[1]],
			'Type': [datos[2]],
			'Aired': [datos[3]],
			'Episodes': [datos[4]],
			'Genre': [datos[5]],
			'Studios': [datos[6]],
			'Producers': [datos[7]],
			'Licensors': [datos[8]],
			'Voice_Actors': [datos[9]],
			'Link': [links['Link'][i]]}
	df = pd.DataFrame(new_row, columns = ['ID', 'Name', 'Rating', 'Type', 'Aired', 'Episodes',
		'Genre', 'Studios', 'Producers', 'Licensors', 'Voice_Actors','Link'])
	if initializer == 0: ##Si es la primera fila
		df.to_csv('data.csv', sep = ';', index=False)
		initializer = 1
	else: ##Agrega unas pocas filas más para tener el archivo
		df.to_csv('data.csv', sep = ';', mode = 'a', header=False, index=False)
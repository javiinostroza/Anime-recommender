from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

def get_info(lista, elemento):
	if elemento == None:
		pass
	#https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
	#saque el usar un find para encontrar los elementos que queremos quitar
	elif elemento.string.find(',') == 1 or elemento.string.find(',') == 0 or (elemento.string.find(' ') == 0 and len(elemento) < 1) or elemento.string.find('\n') != -1:
		#estos son los casos problemáticos, saltamos al siguiente sibling, elemento del mismo nivel
		get_info(lista,elemento.next_sibling)
	elif elemento.string.find('add some') != -1: #Si no tiene la info
		lista.append(None)
		get_info(lista,elemento.next_sibling) ##seguimos buscando, por si acaso saliera otro dato
	else:
		if elemento.string == ' ': ##Si es justo un espacio que por abc motivo paso, aqui se filtra
			get_info(lista,elemento.next_sibling)
		else:
			lista.append(elemento.string.strip()) ##finalmente se agrega el elemento y se revisa si existe uno siguiente
			get_info(lista,elemento.next_sibling)

def get_genre(lista, elemento):
	##https://living-sun.com/es/python/708999-get-itemprop-with-beautifulsoup-python-beautifulsoup.html
	for i in elemento: ##los elementos de la lista según itemprop genre son iterados aqui
		lista.append(i.string)
	if len(elemento) == 0: ##si no existe una lista de elementos, no hay genero
		lista.append(None)

def get_string(elemento):
	if elemento == None: ##Si no existe un string, no se hace nada ya que inicialmente se definen como None
		pass
	else:
		return elemento.string.strip()

def get_type (soup): ##Con esta función se obtiene el tipo de anime que es, fue un poco más complejo que los otros datos
	Tipo = soup.find('span', string = 'Type:').next_element.next_element ##Se avanzan dos elementos (hardcodeado) para llegar hasta donde se necesita
	if Tipo == '\n': ##Si existe ese elemento, hay que avanzar esa cantidad de elementos para llegar, el mismo codigo de la pagina lo tiene asi
		Tipo = sopita.find('span', string = 'Type:').next_element.next_element.next_element.string.strip()
	else: ##Si existe un tipo, se eliminan los espacios y se entrega
		Tipo = Tipo.strip()
	return Tipo

def get_voiceactors(lista,elementos):
	for i in range(len(elementos)): ##Los voice_actors son retirados para solo los personajes principales
		elemento = elementos[i].next_sibling.next_sibling.small #Avanza hardcodeado, buscando small, que es como la página escribe la palabra "Main"
		nombre = None
		if elemento == None: pass
		elif elemento.string == 'Main': ##Una vez que encuentra el elemento, avanza hasta el siguiente elemento hasta llegar al nombre
			siguiente = elemento.next_sibling
			while siguiente == '\n':
				##https://www.kite.com/python/examples/1742/BeautifulSoup-find-the-next-element-after-a-tag
				##de aqui saque la función next_element
				siguiente = siguiente.next_element ##se itera hasta que se obtiene un nombre o algo diferente del \n
			if siguiente.a == None: pass #Si no hay un nombre se pasa
			else: ##Se agrega el nombre del actor de voz a la lista
				nombre = siguiente.a.string
			lista.append(nombre)
	if len(lista) == 0: ##Si no hay ningun actor de voz luego de toda la iteración, le agrega el None
		lista.append(None)

def get_everything(soup): ##Esta función junta todo lo anterior
	##Inicializamos las listas necesarias
	Genre = []
	Studios = []
	Producers = []
	Licensors = []
	Voice_Actors = []
	#https://www.programiz.com/python-programming/methods/string/strip#:~:text=The%20strip()%20method%20returns,of%20characters%20to%20be%20removed).
	##Para poder remover los espacios desde cada lado del string se usa strip()
	Name = soup.title.string.strip() ##El nombre se saca directamente del HTML
	Name = Name[:Name.find(' - MyAnime')] ##Se le quita el nombre de la página al nombre del anime
	Type = get_type(sopita)
	##Para estos datos, se avanza al siguiente elemento del mismo nivel, ya que el algoritmo encuentra el valor que viene antes con el find()
	Aired = get_string(sopita.find('span', string = 'Aired:').next_sibling)
	Episodes = get_string(sopita.find('span', string = 'Episodes:').next_sibling)
	Rating = get_string(sopita.find('span', itemprop = 'ratingValue')) ##Este elemento y el siguiente contienen clasificaciones dentro de la misma página por lo que es más sencillo de obtener
	get_genre(Genre, sopita.find_all('span', itemprop = 'genre'))
	get_info(Studios, sopita.find('span', string = 'Studios:').next_sibling)
	get_info(Producers, sopita.find('span', string = 'Producers:').next_sibling)
	get_info(Licensors, sopita.find('span', string = 'Licensors:').next_sibling)
	get_voiceactors(Voice_Actors,sopita.find_all('h3')) ##los elementos de voice actors están clasificados con h3, dentro de esa lista se buscarán los nombres
	return [Name, Rating, Type, Aired, Episodes, Genre, Studios, Producers, Licensors, Voice_Actors] ##Una lista con todos los datos del anime

def get_ID(link):
	ID = link[link.find('anime/')+6:]
	ID = ID[:ID.find('/')]
	return ID

links  = pd.read_csv('links_myanimelist.csv', sep = ';') ##Este archivo contiene los links de cada anime de la página
#ir de a 1000 animes para evitar errores, el scrapping se demora 1:15 - 1:30 hrs por cada 1000 datos
#a = 18 ##Este numero se cambia segun se quiera, puede incluso no utilizarse
##Lo importante es que el range de i vaya entre cierto intervalo que vaya desde donde quedo el algoritmo hasta un numero deseado
for i in range(5,len(links)):##range((a-1)*1000,a*1000) ###La posicion es +2 en el archivo data, como el initializer termina en la quinta posición, se debe comenzar desde allí range(5,len(links)) sería el rango completo
	##Hacemos el request de cada link y su soup correspondiente
	paginita = requests.get(links['Link'][i])
	sopita = BeautifulSoup(paginita.content, 'html.parser')
	##Con esta función se obtienen todos los datos del anime
	datos = get_everything(sopita)
	ID = get_ID(links['Link'][i])
	##Esta nueva fila tendrá los diferentes datos del anime
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
	##Printeamos el link para ir monitoreando donde queda el algoritmo en caso de falla
	print(new_row['Link'][0])
	##Con esto generamos la fila nueva de datos, la primera fila fue creada anteriormente, por lo que podemos comenzar desde el segundo elemento
	df = pd.DataFrame(new_row, columns = ['ID', 'Name', 'Rating', 'Type', 'Aired', 'Episodes',
		'Genre', 'Studios', 'Producers', 'Licensors', 'Voice_Actors','Link'])
	#https://stackoverflow.com/questions/17530542/how-to-add-pandas-data-to-an-existing-csv-file
	##asi podemos agregar una fila a un archivo ya existente
	#append row to the dataframe
	df.to_csv('data.csv', sep = ';', mode = 'a', header=False, index=False)
	##https://realpython.com/python-sleep/ para dar un delay y que los servidores me permitan hacer scrapping
	time.sleep(random.randint(1,5))

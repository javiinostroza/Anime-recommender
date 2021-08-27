# RepoBaseProyecto - Grupo 05
Gonzalo Barros - Javiera Inostroza - Sebastián León - Samuel Zúñiga

## Importante
+ La documentación de esta entrega se encuentra en  `/Documentación/Presentación de Propuesta y Avance.pdf`
+ Para utilizar los notebooks, antes instalar las siguientes libreras: 
```
  pip3 install pyreclab
  pip3 install lenskit
  pip3 install AST
```


## Descripción de los archivos ejecutables

1. scrape links.py : encargado de obtener los links para realizar el web scrapping de los animes de la página Myanimelist.

2. add_links.py: encargado de agregar los links extraidos a un mismo archivo csv

3. initializer.py: inicializa el archivo donde se guarda el webscrapping de los animes, es necesario utilizarlo antes que scraping de a poco.py

4. scraping de a poco.py : encargado de realizar el webscrapping de la lista 

5. female_users_scrapping.ipynb: encargado de realizar el webscrapping de las calificaciones de los usuarios de género femenino.

6. male_users_scrapping.ipynb: encargado de realizar el webscrapping de las calificaciones de los usuarios de género masculino

7. non_binary_users_scrapping.ipynb: encargado de realizar el webscrapping de las calificaciones de los usuarios de género no binario.

8. Limpieza de datos de animes.ipynb: encargado de realizar la limpieza de datos de los animes y de analizar sus datos

9. users_preprocessing.ipynb: encargado de realizar la limpieza de datos de los usuarios y de analizar sus datos

10. knn-als_rec.ipynb: encargado de realizar predicciones y recomendaciones con los algoritmos knn-item, knn-user y als de LensKit.

11. pyreclab.ipynb: encargado de realizar predicciones y recomendaciones con los algoritmos user average, item average y slope one de PyRecLab

## Descripción de la distribución del repositorio

```
-
+-- Documentación/
| +-- Informe final.pdf
| +-- propuestas_proyecto.pdf
| +-- Presentación de Propuesta y Avance.pdf
+-- datasets_finales/
| +-- animes.csv
| +-- usuarios.csv
+-- links/
| +-- add_links.py
| +-- links_myanimelist1000.csv
| +-- links_myanimelist10000.csv
| +-- links_myanimelist11000.csv
| +-- links_myanimelist12000.csv
| +-- links_myanimelist13000.csv
| +-- links_myanimelist14000.csv
| +-- links_myanimelist15000.csv
| +-- links_myanimelist16000.csv
| +-- links_myanimelist17000.csv
| +-- links_myanimelist18000.csv
| +-- links_myanimelist2000.csv
| +-- links_myanimelist3000.csv
| +-- links_myanimelist4000.csv
| +-- links_myanimelist5000.csv
| +-- links_myanimelist6000.csv
| +-- links_myanimelist7000.csv
| +-- links_myanimelist8000.csv
| +-- links_myanimelist9000.csv
+-- scrapping_anime_list_by_user
| +-- female_ratings.csv
| +-- female_users.csv
| +-- female_users_scrapping.ipynb
| +-- male_ratings.csv
| +-- male_users.csv
| +-- male_users_scrapping.ipynb
+-- .gitignore
+-- Limpieza de datos de animes.ipynb
+-- README.md
+-- data.csv
+-- export_dataframe.csv
+-- initializer.py
+-- knn-als_rec.ipynb
+-- pyreclab.ipynb
+-- scrape links.py
+-- scraping de a poco.py
+-- users_preprocessing.ipynb
-
```

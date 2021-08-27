import pandas as pd

##https://www.geeksforgeeks.org/python-pandas-dataframe-append/#:~:text=append()%20function%20is%20used,are%20populated%20with%20NaN%20value.&text=ignore_index%20%3A%20If%20True%2C%20do%20not%20use%20the%20index%20labels.
##base para sumar los archivos de links
i = 1
df  = pd.read_csv('links_myanimelist{}000.csv'.format(i), sep = ';')
for i in range(2,19):
	df1 = pd.read_csv('links_myanimelist{}000.csv'.format(i), sep = ';')
	df = df.append(df1, ignore_index=True)
print(df)
df.to_csv ('links_myanimelist.csv', sep = ';', index  = False)
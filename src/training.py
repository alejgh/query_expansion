
# coding: utf-8

# # Expansión de consultas con Word2Vec
# Antes de ejecutar este notebook asegurate de que elasticsearch está iniciado. Además los tweets deben estar indexados. Para indexarlos ejecuta el script 'index.py'.
#
# ## Importando las librerías
# Primero vamos a importar las librerías que vamos a usar.

import elasticsearch.helpers
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from gensim.models import word2vec


# Las consultas que realizaremos a lo largo de la práctica son:


index = '2008-feb-02-04-en'
queries = ['American Football Conference', 'David Tyree','defensive end', 'Eli Manning','football', 'Glendale',
           'Laurence Maroney', 'Miami Dolphins', 'Michael Strahan', 'National Football Conference',
           'National Football League', 'New England Patriots', 'New York', 'New York Giants', 'NFL',
           'Plaxico Burress', 'quarterback', 'Randy Moss', 'running back', 'Super Bowl',
           'University of Phoenix', 'Wide receiver', 'XLII']


# La mitad de estas consultas serán para entrenar el modelo de Word2Vec, mientras que la otra mitad se usarán para realizar la expansión de consultas.

queries_train = queries[:len(queries)//2]
queries_test = queries[len(queries)//2:]


# ## Entrenamiento de Word2Vec
# Ahora vamos a realizar las consultas de entrenamiento en ElasticSearch para obtener los documentos con los que entrenaremos el modelo de Word2Vec.

client = Elasticsearch()
documents = []
for query in queries_train:
    s = Search(using=client, index=index).query("match", text=query)

    # al llamar a s.scan() utilizamos las características de scroll
    # de elasticsearch, por lo que no obtenemos todos los resultados
    for tweet in s.scan():
        documents.append(tweet.text)


# Una vez que tenemos los documentos de entrenamiento, necesitamos preparalos para que el modelo de Word2Vec los pueda procesar. Primero necesitamos separar cada tweet en una lista de palabras. Después, eliminaremos las palabras vacías de cada tweet para mejorar los resultados obtenidos con Word2Vec. Finalmente, eliminaremos símbolos de puntuación pegados a las palabras (por ejemplo, 'football,') para evitar añadir ruido al modelo:

import string
from stop_words import get_stop_words
stop_words = get_stop_words('english')

# creamos una tabla de traducción que usaremos a continuación para eliminar los simbolos de puntuación.
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
documents = [[word.translate(remove_punctuation_map) # eliminar simb. puntuacion de cada palabra
              for word in tweet.split(' ') if word not in stop_words] # dividir tweet en palabras y eliminar palabras vacías
              for tweet in documents]

model = word2vec.Word2Vec(documents, size=100, window=9, min_count=5, workers=4)

model.most_similar('football')


print(documents[0])

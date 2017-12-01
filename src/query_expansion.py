#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from elasticsearch_dsl import Search, Q


def get_expanded_query_w2v(model, q0, k=3):
    """ Esta función devuelve los términos expandidos
    respecto a q0 utilizando el modelo de Word2Vec,
    y devuelve una lista de listas con estos términos.
    Cada lista de la lista contiene una palabra de q0
    junto con las k palabras más similares de dicha palabra.
    """
    qe = []
    for word in q0.split(' '):
        expanded_words = [pair[0] for pair in model.most_similar(word)[:k]]
        expanded_words.append(word)
        qe.append(expanded_words)
    return qe


def get_expanded_query_glove(model, q0, k=3):
    """ Esta función devuelve los términos expandidos
    respecto a q0 utilizando el modelo de Glove.
    """
    qe = []
    for word in q0.split(' '):
        expanded_words = [pair[0] for pair in model.most_similar(word,
                                                                 number=k + 1)]
        expanded_words.append(word)
        qe.append(expanded_words)
    return qe


def get_elasticsearch_result(terms, client, index, num_results=10):
    """ Función que realiza una consulta a ElasticSearch sobre los
    términos 'terms' utilizando el cliente e index dados y devuelve
    uan lista con 'num_result' tweets tras aplicar la consulta.
    """
    queries = []
    for term in terms:
        queries.append(Q('match', text=' '.join(term)))
    q = Q('bool', should=queries)
    s = Search(using=client, index=index).query(q)
    result = [(res.text, res.meta.score) for res in s[:1000]]
    return result


def show_most_improved_tweet(original_tweets, expanded_tweets):
    """ Función que muestra por pantalla el tweet que más puestos
    subió en los resultados de ElasticSearch. Compara los tweets
    obtenidos al expandir la consulta con los tweets originales.
    """
    most_improved = ('', -1, -1, -1)
    for i, expanded_tweet in enumerate(expanded_tweets):
        for j, original_tweet in enumerate(original_tweets):
            if expanded_tweet == original_tweet and (j - i) > most_improved[1]:
                most_improved = (expanded_tweet, j - i, j, i)
    print("El tweet '{0}' subió {1} posiciones (desde la posicion {2} hasta la posicion {3})".format(*most_improved))


def show_most_devaluated_tweet(original_tweets, expanded_tweets):
    """ Función que muestra por pantalla el tweet que más puestos
    descendio en los resultados de ElasticSearch. Compara los tweets
    obtenidos al expandir la consulta con los tweets originales.
    """
    most_devaluated = ('', -1, -1, -1)
    for i, expanded_tweet in enumerate(expanded_tweets):
        for j, original_tweet in enumerate(original_tweets[:i]):
            if (expanded_tweet == original_tweet
                    and (i - j)) > most_devaluated[1]:
                most_devaluated = (expanded_tweet, i - j, j, i)
    print("El tweet '{0}' descendió {1} posiciones (desde la posicion {2} hasta la posicion {3})".format(*most_devaluated))

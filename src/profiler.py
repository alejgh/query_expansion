#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gensim.models import word2vec
from glove import Corpus
from glove import Glove

import matplotlib.pyplot as plt
import numpy as np


def word2vec_benchmark(sentences_iterable, size=100, window=5, alpha=0.025,
                       min_count=5, num_threads=1):
    """ Wrapper del constructor de Word2Vec para poder realizar mediciones
    de rendimiento (tiempo y memoria usadas para crear el modelo)
    """
    word2vec.Word2Vec(sentences_iterable, size=size, window=window,
                      alpha=alpha, min_count=min_count, workers=num_threads)


def glove_benchmark(sentences_iterable, window=5, size=100, alpha=0.05,
                    epochs=10, num_threads=1):
    """ Wrapper de los pasos para crear el modelo de Glove para poder
    realizar mediciones del rendimiento.
    """
    corpus_model = Corpus()
    corpus_model.fit(sentences_iterable, window=window)
    glove = Glove(no_components=size, learning_rate=alpha)
    glove.fit(corpus_model.matrix, epochs=epochs,
              no_threads=1, verbose=False)


def plot_results(mem_usage_glove, mem_usage_w2v, time_glove, time_w2v):
    # plot de memoria usada por ambos modelos
    plt.subplot(121)
    plt.plot(np.arange(len(mem_usage_w2v)) * 0.1, mem_usage_w2v,
             'b', label='word2vec')
    plt.plot(np.arange(len(mem_usage_glove)) * 0.1, mem_usage_glove,
             'r', label='glove')
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Memoria usada (mb)")
    plt.title("Memoria consumida por los dos modelos")
    plt.legend()

    # plot de tiempo que tardó cada modelo en entrenarse
    plt.subplot(122)
    xlabels = ["Word2Vec", "Glove"]
    x = [0, 1]
    # y = [time_w2v.average, time_glove.average]
    plt.bar([0], time_w2v.average)
    plt.bar([1], time_glove.average)
    plt.title("Tiempo de entramiento de ambos modelos")
    plt.xlabel("Modelo empleado")
    plt.ylabel("Tiempo (s)")
    plt.xticks(x, xlabels)

    plt.tight_layout()
    plt.show()

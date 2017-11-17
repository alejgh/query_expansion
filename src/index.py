#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Este script indexa la colección de tweets en elasticsearch

import json
import elasticsearch.helpers
from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch()
    filename = '2008-Feb-02-04-EN'
    filepath = '../data/' + filename + '.json'
    batch_amount = 10000
    current_count = 0
    total = 0

    with open(filepath, 'r') as json_file:
        tweets_batch = []
        for line in json_file:
            tweet = json.loads(line)
            current_count += 1
            total += 1

            # Tenemos que pasarle a la funcion bulk el tipo de operacion
            # utilizando el campo '_op_type'
            tweet['_op_type'] = 'index'
            tweet['_index'] = filename.lower()

            # Eliminamos el score de cada tweet ya que nos es irrelevante.
            try:
                del tweet['_score']
            except KeyError:
                pass

            if total % batch_amount == 0:
                print(str(total))

            if current_count <= batch_amount:
                tweets_batch.append(tweet)
            else:
                # indexamos los tweets acumulados en esta tanda
                # y volvemos a empezar
                elasticsearch.helpers.bulk(es, tweets_batch)
                current_count = 0
                tweets_batch.clear()


if __name__ == '__main__':
    main()

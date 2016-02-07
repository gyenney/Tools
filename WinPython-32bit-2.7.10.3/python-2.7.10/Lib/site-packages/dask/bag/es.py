from elasticsearch import Elasticsearch
from dask.bag.core import Bag, tokens
from math import ceil


def get_results(es, kwargs):
    results = es.search(**kwargs)
    return [r['_source'] for r in results['hits']['hits']]


def from_elasticsearch(host, index, query, port=9200, pagination=100):
    """ Create Bag from Elasticsearch Query

    >>> b = from_elasticsearch(host='hostname', index='reddit',
    ...                        query={"match": {'body':'Python'}})
    """
    es = Elasticsearch([{'host': host, 'port': port}])
    count = es.count(index=index, body={'query': query})['count']

    npartitions = int(ceil(count / pagination))
    name = 'elasticsearch' + next(tokens)

    dsk = dict()
    for i in range(npartitions):
        kwargs = {'index': index, 'body': {'query': query,
                                           'from': pagination*i,
                                           'size': pagination}}
        dsk[(name, i)] = (get_results, es, kwargs)

    return Bag(dsk, name, npartitions)

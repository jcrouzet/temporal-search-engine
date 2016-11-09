from elasticsearch import Elasticsearch
import numpy as np

def query_hist(query):
    """
    """
    es = Elasticsearch()
    res = es.search(index="spliine",
                doc_type="article",
                body='{"query":{"match":{"article":"'+ query +'"}},"size":0,"aggregations":{"date_hist":{"date_histogram":{"field":"date_art","interval":"day", "format" : "yyyy-MM-dd"}}}}')

    print(query + " : %d articles corerespondants" % res_dimanche['hits']['total'])

    res_to_hist= {}
    results = res['aggregations']['date_hist']['buckets']
    counts = []
    dates = []

    for doc in results:
        #print("%s) %s" % (doc['key_as_string'], doc['doc_count']))
        counts.append(doc['doc_count'])
        dates.append(doc['key_as_string'].encode('ascii','ignore'))
        res_to_hist[doc['key_as_string'].encode('ascii','ignore')] = doc['doc_count']
        
    return((counts, dates))

def query_articles(query, start, end):
    """
    """
    es = Elasticsearch()
    res = es.search(index="spliine",
                doc_type="article",
                body='{"query":{"bool":{"must":{"range":{"date_art":{"gte":"'+ date1 +'","lte":"'+ date2 +'"}}},"filter":{"query_string":{"query":"'+ query +'","default_operator":"AND"}}}},"size":5}')
    return res

# ### En utilisant `requests`

## make sure ES is up and running
#import requests
#res = requests.get('http://localhost:9200')
#print(res.content)

##connect to our cluster
#from elasticsearch import Elasticsearch
#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#es.get(index='spliine', doc_type='article', id='AVhD3kpOEPyczRd2_-gr')


# ### En utilisant `elasticsearch-py`

from elasticsearch import Elasticsearch
import numpy as np

es = Elasticsearch()

def requete(query):
    res = es.search(index="spliine",
                doc_type="article",
                body='{"query":{"match":{"article":"'+ query +'"}},"size":0,"aggregations":{"date_hist":{"date_histogram":{"field":"date_art","interval":"day", "format" : "yyyy-MM-dd"}}}}')
    return res


# ==============================================================================
# Recheche 1 : mérovingiens

res_merovingiens = requete("mérovingiens")
total1 = res_merovingiens['hits']['total']
print("'mérovingiens' : %d articles correspondants" % total1)

res_to_hist1= {}
results1 = res_merovingiens['aggregations']['date_hist']['buckets']
counts1 = []
dates1 = []

for doc in results1:
    #print("%s) %s" % (doc['key_as_string'], doc['doc_count']))
    counts1.append(doc['doc_count'])
    dates1.append(doc['key_as_string'].encode('ascii','ignore'))
    res_to_hist1[doc['key_as_string'].encode('ascii','ignore')] = doc['doc_count']



# ==============================================================================
# Recheche 2 : dimanche

res_dimanche = requete("dimanche")

print("'dimanche' : %d articles corerespondants" % res_dimanche['hits']['total'])

res_to_hist2= {}
results2 = res_dimanche['aggregations']['date_hist']['buckets']
counts2 = []
dates2 = []

for doc in results2:
    #print("%s) %s" % (doc['key_as_string'], doc['doc_count']))
    counts2.append(doc['doc_count'])
    dates2.append(doc['key_as_string'].encode('ascii','ignore'))
    res_to_hist2[doc['key_as_string'].encode('ascii','ignore')] = doc['doc_count']


# ==============================================================================
# Recheche 3 : séisme

res_seisme = requete("séisme")

total3 = res_seisme['hits']['total']
print("'séisme' : %d articles corerespondants" % total3)


res_to_hist3= {}
results3 = res_seisme['aggregations']['date_hist']['buckets']
counts3 = []
dates3 = []

for doc in results3:
    #print("%s) %s" % (doc['key_as_string'], doc['doc_count']))
    counts3.append(doc['doc_count'])
    dates3.append(doc['key_as_string'].encode('ascii','ignore'))
    res_to_hist3[doc['key_as_string'].encode('ascii','ignore')] = doc['doc_count']


# ==============================================================================
# Sauvegarde des résultats

counts1_save = np.asarray(counts1)
counts2_save = np.asarray(counts2)
counts3_save = np.asarray(counts3)

np.savetxt("recherche_merovingiens.txt", counts1_save, fmt='%d')
np.savetxt("recherche_dimanche.txt", counts2_save, fmt='%d')
np.savetxt("recherche_seisme.txt", counts3_save, fmt='%d')


# ### Récupération des intervalles

import json

# ==============================================================================
# Récupération des intervalles d'évènements
# On utilise le tableau d'intervalles déjà calculé pour la recherche "séisme"

intervalles = np.array([[162, 166], [351, 357], [404, 410], [476, 477], [738, 754], [755, 761]])

def requete_interv(date1, date2, query):
    res = es.search(index="spliine",
                doc_type="article",
                body='{"query":{"bool":{"must":{"range":{"date_art":{"gte":"'+ date1 +'","lte":"'+ date2 +'"}}},"filter":{"query_string":{"query":"'+ query +'","default_operator":"AND"}}}},"size":5}')
    return res


# ==============================================================================
# Création du disctionnaire à afficher

sortie = { "events": [] }

for interv in intervalles:

    d_start = dates3[interv[0]]
    d_end = dates3[interv[1]]

    # Ajout de l'intervalle
    tmp = {}
    tmp["start"] = d_start
    tmp["end"] = d_end
    tmp["title"] =  d_start + " / " + d_end
    tmp["durationEvent"] = 'true'
    tmp["description"] = "Evenement entre " + d_start + " et " + d_end
    tmp["link"] = ""

    sortie['events'].append(tmp)

    # Ajout de l'article marquant de l'intervalle
    tmp = {}
    res_req = requete_interv(d_start, d_end, "séisme")

    tmp["start"] = res_req["hits"]["hits"][0]["_source"]["date_art"].encode('ascii','ignore')
    tmp["title"] = res_req["hits"]["hits"][0]["_source"]["id_art"].encode('ascii','ignore')
    tmp["description"] = "Score de : " + str(res_req["hits"]["hits"][0]["_score"])
    tmp["link"] = "http://localhost:5601/app/kibana#/doc/spliine/spliine/article?id=" + res_req["hits"]["hits"][0]["_source"]["id_art"].encode('ascii','ignore')

    sortie['events'].append(tmp)

# Sauvegarde du `js`
f = open('results.js', 'w')
json.dump(sortie,f,indent=1)
print("Done !")

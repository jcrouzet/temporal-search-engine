import numpy as np

from query import *

def timeline_json(events, dates):
    """
    """
    tl_json = { "events": [] }

    for event in events:

        d_start = dates[event[0]]
        d_end = dates[event[1]]

        # Ajout de l'intervalle
        tmp = {}
        tmp["start"] = d_start
        tmp["end"] = d_end
        tmp["title"] =  d_start + " / " + d_end
        tmp["durationEvent"] = 'true'
        tmp["description"] = "Evenement entre " + d_start + " et " + d_end
        tmp["link"] = ""

        tl_json['events'].append(tmp)

        # Ajout de l'article marquant de l'intervalle
        tmp = {}
        res_req = query_articles("séisme", d_start, d_end)

        tmp["start"] = res_req["hits"]["hits"][0]["_source"]["date_art"].encode('ascii','ignore')
        tmp["title"] = res_req["hits"]["hits"][0]["_source"]["id_art"].encode('ascii','ignore')
        tmp["description"] = "Score de : " + str(res_req["hits"]["hits"][0]["_score"])
        tmp["link"] = "http://localhost:5601/app/kibana#/doc/spliine/spliine/article?id=" + res_req["hits"]["hits"][0]["_source"]["id_art"].encode('ascii','ignore')

        tl_json['events'].append(tmp)

    # Sauvegarde du `js`
    f = open('results.json', 'w')
    json.dump(tl_json, f, indent=1)

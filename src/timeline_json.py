import numpy as np
import json

from query import *

def timeline_json(events, dates, query):
    """
    """
    tl_json = { "events": [] }
    num = 0

    for event in events:

        num = num+1
        d_start = dates[event[0]-1]
        d_end = dates[event[1]-1]

        # Ajout de l'article marquant de l'intervalle
        tmp = {}
        res_req = query_articles(query, d_start, d_end)

        tmp["start"] = res_req["hits"]["hits"][0]["_source"]["date_art"]
        tmp["title"] = num
        tmp["description"] = "Score de : " + str(res_req["hits"]["hits"][0]["_score"]) + "\n" + res_req["hits"]["hits"][0]["_source"]["id_art"]
        tmp["link"] = "http://localhost:5601/app/kibana#/doc/spliine/spliine/article?id=" + res_req["hits"]["hits"][0]["_source"]["id_art"]

        tl_json['events'].append(tmp)

        # Ajout de l'intervalle
        tmp = {}
        tmp["start"] = d_start
        tmp["end"] = d_end
        tmp["title"] = ""
        tmp["durationEvent"] = 'true'
        tmp["description"] = "Evenement entre " + d_start + " et " + d_end
        tmp["link"] = ""

        tl_json['events'].append(tmp)

    return json.dumps(tl_json)

    # Sauvegarde du `js`
    # f = open('results.json', 'w')
    # json.dump(tl_json, f, indent=1)

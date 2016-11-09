# Installation de `elasticsearch-py`

On peut faire appel à Elasticsearch depuis Python grâce à la librairie
`elasticsearch-py`. Elle est facilement installable à l'aide de `pip`. La
commande suivante va permettre l'installation de la librairie

~~~
pip install elasticsearch
~~~

# Configuration de la requête générale

On cherche dans un premier temps à générer un histogramme qui rend le nombre
d'article s correspondants à une requête donnée par jour.

Pour cela on utilise les `requêtes` et les `aggregations` disponibles sous
Elasticsearch.

~~~
{
    query: {
        match_all: {}
    },
    "aggregations": {
        "some_date_facet": {
            "date_histogram": {
                "field": "date_art",
                "interval": "day"
            }
        }
    }
}
~~~

// =============================================================================
// à terminer

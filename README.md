# temporal-search-engine

Here is our Python-based project for the M2 AIC - Recherche et Extraction
d'Information courses.

Based on an Elasticsearch instance, the engine is made to run temporal query on
a database composed of french newpapers from 2012 to 2015. Those queries give
answers as a timeline, where results are spread according to the event they
refer to.

For example, if we search "séisme" (hearthquake), we should find not only the
most relevant results according to a similarity with the query "séisme", but
we need to obtain results corresponding to the several event according to unique
hearthquakes that were dealt with in the newspapers.

The different mesures of peak detection, and a longer explanation of the project
is available with the reports.

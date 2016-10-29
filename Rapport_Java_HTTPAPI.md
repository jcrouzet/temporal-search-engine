### Faire des requêtes à Elasticsearch via Java

Elasticsearch utilise une API HTTP qui permet grâce notamment à des GET (mais
pas que) d'intéragir avec les documents indexés, mais aussi de manière plus
méta avec la santé des clusters, des nodes, etc.

Cette API est disponible sur le port 9200 du serveur où Elasticsearch est
installé (dans notre cas, `localhost:9200/`).

Pour faire des requêtes dans Java, on peut utiliser la librairie [Apache
HTTPComponents](https://hc.apache.org/ "Apache
HTTPComponents").

# Classe API pour communiquer avec l'API Elasticsearch

Disponible dans l'archive avec ce rapport.

# Installation de la librairie (pour les n00bs)

Dans la partie [Download](https://hc.apache.org/downloads.cgi "Dowload") du
même site, télécharger le `.zip` ou le `.tar.gz` correspondant à la librairie
HTTPClient, et extraire l'archive.

Ceci fait, dans Eclipse, aller dans `Project > Properties > Java Build Path`
et sélectionner l'option `Add external JARs...`, puis ajouter les `.jar` de
l'archive extraite.

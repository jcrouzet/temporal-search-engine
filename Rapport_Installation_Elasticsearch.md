### Utilisation de Elasticsearch et Logstash pour indexer les articles

Ici seront détaillées les différentes étapes pour l'installation de Logstash et
Elasticsearch et leurs dépendances, et les moyens mis en oeuvre pour indexer les
articles.

# Installations

## Java

Pour Elasticsearch, une version de Java plus récente que la 8 est nécessaire.

Prenons la dernière en date, [disponible sur le site d'oracle](https://java.com/en/download/linux_manual.jsp "Lien vers la page de téléchargement de Java"). Pour le cas d'un Linux le permettant, on prendra le
fichier `.tar.gz`.

Après avoir placé l'archive dans le fichier où l'on veut installer Java, par
exemple `/usr/java`, on l'extrait et on la supprime :

~~~
cd /usr/java
sudo tar -zxvf jre-8u111-linux-x64.tar.gz
sudo rm jre-8u111-linux-x64.tar.gz
~~~

On ajoute Java à la variable d'environnement `PATH` :

~~~
PATH=/usr/java/jre1.8.0_111/bin:$PATH
export PATH
~~~

On vérifie que tout fonctionne avec un :

~~~
java -version
~~~

Ceci fait, on se lance dans l'installation d'Elasticsearch.

## Elasticsearch 5.0

Elasticsearch est un moteur d'indexation libre, basé sur Java et la bibliothèque
Apache Lucene. Les requêtes à Elasticsearch se font par une HTTP API qui nous
permettra d'y accéder depuis n'importe quel instance de Java.

### Installation

On va installer Elasticsearch dans le dossier elasticsearch de mon home, en
utilisant le `.deb`, [disponible sur le site officiel d'elastic](https://www.elastic.co/guide/en/elasticsearch/reference/5.0/deb.html
   "Site officiel d'Elastic, page d'installation du .deb").

Tout d'abord, on installe la clef signée.

~~~
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
~~~

On installe ensuite le paquet `apt-transport-https` qui nous sera utile, avant
d'enregistrer la définition du dépôt.

~~~
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/5.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-5.x.list
~~~

Reste à installer :

~~~
sudo apt-get update && sudo apt-get install elasticsearch
~~~

Différents problèmes peuvent ensuite se poser : la plupart pour des questions
de droits.

~~~
sudo chown elasticsearch:elasticsearch -R /etc/elasticsearch
~~~

### Configuration

Une fois installé, il faut maintenant configurer le fichier
`/etc/elasticsearch/elasticsearch.yml` en le remplaçant par :

~~~
# ================ elasticsearch.yml - SPLiiNe version =========================

cluster.name: SPLiiNe
node.name: main_node

path:
    data: /var/lib/elasticsearch
    logs: /var/log/elasticsearch

network.host: localhost
~~~

### Lancement

Pour lancer Elasticsearch comme un service, sous Ubuntu, il faut lancer un :

~~~
sudo service elasticsearch start
~~~

On stop le processus, ou on en obtient le status, simplement en remplaçant
`start` par respectivement `stop` ou `status` dans la commande précédente.

Installons à présent Logstash.

## Logstash 5.0

Logstash est un outil qui permet de "formater" les fichiers que l'on va indexer. Il faut

### Installation

Il nous suffit de lancer un :

~~~
sudo apt-get update && sudo apt-get install logstash
~~~

Pour ajouter logstash aux processus de démarrage du serveur (ce que l'on ne veut
pas ici), on ferait :

~~~
sudo update-rc.d logstash defaults 95 10
~~~

On donne finalement les droits de propriété à Logstash sur le fichier de
configuration `/etc/logstash` :

~~~
sudo chown logstash:logstash -R /etc/logstash/
sudo chown logstash:logstash -R /var/log/logstash/
~~~

### Configuration [Pas terminé]

Logstash utilise 3 étapes de traitement pour message arrivant : la
première consistant au traitement des entrées (`input`), la seconde
traitant le parsing (`filter`) et la dernière traitant la sortie
(`output`).

- Pour le premier plugin, nous avons dû récupérer les articles sur notre
serveur de façon à les indexer ensuite. Ainsi il faut indexer des fichiers
entiers. Le plugin `file` n'est pas fait pour indexer des fichiers entiers,
néanmoins, on peut tricher un peu en mettant l'option `start_position =>
beginning` et `sincedb_path => "/dev/null"`. D'où le plugin :

~~~
# ============================ 01_input.conf ===================================
input {
  file {
    path => "/media/nikita/NikitaDD/text/*/*/*/*.txt"
    start_position => beginning
    sincedb_path => "/dev/null"
  }
}
~~~

- Pour le second plugin, notre champ `message` sera constitué du corps épuré de
l'article, et ne nécessite donc à priori aucun traitement. Il faudra cependant
ajouter le champ correspondant à la date de parution de l'article, et celle-ci
est notamment récupérable, tout comme l'id de l'article, dans le titre du
fichier. On utilise donc un plugin de parsing `grok` d'expression régulières.

Pour définir les expressions régulières proprement, je crée un fichier
`grok_patterns.conf` dans le répertoire `/etc/logstash` pour définir ce que l'on
devrait utiliser pour matcher les titres.

~~~
# ========================== grok_patterns.conf ================================
ANNEE_ARTICLE (?>\d\d\d\d)
MOIS_ARTICLE (?>\d\d)
JOUR_ARTICLE (?>\d\d)
~~~

~~~
# ============================ 11_filter.conf ==================================
filter {
  grok {
    patterns_dir => ["/etc/logstash/grok_patterns.conf"]
    match => {
      "path" => "%{GREEDYDATA}/%{ANNEE_ARTICLE:annee}%{MOIS_ARTICLE:mois}%{JOUR_ARTICLE}_%{GREEDYDATA:id}.txt"
    }
    add_field => {
      "date" => "%{annee}-%{mois}-%{jour}"
    }
    remove_field => ["annee","mois","jour"]
  }
}
~~~

- Pour le dernier plugin, il suffit de spécifier que l'on souhaite indexer les
articles dans Elasticsearch, et plus précisément dans l'instance locale.

~~~
# ============================ 21_output.conf ==================================
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "spliine-%{+YYYY.MM.dd}"
  }
}
~~~

S'il y a un problème, ce peut être une question de droits, il suffit alors de
donner la propriété des fichiers à Logstash par un `chown`.

### Lancement

Pour lancer Logstash comme un service, sous Ubuntu, il faut lancer un :

~~~
sudo service logstash start
~~~

On stop le processus, ou on en obtient le status, simplement en remplaçant
`start` par respectivement `stop` ou `status` dans la commande précédente.

Pour pouvoir visualiser nos données et voir notamment les pics de données et
leur comportement, nous utilisons Kibana.

## Kibana 5.0

### Installation

Il nous suffit de lancer un :

~~~
sudo apt-get update && sudo apt-get install kibana
~~~

Pour ajouter Kibana aux processus de démarrage du serveur (ce que l'on ne veut
pas ici), on ferait :

~~~
sudo update-rc.d logstash defaults 95 10
~~~

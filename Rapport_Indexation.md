### Indexation des articles

Une fois qu'elasticsearch, logstash sont installés, vous pouvez indexer la base de données (le dossier `text` de `ProjetREI`).

# Indexation

## Modification du script

Pensez à modifier l'emplacement du dossier `text` et celui du fichier que logstash observe.

## Demmarrer l'indexation

Pour compiler et executer le script de conversion :

~~~
javac indexation/CSVConversion.java
java CSVConversion
~~~

## Verifier que logstash a tout indexer

Dès le début de l'exécution du script, la commande suivante vous permet d'observer l'index (`spliine` si vous avez les mêmes fichiers de configuration que nous).

~~~
curl -X GET 'localhost:9200/_cat/indices?pretty=true'
~~~

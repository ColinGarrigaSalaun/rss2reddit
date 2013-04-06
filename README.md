# Propos

`rss2reddit` permet l'alimentation d'un sous-reddit à partir d'un flux ou d'une liste de flux rss.


# Installation

    $ pip install -r requirements.txt


# Utilisation

## Triviale

Pour soumettre sur le sous-reddit `agilefr` les billets accessibles via le flux `http://example.com/feed.rss`, pour l'utilisateur Reddit `agilefrbot` :

    $ python rss2reddit.py --reddit agilefr --user agilefrbot --password **** --url http://example.com/feed.rss

## Plus sage

Pour ne soumettre que les billets publiés sur les deux derniers jours :

    $ python rss2reddit.py --reddit agilefr --user agilefrbot --password **** --url http://example.com/feed.rss --days 2

## Plus pratique

Pour récupérer une liste de flux RSS d'un fichier :

    $ python rss2reddit.py --reddit agilefr --user agilefrbot --password **** --url-file agilefr.txt --days=1


# Tests

Pour exécuter les tests :

    $ nosetests


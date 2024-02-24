# Librairie requests

Librairie permettant de récupérer les données autorisées par différents sites @

Projet de récupération de données sur les sites suivants :

- https://app.dvf.etalab.gouv.fr/ : [une API est actuellement prévue](https://app.dvf.etalab.gouv.fr/faq.html#question_api) (date 10/01/24)

Il est possible de limiter le nombre de requêtes API selon une certaine durée d'intervalle avec la librairie ratelimit.

Deux paramètres :

> - calls : nombre de requêtes
> - period : fenêtre de temps(s)

Dans l'exemple, calls=15 et period=900 nous limitent à 15 appels d'API toutes les 15 minutes

![](assets/20240224_093325_Sans_titre.png)

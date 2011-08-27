.. _intro-tipmac:

Démon Tipmac
============

Il a été observé qu'un des éléments les plus difficiles à remplir lors
de l'inscription était l'adresse MAC, et en particulier pour les 1ère
années. À partir de la mise en place de Maiznet.fr, il a été décidé de
créer une application spécialisée dans la récupération d'adresse MAC,
pour pouvoir pré-remplir le champ sur le formulaire.

Petits rappels théoriques : pour obtenir l'adresse MAC d'une machine, il
faut se trouver sur le même réseau physique. Or, Tera -- notre serveur
web -- se trouve dans une DMZ à part du réseau interne. C'est pourquoi
il a fallu coder un démon qui tourne sur Batman et qui permette à Tera
d'obtenir une correspondance IP/MAC.

Côté serveur
~~~~~~~~~~~~

Le serveur est contenu dans :py:mod:`maiznet.tools.tipmac.tipmac`. On
utilise :py:mod:`maiznet.tools.tipmac.daemon` pour lancer le serveur en
tant que démon. Pour la documentation complète de la configuration côté
serveur, se référer à `wikimin
<http://wikimin.maiznet.fr/doku.php?id=projets:sitewebdoc:iptomac>`_.

Pour fonctionner le serveur a besoin de :py:mod:`IPy` ainsi que de
:py:mod:`scapy`.

.. automodule:: maiznet.tools.tipmac.tipmac
    :members:

Côté client
~~~~~~~~~~~

La fonction :py:mod:`maiznet.register.tipmac.ip_to_mac` permet de
retourner la correspondance IP/MAC, et elle est appellée à divers
endroits du code qui initialisent le formulaire
d'inscription/modification d'utilisateur.

Cette fonction nécessite :py:mod:`IPy` pour fonctionner.

.. automodule:: maiznet.register.tipmac
    :members:

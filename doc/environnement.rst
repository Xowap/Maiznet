Mise en place d'un environnement de test
========================================

Cet article détaille la procédure précise permettant de créer un environnement de test identique au site d'origine. Si les résultats sont probants, alors on passe en production.

Petit rappel : les fichiers du site ont des dépôts s sur `GitHub <http://github.com/>`_. Pour récupérer ces fichiers et en créer une copie, on commence par définir une racine

.. code-block:: bash

 sudo mkdir /var/wsgi/maiznet-TEST

Dans ce nouveau dossier, on va chercher une copie de la production

.. code-block:: bash

 sudo git clone https://github.com/EquiNux/Maiznet.git /var/wsgi/maiznet-TEST/

Ensuite, on indique à Apache qu'on veut un deuxième site

.. code-block:: bash

 cp /etc/apache2/sites-available/fr.maiznet /etc/apache2/sites-available/fr.maiznet-TEST

le contenu de ce nouveau fichier de conf doit être légèrement modifié  par rapport au premier :

.. code-block:: bash

 [...]
 ServerName maiznet-TEST.fr
 [...]
 DocumentRoot /var/www/maiznet-TEST
 Alias /maiznet-media /var/wsgi/maiznet-TEST/maiznet/media
 Alias /maiznet-doc /var/wsgi/maiznet-TEST/maiznet/doc/_build/html
 [...]

Le site est disponible. Cependant il faut l'indiquer à la machine cliente, car maiznet-TEST.fr n'est pas enregistré au niveau DNS. Cela passe par rajouter la ligne

.. code-block:: bash

 192.168.0.10 maiznet-TEST.fr

dans un fichier. Sous windows il s'agit de :py:mod: c:\windows\system32\drivers\etc\hosts, et sous Linux /etc/hosts.

Enfin, on peut lancer une synchronisation avec la base de données pour y remplacer au moins les fixtures (cad les constantes) : dans maiznet-TEST, faire un

.. code-block:: bash

 ./manage.py syncdb

Voilà, l'environnement de test est en place. On peut faire ce qu'on veut au nouveau site, ça n'affectera pas la production.

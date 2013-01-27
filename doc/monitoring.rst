Application monitoring
======================

Cette section contient la configuration d'une part la configuration du smokeping, en donne une brève description et d'autre part donne quelques commandes de base.

Configuration
-------------

La configuration est rértie dans 8 fichiers dans /etc/smokeping/config.d
Seuls les fichiers Database, General, Presentation, Probes et Targets ont été  modifiés, et voici les lignes modifiées/rajoutés :

Database
~~~~~~~~

.. code-block:: bash

 [...]
 step	= 60
 pings	= 10
 [...]

On fait 10 pings toutes les minutes. 

General
~~~~~~~

.. code-block:: bash

 [...]
 owner	 = Maiznet
 contact = maiznet-monitoring@googlegroups.com
 [...]

Pas de grand intérêt à part afficher ces références sur la page du smokeping.

Presentation
~~~~~~~~~~~~

.. code-block:: bash

 [...]
 "Dernière heure"	1h
 "Dans la journée"	1d
 "Dans la semaine"	7d
 "Dans le mois"		30d
 "Dans l'année"		365d
 "10 dernières années"	3650d
 [...]

C'est ici qu'on choisit les amplitudes des différents graphes.

Probes
~~~~~~

.. code-block:: bash

 [...]
 ++ FPingDefault

 ++ FPingSDSL

 sourceaddress = 192.168.0.10

 ++ FPingADSL1

 sourceaddress = 192.168.0.11

 ++ FPingADSL2

 sourceaddress = 192.168.0.12

Element assez important de la conf. C'est là qu'on définit des manières dont serons, nt réalisés les pings, ou plus précisément les types de "sondages".

Targets
~~~~~~~

.. code-block:: bash

 [...]
 title = Smokeping

 + Lignes

 menu = Lignes
 title = Lignes

 ++ adsl1

 menu = ADSL1
 title = ping vers google.com via ADSL 1
 probe = FPingADSL1
 host = www.google.com

 ++ adsl2

 menu = ADSL 2
 title = ping vers google.com via ADSL 2
 probe = FPingADSL2
 host = www.google.com

 ++ sdsl

 menu = SDSL
 title = ping vers google.com via SDSL
 probe = FPingSDSL
 host = www.google.com

La syntaxe est assez simple.

A noter que le nombre de "+" hiérarchise les menus dans l'interface utilisateur.

Administration
--------------

Quelques commandes de base :

Arrêt

.. code-block:: bash

 sudo /etc/init.d/smokeping stop

Reprise/lancement

.. code-block:: bash

 sudo /etc/init.d/smokeping start

Relance (doit être fait pour appliquer une nouvelle connf)

.. code-block:: bash

 sudo /etc/init.d/smokeping restart

La même chose sans interruption du service

.. code-block:: bash

 sudo /etc/init.d/smokeping reload

Cependant, il faut il temps relativement long avant que le restart/reload soit pris en compte (~5 min). Pour forcer le tout rapidement (c'est un peu brutal mais instantané)

.. code-block:: bash

 sudo /etc/init.d/apache2 restart


Les valeurs exploitées dans les graphes sont stockées dans :py:mod:`/var/lib/smokeping/CHEMIN/FICHIER.rrd`. Supprimer ce fichier réinitialisera le graphe correspondant. Cela peut être utile si l'on veut modifier la fréquence des pings.

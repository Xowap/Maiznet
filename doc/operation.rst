Opération du site
=================

Le but de cette section est de décrire les différents à suivre pour
pouvoir opérer le site.

Installation
------------

Nous détaillerons ici la procédure d'installation du site sur une
Debian, que ce soit pour une plateforme de production ou pour effectuer
du développement.

Dépendances
~~~~~~~~~~~

Pour fonctionner, différents modules sont nécessaires :

  - :py:mod:`django` qui est le moteur du site. La version actuelle du
    site s'attend à un Django 1.2.
  - :py:mod:`IPy` est utilisé pour diverses opération de calcul sur les
    adresses IP.
  - :py:mod:`matplotlib` pour tracer les graphes du monitoring.
  - :py:mod:`simplejson` sert lors de la communication avec du
    javascript.
  - :py:mod:`modeltranslation` s'occuper de traduire certains modèles.
  - :py:mod:`piwik` permet l'intégration à Piwik, pour les stats du
    site.
  - :py:mod:`jabber` est utilisé pour monitorer le serveur Jabber.
  - :py:mod:`sphinx` est utilisé pour gérer la documentation.

De plus, *gettext* et nécessaire pour les traductions.

Sous debian,

.. code-block:: bash

 aptitude install python-django python-ipy python-matplotlib gettext python-pip python-simplejson

De plus il faut installer modeltranslation à la main. Pour cela, le
télécharger sur son site
(http://code.google.com/p/django-modeltranslation/), le décompresser,
aller dans le répertoire ainsi créé, puis en tant que root

.. code-block:: bash

 ./setup.py install

Et enfin, l'installation de :py:mod:`piwik` se fait avec Pip :

.. code-block:: bash

 pip install piwik

Copie du code
~~~~~~~~~~~~~

Une fois que toutes les dépendances sont présentes, il faut installer le
site en lui même. Le code est géré par Git, et hébergé sur GitHub. La
page GitHub est à l'adresse https://github.com/Xowap/Maiznet. 

Dans le cas où on voudrait installer un site en production, le mieux est
de prendre la branche de référence. On la récupère comme suit :

.. code-block:: bash

 git clone https://github.com/Xowap/Maiznet.git maiznet

Cependant, pour faire du développement, chaque développeur est invité à
effectuer un fork de la branche principale, et de faire ses
modifications à part. Les modifications seront ensuite réintégrées au
site principal par le mainteneur.

Pour déboguer ou développer une nouvelle partie du site, on peut égalemment être ammené à passer par un `environnement de test <http://maiznet.fr/maiznet-doc/environnement.html>`_.

Configuration d'Apache
~~~~~~~~~~~~~~~~~~~~~~

Django 1.2 n'est pas prévu pour servir tous les fichiers statiques par
lui même, et aura besoin de l'aide d'un serveur web pour cela. De très
nombreuses possibilités de configuration existent, mais dans le cas
présent on utilisera un Apache par souci de simplicité.

Il y a 2 choses à servir pour Django : les medias du site, et les medias
de l'interface d'administration. Voilà ce qu'on peut trouver dans la
configuration de Tera (fichier
:file:`/etc/apache2/sites-enabled/fr.maiznet`)

.. code-block:: apache

         Alias /maiznet-media /var/wsgi/maiznet/media
         <Directory "/home/remy/Dev/maiznet/media">
                 Options Indexes FollowSymLinks MultiViews
                 Order allow,deny
                 Allow from all
         </Directory>
 
         Alias /django-admin-media /usr/share/pyshared/django/contrib/admin/media
         <Directory "/usr/share/pyshared/django/contrib/admin/media">
                 Options Indexes FollowSymLinks MultiViews
                 Order allow,deny
                 Allow from all
         </Directory>

Le premier bloc sert à définir un alias pour les medias spécifique au
site, donc attention au chemin utilisé. Le 2ème peut être copié/collé
tel quel sur n'importe quelle Debian.

Le résultat de l'opération c'est que les media sont disponibles (par
exemple) à l'adresse http://maiznet.fr/maiznet-media/.

Ensuite, il faut servir le Django en lui même. Si c'est un serveur de
production on utilisera WSGI. Dans la configuration d'Apache

.. code-block:: apache

 WSGIScriptAlias / /var/wsgi/maiznet/django.wsgi

Et le fichier :file:`/var/wsgi/maiznet/django.wsgi` lui même :

.. code-block:: python

 import os
 import sys
 
 sys.path.append('/var/wsgi/maiznet')
 sys.path.append('/var/wsgi')
 
 os.environ["DJANGO_SETTINGS_MODULE"] = "maiznet.settings"
 
 import django.core.handlers.wsgi
 application = django.core.handlers.wsgi.WSGIHandler()

Dans le cas d'un serveur de dev, on utilisera le serveur intégré au
:file:`manage.py`, comme expliqué dans le `tutoriel django
<https://docs.djangoproject.com/en/1.2/intro/tutorial01/>`_.

Configuration du site
~~~~~~~~~~~~~~~~~~~~~

Une fois qu'Apache est configuré, il reste encore à configurer le site
lui même pour qu'il puisse fonctionner. La configuration est répartie
sur 2 fichiers :

  - Le fichier :file:`settings.py`, qui contient la configuration qui ne
    doit pas changer entre 2 installation du site (les langues gérées,
    les applications activées, etc).
  - Le fichier :file:`local_settings.py`, avec toutes les valeurs
    susceptibles d'être modifées entre deux installations.

Comme le fichier :file:`local_settings.py` est dépendant de
l'installation, il n'est pas possible de le versionner dans Git. Pour
compenser cela, il existe un fichier :file:`local_settings.py-dist` qui
est en fait un modèle pour :file:`local_settings.py`.

La première étape de configuration consiste donc à copier
:file:`local_settings.py-dist` en :file:`local_settings.py`, puis de
mettre à jour les valeurs de ce dernier. En particulier, penser à
changer la valeur de DEBUG en fonction de si c'est un site de production
ou non. Il faudra aussi penser à configurer la base de données (et donc
éventuellement en créer une, ou utiliser sqlite pour le développement).

Finitions diverses
~~~~~~~~~~~~~~~~~~

Arrivé à ce stade, quelques éléments restent encore à configurer.

  - Penser à mettre en place :ref:`tipmac <intro-tipmac>` si nécessaire.
  - En prod, s'assurer que le `script de mise à jour du DHCP
    <http://wikimin.maiznet.fr/doku.php?id=projets:dhcp>`_ fonctionne
    bien avec la bonne URL.
  - :ref:`Compiler les traductions <compil-trad>`.
  - Faire un *runserver* si c'est une plateforme de dev.
  - S'assurer que les chambres sont correctes.
  - Dans l'interface d'administration, configurer correctement le nom du
    site.
  - Et peut être même :ref:`générer la documentation <gen-doc>`.

Intégration à Piwik
~~~~~~~~~~~~~~~~~~~

Ceci nécessite qu'un Piwik soit installé. Une fois que cela est fait, et
qu'un site maiznet.fr a été créé dans Piwik, il faut mettre à jour
:file:`local_settings.py` :

  - **PIWIK_TOKEN** est la valeur donnée par Piwik dans la section
    "API".
  - **PIWIK_URL** correspond à l'URL à laquelle le Piwik est installé.

Ces opérations étant effectuées, il faut aller dans l'interface
d'administration de Maiznet.fr pour créer le site Piwik.

.. _site-update:

Mise à jour
-----------

La mise à jour est assez simple. Sur un serveur de production, il suffit
de se rendre dans le dossier contenant les sources, et d'utiliser git

.. code-block:: bash

 git pull origin master

Il faut cependant faire bien attention à certaines modification :

  - Les mises à jour de schema de base de données ne sont pas
    répercutées automatiquement, il faut les faire à la main.
  - Si :file:`local_settings.py-dist` a été modifié, il faut répercuter
    les changements dans :file:`local_settings.py`
  - Un changement des traductions demande une :ref:`re-compilation
    des traductions <compil-trad>`.

Traduction
----------

La traduction est gérée par Django. Inutile de remplacer la
`documentation officielle
<https://docs.djangoproject.com/en/1.2/topics/i18n/>`_, mais un
aide-mémoire ne fera pas de mal.

Traduction des messages
~~~~~~~~~~~~~~~~~~~~~~~

On suppose que les chaînes sont correctement formatées pour être
traduites, comme l'explique `la documentation
<https://docs.djangoproject.com/en/1.2/topics/i18n/internationalization/>`_.
Une fois que cela est fait, il faut générer les fichiers .po, qui
recencent les traductions dans les différents langages :

.. code-block:: bash

 ./manage.py makemessages -a

Les fichiers sont créés dans le répertoire :file:`locale`, par exemple
:file:`locale/fr/LC_MESSAGES/django.po`. Il faut éditer ces fichiers
avec un éditeur du type *poedit*.

Une fois la traduction effectuée, ne pas oublier de commiter la
traduction. Ensuite, c'est à la :ref:`mise à jour <site-update>` des
différentes copies que les traductions seront distribuées. À ce moment
là, il faudra compiler les traductions pour qu'elles soient prises en
compte.

.. _compil-trad:

Compilation des traductions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour des raisons d'optimisation, gettext n'utilise pas les fichiers .po
bruts, mais plutôt leur version compilée en .mo. Django gère l'opération
de compilation tout seul :

.. code-block:: bash

 ./manage.py compilemessages

Les changements de traduction ne sont pas pris en compte immédiatement,
et il faudra redémarrer le serveur web pour cela. En production :

.. code-block:: bash

 service apache2 restart

Documentation
-------------

Et oui, de la doc sur la doc :)

Donc, la documentation est gérée par `sphinx
<http://sphinx.pocoo.org/>`_. Il y a tout un tas d'explications sur
comment ça marche, RTFM.

.. _gen-doc:

Génération de la doc
~~~~~~~~~~~~~~~~~~~~

La documentation se trouve dans :file:`doc/`. Il faut se rendre dans ce
répertoire et faire :

.. code-block:: bash

 make html

Et là, la doc sera générée dans le répertoire :file:`doc/_build`.

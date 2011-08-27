Application *News*
==================

Les News sont affichées en page d'accueil du site. Elles servent à
informer les utilisateurs des nouveautés, pannes ou opérations de
maintenance.

Partie administrateur
~~~~~~~~~~~~~~~~~~~~~

La gestion des news se fait pas l'interface d'administration de Django.
Il y a trois catégories de news :

Les annonces sont notamment utilisées pour informer les utilisateurs des
nouveaux services qui se mettent en place. Elles peuvent éventuellement
avoir une date de fin.

Les news de catégorie "Maintenance" informent les utilisateurs des
services qui seront coupés à cause d'une opération effectuée par les
administrateurs. Elle a nécessairement une date de début et une date de
fin. Ces news sont systématiquement affichées au-dessus des autres news.

Les news de catégorie "Problème" sont utilisées pour notifier des pannes
qu'il peut y avoir. Il n'y a pas nécessairement de date de fin. Ces news
sont affichées entre les news de maintenance et les annonces.

Les news sont affichées 3 jours avant leur date de début, jusqu'à 2h
après leur date de fin (si elle est indiquée).

Code
----

Vues
~~~~

.. automodule:: maiznet.news.views
    :members:

Modèles
~~~~~~~

.. automodule:: maiznet.news.models
    :members:

Administration
~~~~~~~~~~~~~~

.. automodule:: maiznet.news.admin
    :members:


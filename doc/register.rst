Application *register*
======================

Comme expliqué en :ref:`introduction <intro-register>`, il est
nécessaire que les utilisateurs du réseau s'inscrivent pas le bais de
l'application register.

La partie utilisateur permet de définir diverses données personnelles,
et en particulier de donner ses adresses MAC.

Partie administrateur
---------------------

Gestion des utilisateurs
~~~~~~~~~~~~~~~~~~~~~~~~

La gestion des utilisateurs est celle de Django, rien de particulier à
signaler. Les pages d'édition des utilisateurs permettent entre autre
d'éditer les adresses MAC, le numéro de chambre, etc.

En ce qui concerne les administrateurs Maiznet, ils doivent être membre
du groupe "Maiznet", en plus d'être dans le groupe correspondant à leur
promotion, et doivent être coché en tant que "Statut équipe".

Groupes et promotions
~~~~~~~~~~~~~~~~~~~~~

L'interface d'administration permet à la fois d'éditer les groupes et
les promotions. Les promotions sont en fait inclues dans les groupes,
mais l'inverse n'est pas vrai :

  - Les promotions sont listées dans la liste des promos à
    l'inscription.
  - Les groupes n'étant pas des promotions quand à eux ne sont pas
    choisissables par les utilisateurs, mais on les utilises pour des
    raisons administratives, comme par exemple donner des droits à un
    groupe.

En outre, sur Jabber les contacts sont placé dans le roster par groupe,
et non pas par promotion uniquement. Cela permet par exemple la présence
de l'administration de Maiz dans le roster.

Chambres
~~~~~~~~

Pas grand chose à dire : il faut que l'ensemble des chambres soient
présentes. On ne peut avoir qu'un utilisateur par chambre, alors pour
les FA qui sont à plusieurs dans une salle, on créé plusieurs "chambres"
pour la même salle, d'où les "Cyclamen 1", "Cyclamen 2", etc...

Normalement, on ne touche pas aux chambres, et s'il y avait besoin de le
faire, c'est normalement l'administration de Maiz qui le fera.

Code
----

Vues
~~~~

.. automodule:: maiznet.register.views
    :members:
    :undoc-members:

Modèles
~~~~~~~

.. automodule:: maiznet.register.models
    :members:

Administration
~~~~~~~~~~~~~~

.. automodule:: maiznet.register.admin
    :members:

Décorateurs
~~~~~~~~~~~

.. automodule:: maiznet.register.decorators
    :members:

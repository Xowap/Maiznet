Application *pages*
===================

Administration
--------------

Il est nécessaire d'avoir des pages statiques de contenu, par exemple
pour les erreurs ou les différents guides. Ces pages peuvent être
créées dans l'interface d'administration, dans la rubrique associée. On
y rentre un titre, un contenu et un slug. Le slug est utilisé dans
l'URL. Une fois la page saisie, on peut y accéder à l'URL
http://maiznet.fr/pages/slug

Comme il est prévu qu'il y ait des étudiants internationaux à Maiz, ces
pages doivent également être écrites en anglais, d'où la présence d'un
champ français et d'un champ anglais pour le titre et le contenu.

Code
----

Gestion de la traduction
~~~~~~~~~~~~~~~~~~~~~~~~

La traduction est gérée automatiquement par l'application
`django-modeltranslation
<http://code.google.com/p/django-modeltranslation/>`_, qui doit être
installée sur le serveur faisant tourner le site.

.. autoclass:: maiznet.translation.PageTranslationOptions

Modèles
~~~~~~~

.. automodule:: maiznet.pages.models
    :members:

Vues
~~~~

.. automodule:: maiznet.pages.views
    :members:

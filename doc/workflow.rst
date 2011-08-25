Workflow utilisateur
====================

Le site centralise la majorité des outils de communication de Maiznet.
En outre, l'utilisateur est amené à le fréquenter régulièrement, pour
différentes raisons.

Erreurs
-------

Une des principales causes pour lesquelles un utilisateur peut être
envoyé sur le site est qu'il s'est passé une erreur. À l'heure
actuelle, il n'y a que deux erreurs possibles :

  - Quand un utilisateur n'est pas enregistré
  - Ou quand il tente d'utiliser le proxy

Les redirections sont gérées par Aquaman et ipfw, mais ça n'est pas
vraiment la question. Le site se contente d'afficher les raisons de
l'erreur, et la manière de la corriger.

.. _intro-register:

Enregistrement
--------------

Le cas des utilisateurs non enregistrés est un peu spécial. En effet,
pour des raisons juridiques et pratique, il nous faut identifer les
utilisateurs, en leur assignant une adresse IP spécifique. Comment faire
cela sans sombrer dans des démarches administratives sans fin ou devoir
faire confiance à l'utilisateur ? L'identifier par sa chambre.

Chaque chambre est donc associée à un « *ticket* », c'est à dire une
sorte de mot de passe qui permet à l'utilisateur de prouver qu'il occupe
bien la chambre.

Ce ticket est remis à l'utilisateur avec les clefs, sur un papier
imprimé par l'administration de Maiz. Ce papier contient non seulement
le numéro de ticket, mais aussi une documentation rapide pour avoir un
aperçu des services proposés par Maiz. Pour plus d'informations, s'en
référer à l'application :ref:`register <generation-tickets>`.

Pour faire valoir son ticket, l'utilisateur doit se rendre à l'URL
http://maiznet.fr/register, à laquelle on lui demandera de s'identifier
-- ou de s'inscrire si ce n'est pas encore fait -- et de saisir son
ticket. Cela aura pour effet de l'associer à une chambre, et donc de
l'ajouter dans la configuration du DHCP.

Si un utilisateur non enregistré tente de surfer sur le web, il sera
immédiatement redirigé vers l'URL d'enregistrement, et devra suivre la
procédure d'inscription.

Il n'y a pas besoin de se soucier de sortir les gens des chambres une
fois qu'ils sont parti : en effet, le ticket faisant office de preuve
d'occupation de la chambre, il montre aussi que l'occupant précédent est
parti.

Actualité et maintenance
------------------------

Une partie du site est dédiée à l'actualité de Maiznet : les différentes
dépèches sont écrites, on peut voir l'état des services, etc. De plus,
lors d'un problème sur le réseau, les administrateurs peuvent poster des
messages d'informations, indiquant le problème, sa date de début et sa
date de fin.

Le site Maiznet.fr est porté à la connaissance des utilisateurs lors de
leur inscription, libre à eux de s'y intéresser ou non.

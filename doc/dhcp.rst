.. _appli-dhcp:

Application *DHCP*
==================

Une fois les utilisateurs enregistrés, il faut leur attribuer une
adresse IP dans la plage des utilisateurs enregistrés -- à savoir
172.17.128.0/18. Cela se fait bien entendu par DHCP. Cependant, le
serveur DHCP ne se connecte pas directement sur la base SQL, et à la
place l'application DHCP se charge de générer le fichier de
configuration, qui est téléchargé périodiquement par le serveur.

Le téléchargement de la configuration est expliqué plus en détail sur
`wikimin
<http://wikimin.maiznet.fr/doku.php?id=projets:dhcpdoc:confup>`_.

Génération des IP
-----------------

L'application DHCP a simplement pour but la génération du fichier
dhcp.conf qui sera téléchargé sur le serveur. C'est dans le fichier de
template que le modèle du dhcpd.conf est défini.

La génération des IP doit être effectuée en prenant en compte certains
critères :

  - Il faut éviter de tomber à cours de place.
  - Quand une adresse MAC se voit attribuer une IP, il ne faut pas
    qu'elle en change...
  - ... et encore moins qu'une IP déjà attribuée soit re-attribuée
    immédiatement à une autre adresse MAC.

Pour cela, chaque chambre a son subnet IP, et les adresses MAC de
l'utilisateurs se voient attribuer des IP membres de ce subnet.
Cependant, elles ne sont pas toujours attribuées de manière contigüe :
admettons qu'un utilisateur ait les adresses MAC A, B et C. S'il
supprime la C, en ayant des adresses contigües la MAC C prendrait
l'adresse de B. Pour éviter le problème, on utilise le modèle Slot, qui
garde en mémoire l'état d'attribution des IP, et attribue le « premier
trou » aux nouvelles MAC.

Code
----

Vues
~~~~

.. automodule:: maiznet.dhcp.views
    :members:

Modèles
~~~~~~~

.. automodule:: maiznet.dhcp.models
    :members:

Utilitaires
~~~~~~~~~~~

.. automodule:: maiznet.dhcp.utils
    :members:

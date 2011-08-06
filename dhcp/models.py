########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> dhcp/models.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.db import models
from django.utils import simplejson
from maiznet.register.models import Presence
from maiznet.dhcp import utils
from IPy import intToIp

_enc = simplejson.JSONEncoder().encode
_dec = simplejson.JSONDecoder().decode

def make_ip(room, machine):
	"""
	Génère une IP à partir du numéro de chambre et de l'index de la
	machine. Il s'agit d'appliquer le plan d'adressage de Maiz pour
	les résidents enregistrés. Au cas où la documentation se perde,
	voici comment c'est foutu :

	    172.17.R S C C C C C C . C C C M M M M M

	172.17 est le préfixe, y'a pas de souci avec ça.

	R et S définissent le type de machine. Dans le cas d'un résident
	enregistré, c'est 10. (00 pour un serveur, 01 pour un switch, et
	11 pour un invité).

	Les bits C définissent le numéro de chambre.

	Les bits M définissent le numéro de machine.

	La fonction prends en argument les numéros de chambre et de
	machine, et retourne une chaîne contenant l'IP valide.
	"""

	# On utilise la classe BinString qui permet de créer une "chaîne
	# binaire" bits par bits assez simplement.
	s = utils.BinString()

	# Si on ne peut pas encoder la chambre, on gueule
	if len(bin(room)) > 11:
		raise Exception(_('Could not generate IP: room number to high (%(number)d)') % {'number': room})

	# Si on ne peut pas encoder la machine, on laisse l'utilisateur
	# se démerder avec ses IP multiples
	machine = machine % 31

	# 172.17, le préfixe Maiznet
	s += utils.tobinrep(172, 8)
	s += utils.tobinrep(17, 8)

	# On a une IP de résident, donc les deux bits suivants sont 10
	s += '10'

	# On ajoute ensuite la chambre et la machine
	s += utils.tobinrep(room, 9)
	s += utils.tobinrep(machine, 5)

	# Et finalement, on génère l'IP
	ip = intToIp(s.to_int(), 4)

	return ip

class Slot(models.Model):
	"""
	Quand on génère la configuration du DHCP, on attribue les
	adresses IP aux adresses MAC, et jusque là tout va bien.
	Cependant, dans un système trop naïf, les IP seraient attribuées
	dans l'ordre de présence des adresses MAC dans la base. Mais
	prenons par exemple le cas d'un utilisateur qui a 5 adresses
	MAC, et qui supprime la 3ème. Dans ce cas, la 4ème devient la
	3ème, et la 5ème devient la 4ème. Ce qui pose problème, car si
	les machines sont connectées pendant ce temps là, l'ex-5ème
	risque de prendre l'IP de la 4ème.

	Cette version du problème est simplifiée, et pour des raisons
	d'implémentation il y a tout un tas d'autres cas dans lesquels
	on risque de générer un conflit d'IP.

	Par conséquent, quand on assigne une IP à une MAC, on l'assigne
	définitivement (jusqu'au changement de chambre). Le but de cette
	classe est de garder en mémoire les assignations, ainsi que de
	génerer les nouvelles assignations quand il le faut.
	"""

	presence = models.ForeignKey(Presence)
	assign = models.TextField(blank=True, null=True)

	def _get_attribution(self, commit = True):
		"""
		Là c'est la fonction joyeux bordel. Elle s'occupe de
		faire l'ajout/suppression de MAC depuis la dernière
		fois, et de calculer l'index de chaque MAC, ce qui
		servira à donner une IP. Comprendra l'algorithme qui
		pourra :)

		L'important, c'est que cette méthode retourne un
		dictionnaire indexe => MAC, qui permet de savoir quel
		est le "numéro" de la MAC dans la chambre.

		L'option commit sert à éviter l'écriture de la mise à
		jour dans la base. À priori, ça ne sert à rien de la
		mettre à False, mais sait-on jamais.

		Un autre détail : normalement, personne n'aura jamais à
		toucher à cette fonction. Elle est indépendante du
		nombre d'IP par chambre etc, donc même en cas de
		changement du plan d'adressage, elle devrait continuer à
		fonctionner.

		--> Pour résumer : ne vous souciez _jamais_ de cette
		fonction, ne l'appellez pas, ne cherchez pas à savoir
		comment elle fonctionne.
		"""
		try:
			m = _dec(self.assign)
		except:
			m = {}

		macs = {}
		for mac in self.presence.netif.split(','):
			try:
				macs[mac] = int(m.keys()[m.values().index(mac)])
			except:
				macs[mac] = None

		m = {}
		for k, v in macs.items():
			if v != None:
				m[v] = k
			else:
				i = 0
				while True:
					try:
						macs.values().index(i)
						i += 1
					except ValueError:
						m[i] = k
						macs[k] = i
						break

		self.assign = _enc(m)

		if commit:
			self.save()

		return m

	def get_ips(self, commit = True):
		"""
		Ça, c'est la fonction qui retourne la liste des IP d'une
		Presence. Elle se charge toute seule d'appeller
		get_attribution().
		"""
		attrs = self._get_attribution(commit)

		room = self.presence.room_id

		out = []
		for k, v in attrs.items():
			out.append({
				'host': '%s_%d' % (self.presence.user.username.lower(), k),
				'mac': v,
				'ip': make_ip(room, k + 1),
			})

		return out

# Bon, si je met pas ça là, j'ai une boucle d'import. C'est crade, soit.
def presence_get_slot(self):
	try:
		s = Slot.objects.get(presence=self)
	except Slot.DoesNotExist:
		s = Slot(presence=self)

	return s
Presence.get_slot = presence_get_slot

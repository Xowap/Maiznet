########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> tools/tipmac/tipmac.py
#
#
# Copyright 2011 Grégoire Leroy <gregoire.leroy@retenodus.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
import socket
import IPy
import scapy.all as scapy

def main():
	"""
	Fonction principale du démon tipmac. Elle attend des connexions
	entrantes lui demandant d'établir la correspondance IP/MAC.
	"""

	HOST=''
	PORT=1337

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	while 1 :
		conn, addr = s.accept()
		data = conn.recv(1024)
		print data
		ip = IPy.IP(data).strNormal()
		ans,unans = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=ip),timeout=2)
		try :
			a  = ans[0][1].sprintf("%src%")
		except :
			a = "fail"

		conn.send(a)
		conn.close()

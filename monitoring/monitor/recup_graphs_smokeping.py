import os, sys
import Image
import config

def traitement(fichier, ligne):
	"sauvegarde le graphe du smokeping, et en genere une miniature"

	graphe = Image.open(fichier)
	graphe.save(config.IMAGES_PATH + ligne + ".png", "PNG")
	graphe.crop((68, 31, 675, 231)).resize((200, 150), Image.ANTIALIAS).save(config.IMAGES_PATH + "mini_" + ligne + ".png", "PNG")

images = [
	(config.SMOKEPING + "adsl1_last_3600.png", "adsl1"),
	(config.SMOKEPING + "adsl2_last_3600.png", "adsl2"),
	(config.SMOKEPING + "adsl3_last_3600.png", "adsl3"),
	(config.SMOKEPING + "sdsl_last_3600.png", "sdsl")
]
for fichier, ligne in images:
	traitement(fichier, ligne)

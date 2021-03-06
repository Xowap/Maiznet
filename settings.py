########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> settings.py
#
#
# Copyright 20xx Xxxxx Xxxxx <xxxx.xxxx@xxxxxx.xxx>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

# Configuration Django pour le site Maiznet.fr

# Import des paramètres spécifiques au serveur
from local_settings import *

MANAGERS = ADMINS

SITE_ID = 1

# Code de langage
LANGUAGE_CODE = 'en'

LANGUAGES = (
	('fr', 'Français'),
	('en', 'English'),
)

# On utilise l'internationalisation (et oui, il y a des étranger qui
# viennent à Maiz, il est important d'avoir au moins une version
# anglaise !)
USE_I18N = True

# De même, active la localisation, c'est à dire le formattage des dates
# au format usuel de la langue utilisée.
USE_L10N = True

# Chemin absolu vers le répertoire qui contient les fichiers media
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = relpath + '/media/'

# Profil des utilisateurs
AUTH_PROFILE_MODULE = "register.Presence"

# Liste des fonctions qui peuvent importer des templates depuis diverses
# sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

FIXTURE_DIRS = (
	relpath + '/news/fixtures',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'piwik.django.middleware.PiwikMiddleware',
)

ROOT_URLCONF = 'maiznet.urls'

TEMPLATE_DIRS = (
	relpath + '/templates/',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.admin',

	'modeltranslation',
	'piwik.django',

	'maiznet.news',
	'maiznet.monitoring',
	'maiznet.register',
	'maiznet.dhcp',
	'maiznet.pages',
)

MODELTRANSLATION_TRANSLATION_REGISTRY = 'maiznet.translation'

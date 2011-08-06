########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> dhcp/tests.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}


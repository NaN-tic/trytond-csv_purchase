# This file is part of the csv_purchase module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class CSVPurchaseTestCase(ModuleTestCase):
    'Test CSV Purchase module'
    module = 'csv_purchase'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CSVPurchaseTestCase))
    return suite

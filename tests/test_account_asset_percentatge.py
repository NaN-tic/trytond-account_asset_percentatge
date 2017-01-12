# This file is part account_asset_percentatge module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction
from decimal import Decimal


class AccountAssetPercentatgeTestCase(unittest.TestCase):
    'Test Account Asset Percentatge module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('account_asset_percentatge')
        self.template = POOL.get('product.template')

    def test0005views(self):
        'Test views'
        test_view('party')

    def test0006depends(self):
        'Test depends'

    def test0010percentatge(self):
        'Test percentatge'
        with Transaction().start(DB_NAME, USER,
                context=CONTEXT) as transaction:
            template1 = self.template()
            template1.depreciation_percentatge = 1
            r = template1.on_change_depreciation_percentatge()
            self.assertEqual(r['depreciation_duration'], 12)

            template2 = self.template()
            template2.depreciation_percentatge = 0.5
            r = template2.on_change_depreciation_percentatge()
            self.assertEqual(r['depreciation_duration'], 24)

            template3 = self.template()
            template3.depreciation_duration = Decimal('6')
            r = template3.on_change_depreciation_duration()
            self.assertEqual(r['depreciation_percentatge'], Decimal('2'))

            template4 = self.template()
            template4.depreciation_duration = Decimal('18')
            r = template4.on_change_depreciation_duration()
            self.assertEqual(r['depreciation_percentatge'],
                Decimal('0.6666666666666666666666666667'))


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountAssetPercentatgeTestCase))
    return suite

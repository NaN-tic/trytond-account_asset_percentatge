# This file is part account_asset_percentatge module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.pool import Pool
from decimal import Decimal


class AccountAssetPercentatgeTestCase(ModuleTestCase):
    'Test Account Asset Percentatge module'
    module = 'account_asset_percentatge'

    @with_transaction()
    def test_percentatge(self):
        'Test percentatge'
        Template = Pool().get('product.template')

        template1 = Template()
        template1.depreciation_percentatge = 1
        template1.on_change_depreciation_percentatge()
        self.assertEqual(template1.depreciation_duration, 12)

        template2 = Template()
        template2.depreciation_percentatge = 0.5
        template2.on_change_depreciation_percentatge()
        self.assertEqual(template2.depreciation_duration, 24)

        template3 = Template()
        template3.depreciation_duration = Decimal('6')
        template3.on_change_depreciation_duration()
        self.assertEqual(template3.depreciation_percentatge, Decimal('2'))

        template4 = Template()
        template4.depreciation_duration = Decimal('18')
        template4.on_change_depreciation_duration()
        self.assertEqual(template4.depreciation_percentatge,
            Decimal('0.6666666666666666666666666667'))


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountAssetPercentatgeTestCase))
    return suite

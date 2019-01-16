# This file is part account_asset_percent module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta, Pool
from trytond import backend

__all__ = ['Template']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    depreciation_percentatge = fields.Numeric(
            'Depreciation Percentatge', digits=(16, 4),
            states={
                'readonly': ~Eval('active', True),
                'invisible': (~Eval('depreciable')
                    | (Eval('type', '') != 'assets')
                    | ~Eval('context', {}).get('company')),
                },
            depends=['depreciable', 'active', 'type'],
            help='% deprecation to calculate months')

    @fields.depends('depreciation_percentatge')
    def on_change_depreciation_percentatge(self):
        if self.depreciation_percentatge:
            depreciation_duration = (12 / self.depreciation_percentatge)
            self.depreciation_duration = int(round(depreciation_duration))
            self.depreciation_percentatge = (
                12 / depreciation_duration)

    @fields.depends('depreciation_duration')
    def on_change_depreciation_duration(self):
        if self.depreciation_duration:
            self.depreciation_percentatge = (
                12 / self.depreciation_duration)

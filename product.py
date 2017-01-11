# This file is part account_asset_percent module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Template']


class Template:
    __metaclass__ = PoolMeta
    __name__ = 'product.template'
    depreciation_percentatge = fields.Property(fields.Numeric(
            'Depreciation Percentatge', digits=(16, 0),
            states={
                'readonly': ~Eval('active', True),
                'invisible': (~Eval('depreciable')
                    | (Eval('type', '') != 'assets')
                    | ~Eval('context', {}).get('company')),
                },
            depends=['active', 'depreciable', 'type'],
            help='% deprecation to calculate months'))

    @fields.depends('depreciation_percentatge')
    def on_change_depreciation_percentatge(self):
        changes = {}
        if self.depreciation_percentatge:
            changes['depreciation_duration'] = (
                12 * self.depreciation_percentatge) / 100
        return changes

    @fields.depends('depreciation_duration')
    def on_change_depreciation_duration(self):
        changes = {}
        if self.depreciation_duration:
            changes['depreciation_percentatge'] = (
                self.depreciation_duration * 100) / 12
        return changes

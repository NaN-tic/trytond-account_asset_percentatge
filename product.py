# This file is part account_asset_percent module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta, Pool
from trytond import backend

__all__ = ['Template']


class Template:
    __metaclass__ = PoolMeta
    __name__ = 'product.template'
    depreciation_percentatge = fields.MultiValue(fields.Numeric(
            'Depreciation Percentatge', digits=(16, 4),
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

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'depreciation_percentatge'}:
            return pool.get('product.template.account')
        return super(Template, cls).multivalue_model(field)


class TemplateAccount:
    __metaclass__ = PoolMeta
    __name__ = 'product.template.account'

    depreciation_percentatge = fields.Numeric(
        'Depreciation Percentatge', digits=(16, 4),
        states={
            'readonly': ~Eval('active', True),
            'invisible': (~Eval('depreciable')
                | (Eval('type', '') != 'assets')
                | ~Eval('context', {}).get('company')),
            },
        depends=['active', 'depreciable', 'type'])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)
        if exist:
            table = TableHandler(cls, module_name)
            exist &= (table.column_exist('depreciation_percentatge'))

        super(TemplateAccount, cls).__register__(module_name)

        if not exist:
            # Re-migration
            cls._migrate_property([], [], [])

# This file is part account_asset_percent module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pyson import Eval
from trytond.pool import PoolMeta
from trytond.modules.currency.fields import Monetary


class Asset(metaclass=PoolMeta):
    __name__ = 'account.asset'
    purchase_value = Monetary('Purchase Value',
        digits='currency', currency='currency', states={
            'readonly': (Eval('lines', [0]) | (Eval('state') != 'draft')),
        }, depends=['state'])

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.account_journal.context = {'company': Eval('company', -1)}
        cls.account_journal.depends.add('company')
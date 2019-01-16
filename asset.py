# This file is part account_asset_percent module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Asset']


class Asset(metaclass=PoolMeta):
    __name__ = 'account.asset'
    purchase_value = fields.Numeric('Purchase Value',
        digits=(16, Eval('currency_digits', 2)), states={
            'readonly': (Eval('lines', [0]) | (Eval('state') != 'draft')),
            },
        depends=['currency_digits', 'state'])

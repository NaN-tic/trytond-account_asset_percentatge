# This file is part account_asset_percentatge module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .asset import *
from .product import *


def register():
    Pool.register(
        Asset,
        Template,
        module='account_asset_percentatge', type_='model')

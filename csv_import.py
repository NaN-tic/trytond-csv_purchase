# This file is part of csv_purchase module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def _add_default_values(cls, model, values, parent_values=None):
        '''
        Get default values from Purchase and PurchaseLine objects
        '''
        values = super(CSVArchive, cls)._add_default_values(model, values, parent_values)

        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        PurchaseLine = pool.get('purchase.line')
        Company = pool.get('company.company')

        model_name =  model.__name__

        if model_name == 'purchase.purchase':
            party = values.get('party')
            if party:
                Party = pool.get('party.party')
                party = Party(party)
                model.party = party

                if values.get('invoice_address'):
                    if not values.get('invoice_address') in party.addresses:
                        del values['invoice_address']

                vals = Purchase(**values).on_change_party()
                vals.update(values)
                values = vals.copy()

        if model_name == 'purchase.line':
            if values.get('product') and values.get('quantity'):
                currency = parent_values.get('currency')
                if not currency:
                    company = Transaction().context.get('company')
                    if company:
                        currency = Company(company).currency.id
                values = {
                    'product': values.get('product'),
                    '_parent_purchase.currency': currency,
                    '_parent_purchase.party': parent_values.get('party'),
                    'purchase': None,
                    'type': 'line',
                    'quantity': values.get('quantity'),
                    'unit': None,
                    'description': None
                }
                values.update(PurchaseLine(**values).on_change_product())
                values.update(PurchaseLine(**values).on_change_quantity())
                del values['_parent_purchase.currency']
                del values['_parent_purchase.party']
                del values['purchase']

        return values

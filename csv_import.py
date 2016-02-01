# This file is part of csv_purchase module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def _import_data_purchase(cls, record, values, parent_values=None):
        '''
        Purchase and Purchase Line data
        '''
        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        Line = pool.get('purchase.line')
        Party = pool.get('party.party')

        record_name = record.__name__

        if record_name == 'purchase.purchase':
            party = values.get('party')

            if party:
                party = Party(party)

                if not record.id:
                    default_values = record.default_get(record._fields.keys())
                    for key in default_values:
                        if 'rec_name' not in key:
                            setattr(record, key, default_values[key])
                    record.party = party
                record.on_change_party()

                if values.get('invoice_address') \
                        and values.get('invoice_address') in party.addresses:
                    record.invoice_address = values.get('invoice_address') 

                if values.get('lines'):
                    record.lines = values.get('lines')

                return record

        if record_name == 'purchase.line':
            if values.get('product') and values.get('quantity'):
                purchase = Purchase()
                default_values = Purchase.default_get(Purchase._fields.keys(),
                        with_rec_name=False)
                for key in default_values:
                    setattr(purchase, key, default_values[key])
                purchase.party = parent_values.get('party')
                purchase.on_change_party()

                line = Line()
                line.purchase = purchase
                line.product = values.get('product')
                line.quantity = values.get('quantity')
                line.on_change_product()

                return line

        return record

# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"
    _description = "Purchase Analysis Report"

    PURCHASE_ORDER_STATES = [
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ]

    currency_id2 = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda Secundaria',
        readonly=True
    )

    price_subtotal_rate = fields.Monetary(
        string="Subtotal Moneda secundaria",
        readonly=True,
        currency_field='currency_id2'  # Best practice: link the currency field explicitly
    )

    def _select(self):
        """ Inject custom fields into the SELECT statement. """
        select_str = super(PurchaseReport, self)._select()
        # Use 'po' for purchase_order and 'l' for purchase_order_line.
        # Since price_subtotal_rate is a measure, it must be aggregated using SUM().
        select_str += ", po.currency_id2 as currency_id2, sum(l.price_subtotal_rate) as price_subtotal_rate"
        return select_str

    def _group_by(self):
        """ Inject custom dimensions into the GROUP BY statement. """
        group_by_str = super(PurchaseReport, self)._group_by()
        # Only group by the dimension (currency_id2), not the measure (price_subtotal_rate).
        group_by_str += ", po.currency_id2"
        return group_by_str
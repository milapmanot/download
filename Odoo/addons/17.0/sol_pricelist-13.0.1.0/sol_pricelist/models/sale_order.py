# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('pricelist_id')
    def onchange_pricelist_id(self):
        for line in self.order_line:
            line.price_list_id = self.pricelist_id.id
            line.product_id_change()
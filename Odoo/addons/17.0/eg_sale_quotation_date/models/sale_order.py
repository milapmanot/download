from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        date_order = self.date_order
        res = super(SaleOrder, self).action_confirm()
        self.date_order = date_order
        return res

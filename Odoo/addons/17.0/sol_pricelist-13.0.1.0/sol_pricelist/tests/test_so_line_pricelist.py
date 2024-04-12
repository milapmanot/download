from odoo.tests.common import TransactionCase


class TestSOLinePricelist(TransactionCase):

    def setUp(self):
        super(TestSOLinePricelist, self).setUp()
        self.SaleOrder = self.env["sale.order"]
        self.ProductPricelist = self.env['product.pricelist']

        self.at_receivable = self.env["account.account.type"].create({
            "name": "Test receivable account",
            "type": "receivable",
            "internal_group": "asset"
        })
        self.a_receivable = self.env["account.account"].create({
            "name": "Test receivable account",
            "code": "TEST_RA",
            "user_type_id": self.at_receivable.id,
            "reconcile": True,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'property_product_pricelist': 1,
            'property_account_receivable_id': self.a_receivable.id,
        })
        self.product = self.env['product.template'].create({
            'name': 'Product Test',
            'list_price': 100.00,
        })
        self.sale_pricelist_id_1 = self.ProductPricelist.create({
            'name': 'Test Sale pricelist',
            'item_ids': [(0, 0, {
                    'applied_on': '1_product',
                    'compute_price': 'fixed',
                    'fixed_price': 300.00,
                    'product_tmpl_id': self.product.id,
                })],
        })
        self.sale_pricelist_id_2 = self.ProductPricelist.create({
            'name': 'Test Sale pricelist 2',
            'item_ids': [(0, 0, {
                'applied_on': '1_product',
                'compute_price': 'fixed',
                'fixed_price': 200.00,
                'product_tmpl_id': self.product.id,
            })],
        })
        self.sale_order = self.SaleOrder.create({
            'partner_id': self.partner.id,
            'pricelist_id': self.sale_pricelist_id_1.id
        })


    def test_account_so_line_change_pricelist(self):
        so_line_1 = self.sale_order.order_line.create({
            'order_id': self.sale_order.id,
            'product_id': self.product.product_variant_ids[:1].id,
            'price_list_id':self.sale_pricelist_id_1.id,
            'product_uom_qty': 1.0,
            'name': 'Test line',
        })
        so_line_2 = self.sale_order.order_line.create({
            'order_id': self.sale_order.id,
            'product_id': self.product.product_variant_ids[:1].id,
            'price_list_id': self.sale_pricelist_id_2.id,
            'product_uom_qty': 1.0,
            'name': 'Test line',
        })
        price = so_line_1.price_unit + so_line_2.price_unit
        self.assertEqual(price, 500.00, "Check prices !")

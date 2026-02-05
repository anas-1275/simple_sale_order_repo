from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_id = fields.Many2one('product.template')
    quantity = fields.Float()
    price_unite = fields.Float()
    
    def confirm_action_action(self):
        for rec in self:
            for line in rec.order_line:
                self.env['simple.sale.order'].create({
                    'customer_id': rec.partner_id.id,
                    'order_date': rec.date_order,
                    'user_id':rec.user_id.id,
                    'sale_order_id': rec.id,
                    'line_ids': [(0, 0, {
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'price_unite': line.price_unit,
                    })]
                })


    def open_records_action(self):
          action=self.env['ir.actions.actions']._for_xml_id('simple_sales_manager.simple_sale_order_action')
          action['context'] ={'default_sale_order': self.id}
        #   action['domain'] = [('customer_id', '=', self.partner_id.id),('order_date', '=', self.date_order),('user_id','=',self.user_id.id)]
          action['domain'] = [('sale_order_id', '=', self.id),]
          return action

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_id = fields.Many2one('product.template')
    quantity = fields.Float()
    price_unite = fields.Float()
    currency_id = fields.Many2one(
        comodel_name='res.currency',
    )
    
    def confirm_action_action(self):
            for rec in self:
                existing_order = self.env['simple.sale.order'].search([('sale_order_id', '=', rec.id)], limit=1)
                
                if existing_order:
                    raise ValidationError("this record already exist")
                else:
                    line_data = []
                    for line in rec.order_line:
                        line_data.append((0, 0, {
                            'product_id': line.product_id.id,
                            'quantity': line.product_uom_qty,
                            'price_unite': line.price_unit,
                        }))
                        
                    self.env['simple.sale.order'].create({
                        'customer_id': rec.partner_id.id,
                        'order_date': rec.date_order,
                        'user_id': rec.user_id.id,
                        'sale_order_id': rec.id,
                        'currency_id': rec.currency_id.id,
                        'line_ids': line_data
                    })


    def open_records_action(self):
          action=self.env['ir.actions.actions']._for_xml_id('simple_sales_manager.simple_sale_order_action')
          action['context'] ={'default_sale_order': self.id}
        #   action['domain'] = [('customer_id', '=', self.partner_id.id),('order_date', '=', self.date_order),('user_id','=',self.user_id.id)]
          action['domain'] = [('sale_order_id', '=', self.id),]
          return action

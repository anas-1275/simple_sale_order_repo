from odoo import fields,models,api
from odoo.exceptions import ValidationError,UserError

class SimpleSaleOrder(models.Model):
    _name="simple.sale.order"

    name=fields.Char(default="New" ,readonly=1)
    user_id=fields.Many2one('res.users')
    customer_id=fields.Many2one('res.partner')
    
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
    )
    
    order_date=fields.Date()
    state=fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('done','Done'),
    ],default="draft",readonly=1)
    
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        required=1
    )
    
    total_amount=fields.Monetary( compute='_compute_calculate_all_subtotal', currency_field='currency_id') #Monetary collects currency and money 
    
    line_ids = fields.One2many(
        comodel_name='simple.sale.order.line',
        inverse_name='order_id',
    )
    
    note=fields.Text()
    
    @api.depends('line_ids.subtotal')
    def _compute_calculate_all_subtotal(self):
        for rec in self:
            rec.total_amount=sum(rec.line_ids.mapped('subtotal'))



    _sql_constraints=[
        ('unique_name','unique(name)','This Name Is Exist!')
    ]

    def draft_action(self):
        for rec in self:
            rec.state='draft'
    
    def confirmed_action(self):
        for rec in self:
            if not rec.line_ids or rec.total_amount == 0.00 :
                raise ValidationError("You Must Do atleast 1 Lines ")
            else:
               rec.state='confirmed'
            
    
    def done_action(self):
        for rec in self:
            rec.state='done'



    def create(self,vals):
        vals['name']=self.env['ir.sequence'].next_by_code('simple_sale_order_seq')
        return super().create(vals)







class SimpleSaleOrderLine(models.Model):
    _name="simple.sale.order.line"

    order_id=fields.Many2one('simple.sale.order')
    
    product_id = fields.Many2one(
        comodel_name='product.product',
        required=1,
    )
    quantity=fields.Float(required=1)
    price_unite=fields.Monetary(currency_field='currency_id',required=1)
    currency_id=fields.Many2one('res.currency',related='order_id.currency_id' ,readonly=1)
    subtotal=fields.Monetary(compute="_compute_calculate" ,currency_field='currency_id',readonly=1)


    # @api.onchange('order_id','currency id')
    # def _onchange_product(self):
    #     if self.order_id.currency_id:
    #         self.currency_id = self.order_id.currency_id

    
    @api.depends('quantity','price_unite')
    def _compute_calculate(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price_unite


   
    
    
    
    
    
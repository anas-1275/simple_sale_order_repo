from odoo import http
from odoo.http import request
import io
import xlsxwriter
import base64
from odoo import fields,models
from odoo.exceptions import ValidationError,UserError


class PrintReportWizerd(models.TransientModel):
    _name="print.report.wizerd"

    date_from=fields.Date()
    date_to=fields.Date()
    simple_sale_id=fields.Many2one('simple.sale.order')

    def action_confirm(self):
        orders = self.env['simple.sale.order'].search([   
        ('order_date', '>=', self.date_from),
        ('order_date', '<=', self.date_to),]) 
        if not orders:
            raise ValidationError("No Sale Order Found")
        action = self.env.ref('simple_sales_manager.simple_sale_order_report').report_action(orders)
        return action
        # self.env.ref ----> search for xml file by external id // report_action --> do report with records that inside the order

    def action_excel(self):
        orders = self.env['simple.sale.order'].search([
            ('order_date', '>=', self.date_from),
            ('order_date', '<=', self.date_to),
        ])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sales Report')
        
        header_format = workbook.add_format({'bold': True, 'bg_color': '#714B67', 'color': 'white'})
        headers=['Name','Customer','Order Date','Currency','User','state','Total Amount']
        for col_num,header in enumerate(headers):
              worksheet.write(0,col_num,header,header_format)

        row = 1
        for order in orders:
            worksheet.write(row, 0, order.name or '')
            worksheet.write(row, 1, order.customer_id.name if order.customer_id else '')
            worksheet.write(row, 2, str(order.order_date) if order.order_date else '')
            worksheet.write(row, 3, order.currency_id.name if order.currency_id else '')
            worksheet.write(row, 4, order.user_id.name if order.user_id else '')
            
             
            state_label = dict(order._fields['state'].selection).get(order.state, '')
            worksheet.write(row, 5, state_label)
            
            worksheet.write(row, 6, order.total_amount or 0.0)
            row += 1

        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.read())
        output.close()

        attachment = self.env['ir.attachment'].create({
            'name': 'Sales_Report_%s.xlsx' % fields.Date.today(),
            'type': 'binary',
            'datas': file_data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
    

    def action_list_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'simple.sale.order',
            'view_mode': 'tree,form',
            'domain': [
                ('order_date', '>=', self.date_from),
                ('order_date', '<=', self.date_to),
            ],
            'target': 'current',
        }
        




    

    
        
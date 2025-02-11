from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    requests_for_quotation = fields.Char(string='Requests for quotation Number')

    def create(self, vals_list):
        if vals_list.get('name', 'New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code('requests.for.quotation.sequence')
        return super(PurchaseOrder, self).create(vals_list)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        # self.requests_for_quotation = self.name
        self.write({
            'name': self.env['ir.sequence'].next_by_code('purchase.order'),
            'requests_for_quotation': self.name,

        })
        return res

    def action_cancel(self):
        res = super(PurchaseOrder, self).action_cancel()
        self.write({
            'name': self.requests_for_quotation or self.name,
            'Requests_for_quotation': False,
        })
        return res

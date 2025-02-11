from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('reject', 'Rejected')])
    reject_type = fields.Selection([
        ('active', 'Active'),
        ('reject', 'Rejected'),
        ('rej_cancel', 'Rejected & Cancel')], string='Reject Type', default='active')
    reject_reason = fields.Text(string="Reject Reason")
    show_cancel = fields.Boolean(string="Show Cancel Button", compute='_show_cancel', default=False)

    def _show_cancel(self):
        for rec in self:
            rec.show_cancel = False
            if rec.state in ['cancel', 'reject'] and rec.reject_type != 'rej_cancel':
                rec.show_cancel = True

    def button_reject(self):
        self.ensure_one()
        return {
            'name': _('Reject'),
            'view_mode': 'form',
            'res_model': 'reject.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'po_id': self.id}
        }

    def write(self, vals):
        if self.reject_type == 'rej_cancel':
            raise ValidationError("You cannot Edit a Permanent Rejected PO")
        return super(PurchaseOrder, self).write(vals)

    def unlink(self):
        res = super(PurchaseOrder, self).unlink()
        if self.reject_type == 'rej_cancel':
            raise ValidationError("You cannot Delete a Permanent Rejected PO")
        return res

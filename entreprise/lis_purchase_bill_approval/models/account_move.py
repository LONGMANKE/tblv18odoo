from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    approval_state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('to_approve', 'To Approve'),
            ('approved', 'Approved'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
            ('reject', 'Rejected')
        ],
        string='Status',
        default='draft',
    )
    reject_type = fields.Selection([
        ('active', 'Active'),
        ('reject', 'Rejected'),
        ('rej_cancel', 'Rejected & Cancel')], string='Reject Type', default='active')
    reject_reason = fields.Text(string="Reject Reason")
    show_cancel = fields.Boolean(string="Show Cancel Button", compute='_show_cancel', default=False)
    bill_url = fields.Char(string="Bill URL", compute="_bill_url")

    def _bill_url(self):
        for rec in self:
            rec.bill_url = rec.get_base_url() + '/odoo/bills/' + rec.id

    @api.depends('date', 'auto_post')
    def _compute_hide_post_button(self):
        for record in self:
            record.hide_post_button = (
                    record.state != 'approved'
                    or record.auto_post != 'no'
                    and record.date > fields.Date.context_today(record)

            )

    def button_send_approval(self):
        for rec in self:
            # account_admin_group = self.env.ref('account.group_account_manager')
            # template = self.env.ref('lis_purchase_bill_approval.bill_approval_template')
            # users = account_admin_group.users
            # for user in users:
            #     template.with_context(user=user).send_mail(rec.id, force_send=True,
            #                                                email_values={'email_to': user.email})
            rec.write({
                'approval_state': 'to_approve'
            })

    def button_approve(self):
        for rec in self:
            rec.write({
                'state': 'posted'
            })

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
            'context': {'bill_id': self.id}
        }

    def write(self, vals):
        if self.reject_type == 'rej_cancel':
            raise ValidationError("You cannot Edit a Permanent Rejected Bill")
        if vals.get('state'):
            if self.approval_state != vals.get('state'):
                vals.update({
                    'approval_state': vals.get('state')
                })
        return super(AccountMove, self).write(vals)

    def unlink(self):
        res = super(AccountMove, self).unlink()
        if self.reject_type == 'rej_cancel':
            raise ValidationError("You cannot Delete a Permanent Rejected Bill")
        return res

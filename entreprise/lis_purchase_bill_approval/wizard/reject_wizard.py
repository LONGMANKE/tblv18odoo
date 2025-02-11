from odoo import fields, models, api


class RejectWizard(models.TransientModel):
    _name = 'reject.wizard'
    _description = 'Reject Wizard'

    reason = fields.Text(string="Reason")


    def reject_record(self, record, state_field):
        record.button_cancel()
        record.write({
            'reject_type': 'reject',
            'reject_reason': self.reason,
            state_field: 'reject'
        })

    def reject_cancel_record(self, record, state_field):
        record.button_cancel()
        record.write({
            'reject_type': 'rej_cancel',
            'reject_reason': self.reason,
            state_field: 'reject'
        })

    def action_reject(self):
        po_id = self.env.context.get('po_id')
        bill_id = self.env.context.get('bill_id')
        purchase_obj = self.env['purchase.order'].sudo()
        bill_obj = self.env['account.move'].sudo()
        if bill_id:
            bill_rec = bill_obj.browse(int(bill_id))
            if bill_rec:
                self.reject_record(bill_rec, 'approval_state')

        if po_id:
            purchase_rec = purchase_obj.browse(int(po_id))
            if purchase_rec:
                self.reject_record(purchase_rec, 'state')

    def action_reject_cancel(self):
        po_id = self.env.context.get('po_id')
        bill_id = self.env.context.get('bill_id')
        purchase_obj = self.env['purchase.order'].sudo()
        bill_obj = self.env['account.move'].sudo()
        if bill_id:
            bill_rec = bill_obj.browse(int(bill_id))
            if bill_rec:
                self.reject_cancel_record(bill_rec, 'approval_state')

        if po_id:
            purchase_rec = purchase_obj.browse(int(po_id))
            if purchase_rec:
                self.reject_cancel_record(purchase_rec, 'state')

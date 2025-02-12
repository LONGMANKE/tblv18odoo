# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2024 ZestyBeanz Technologies.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountAccount(models.Model):
    _inherit = "account.account"
    
    
    approval_status = fields.Selection([('to_approve','To Approve'),('approved','Approved')],string='Approval Status', default='to_approve',tracking=True,copy=False)
    
    
    def action_approve(self):
        for rec in self:
            rec.approval_status = 'approved'
    
    def action_disapprove(self):
        for rec in self:
            rec.approval_status = 'to_approve'


class ValidateAccountMove(models.TransientModel):
    _inherit = "validate.account.move"

    def validate_move(self):
        if self._context.get('active_model') == 'account.move':
            domain = [('id', 'in', self._context.get('active_ids', [])), ('state', '=', 'draft')]
        elif self._context.get('active_model') == 'account.journal':
            domain = [('journal_id', '=', self._context.get('active_id')), ('state', '=', 'draft')]
        else:
            raise UserError(_("Missing 'active_model' in context."))
        moves = self.env['account.move'].search(domain).filtered('line_ids')
        accounts_in_draft = moves.mapped('line_ids.account_id').filtered(lambda acc: acc.approval_status == 'to_approve')
        if accounts_in_draft:
            unique_accounts = set()
            for acc in accounts_in_draft:
                unique_accounts.add((acc.code, acc.name))
            account_list = '\n'.join(['{}. {} {}'.format(idx+1, code, name) for idx, (code, name) in enumerate(unique_accounts)])
            raise UserError(_("The Following Accounts are Not Approved:\n{}\nPlease Contact the Accounts Approver or Administrator".format(account_list)))
        return super(ValidateAccountMove, self).validate_move()


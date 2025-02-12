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


class AccountMove(models.Model):
    _inherit = "account.move"
    
    
    def _post(self, soft=True):
        for rec in self:
            unapproved_accounts = rec.line_ids.filtered(lambda line: line.account_id and line.account_id.approval_status == 'to_approve')
            if unapproved_accounts:
                unique_accounts = set()
                for line in unapproved_accounts:
                    unique_accounts.add((line.account_id.code, line.account_id.name))
                account_list = '\n\t'.join(['{}. {} {}'.format(idx+1, code, name) for idx, (code, name) in enumerate(unique_accounts)])
                raise UserError("The Following Accounts are Not Approved:\n\t{}\nPlease Contact the Accounts Approver or Administrator!".format(account_list))
        return super(AccountMove, self)._post(soft)

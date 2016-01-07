# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2015 Argil Consulting - http://www.argil.mx
############################################################################
#    Coded by: Israel Cruz Argil (israel.cruz@argil.mx)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp import netsvc
from openerp.osv.orm import browse_record, browse_null


class account_invoice(orm.Model):
    _inherit = "account.invoice"


    def _get_invoice_line_key_cols(self, cr, uid, invoice_line): # Modificada
        return ('name', 'origin', 'discount',
                'invoice_line_tax_id', 'price_unit',
                'product_id', 'account_id',
                'account_analytic_id','vehicle_id','employee_id')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

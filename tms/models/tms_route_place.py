# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class TmsRoutePlace(models.Model):
    _name = 'tms.route.place'
    _order = 'sequence'

    route_id = fields.Many2one(
        'tms.route',
        string="Route")
    sequence = fields.Integer(default=10)
    place_id = fields.Many2one('tms.place', string="Place")
    state_id = fields.Many2one(
        'res.country.state',
        related="place_id.state_id",
        readonly=True,
        string="State")
    country_id = fields.Many2one(
        'res.country',
        related="place_id.country_id",
        readonly=True,
        string="Country")

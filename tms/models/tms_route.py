# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from openerp import _, api, exceptions, fields, models

import requests

import simplejson as json


class TmsRoute(models.Model):
    _name = 'tms.route'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Routes'

    name = fields.Char('Route Name', size=64, required=True, select=True)
    departure_id = fields.Many2one('tms.place', 'Departure', required=True)
    arrival_id = fields.Many2one('tms.place', 'Arrival', required=True)
    distance = fields.Float(
        'Distance (mi./kms)', digits=(14, 4),
        help='Route distance (mi./kms)', required=True)
    travel_time = fields.Float(
        'Travel Time (hrs)', digits=(14, 4),
        help='Route travel time (hours)')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
    driver_factor_ids = fields.One2many(
        'tms.factor', 'route_id',
        string="Expense driver factor")
    distance_loaded = fields.Float(
        string='Distance Loaded (mi./km)',
        required=True
        )
    distance_empty = fields.Float(
        string='Distance Empty (mi./km)',
        required=True
        )
    fuel_efficiency = fields.Float(required=True)

    @api.depends('distance_empty', 'distance')
    @api.onchange('distance_empty')
    def on_change_disance_empty(self):
        for rec in self:
            if rec.distance_empty < 0.0:
                raise exceptions.ValidationError(
                    _("The value must be positive and lower than"
                        " the distance route."))
            rec.distance_loaded = rec.distance - rec.distance_empty

    @api.depends('distance_loaded', 'distance')
    @api.onchange('distance_loaded')
    def on_change_disance_loaded(self):
        for rec in self:
            if rec.distance_loaded < 0.0:
                raise exceptions.ValidationError(
                    _("The value must be positive and lower than"
                        " the distance route."))
            rec.distance_empty = rec.distance - rec.distance_loaded

    @api.multi
    def get_route_info(self, error=False):
        for rec in self:
            departure = {
                'latitude': rec.departure_id.latitude,
                'longitude': rec.departure_id.longitude
            }
            arrival = {
                'latitude': rec.arrival_id.latitude,
                'longitude': rec.arrival_id.longitude
            }
            if not departure['latitude'] and not departure['longitude']:
                raise exceptions.UserError(_(
                    "The departure don't have coordinates."))
            if not arrival['latitude'] and not arrival['longitude']:
                raise exceptions.UserError(_(
                    "The arrival don't have coordinates."))
            if error:
                url = ''
            else:
                url = 'http://maps.googleapis.com/maps/api/distancematrix/json'
            origins = (str(departure['latitude']) + ',' +
                       str(departure['longitude']))
            destinations = (str(arrival['latitude']) + ',' +
                            str(arrival['longitude']))
            params = {
                'origins': origins,
                'destinations': destinations,
                'mode': 'driving',
                'language': self.env.lang,
                'sensor': 'false',
            }
            try:
                result = json.loads(requests.get(url, params=params).content)
                distance = duration = 0.0
                if result['status'] == 'OK':
                    res = result['rows'][0]['elements'][0]
                    distance = res['distance']['value'] / 1000.0
                    duration = res['duration']['value'] / 3600.0
                self.distance = distance
                self.travel_time = duration
            except:
                raise exceptions.UserError(_("Google Maps is not available."))

    @api.multi
    def open_in_google(self):
        for route in self:
            points = (
                str(route.departure_id.latitude) + ',' +
                str(route.departure_id.longitude) + ',' +
                str(route.arrival_id.latitude) + ',' +
                str(route.arrival_id.longitude))
            url = "/tms/static/src/googlemaps/get_route.html?" + points
        return {'type': 'ir.actions.act_url',
                'url': url,
                'nodestroy': True,
                'target': 'new'}

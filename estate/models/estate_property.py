from email.policy import default
from xmlrpc.client import Boolean
from dateutil.relativedelta import relativedelta
from odoo import fields, models

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    # Calcular una fecha futura
    three_months_from_now = fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=three_months_from_now, string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    status = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Recieved'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )
    active = fields.Boolean(default=True)